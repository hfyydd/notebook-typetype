"""
YAML-based model configuration layer for cloud-service deployment.

Enables a deployment where all model API keys and tier mappings live in a
single YAML file (config/models.yaml), so end users never have to configure
any models — the backend is fully managed.

Design goals:
- Zero touch for end users (no Settings → Models page needed)
- Multiple tiers (free / standard / premium) with different model quality/cost
- Secrets referenced via ${ENV_VAR} so keys never enter the yaml file itself
- Fully backward compatible: if no yaml exists, the original DB-based flow runs

This module only parses and exposes configuration. The actual model instances
are still built by ModelManager via Esperanto's AIFactory (see models.py), so
we plug in here as a "preferred data source" that the manager consults first.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

try:
    import yaml
except ImportError:  # pragma: no cover - pyproject already depends on it transitively
    yaml = None  # type: ignore[assignment]

# Location of the model configuration file, relative to the project root.
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "models.yaml"

# Regex to detect ${ENV_VAR} references inside yaml string values.
_ENV_REF_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")

# The model "purposes" that a tier can define. Kept in sync with
# ModelManager.get_default_model()'s model_type argument and DefaultModels slots.
SUPPORTED_PURPOSES = (
    "language",
    "embedding",
    "text_to_speech",
    "speech_to_text",
    "large_context",
)


@dataclass
class ModelConfig:
    """Configuration for a single model entry within a tier."""

    provider: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    # Catch-all for provider-specific fields (api_version, endpoint, project, ...).
    # These are forwarded verbatim into the Esperanto config dict.
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_esperanto_config(self) -> Dict[str, Any]:
        """Build the config dict consumed by Esperanto's AIFactory."""
        config: Dict[str, Any] = {}
        if self.api_key:
            config["api_key"] = self.api_key
        if self.base_url:
            config["base_url"] = self.base_url
        config.update(self.extra)
        return config


@dataclass
class TierConfig:
    """A tier is a named bundle of model configs, one per purpose."""

    name: str
    models: Dict[str, ModelConfig] = field(default_factory=dict)

    def get(self, purpose: str) -> Optional[ModelConfig]:
        return self.models.get(purpose)


class ModelConfigProvider:
    """
    Singleton that loads and caches config/models.yaml.

    Lifecycle:
    - On first access via get_instance(), attempts to load the yaml.
    - If the file is absent, the provider reports not available and the app
      falls back to the original DB-based model provisioning.
    - reload() re-reads the file; safe to call from a /models/reload endpoint.
    """

    _instance: Optional["ModelConfigProvider"] = None

    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
        self._config_path = config_path
        self._available: bool = False
        self._default_tier: Optional[str] = None
        self._tiers: Dict[str, TierConfig] = {}
        self._raw: Dict[str, Any] = {}

    @classmethod
    def get_instance(cls) -> "ModelConfigProvider":
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.load()
        return cls._instance

    # ------------------------------------------------------------------ #
    # Loading
    # ------------------------------------------------------------------ #

    def load(self) -> None:
        """Parse the yaml file (if present) into the in-memory tier map."""
        self._available = False
        self._default_tier = None
        self._tiers = {}
        self._raw = {}

        if yaml is None:
            logger.warning(
                "PyYAML not installed; YAML model config disabled. "
                "Install pyyaml to enable cloud-service model configuration."
            )
            return

        path = self._config_path
        if not path.exists():
            logger.info(
                f"No model config file at {path}. "
                f"Using database-based model configuration (legacy mode)."
            )
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Failed to parse model config {path}: {e}")
            return

        if not isinstance(raw, dict):
            logger.error(f"Model config {path} must be a mapping at the top level.")
            return

        self._raw = raw
        default_tier = raw.get("default_tier")
        tiers_raw = raw.get("tiers") or {}

        if not isinstance(tiers_raw, dict):
            logger.error("'tiers' in model config must be a mapping.")
            return

        for tier_name, tier_body in tiers_raw.items():
            if not isinstance(tier_body, dict):
                logger.warning(f"Tier '{tier_name}' is not a mapping; skipping.")
                continue
            tier = TierConfig(name=tier_name)
            for purpose, entry in tier_body.items():
                if purpose not in SUPPORTED_PURPOSES:
                    logger.debug(
                        f"Ignoring unsupported purpose '{purpose}' in tier '{tier_name}'."
                    )
                    continue
                if not isinstance(entry, dict):
                    logger.warning(
                        f"Entry for {tier_name}.{purpose} must be a mapping; skipping."
                    )
                    continue
                resolved = self._resolve_entry(entry)
                provider = resolved.pop("provider", None)
                model = resolved.pop("model", None)
                if not provider or not model:
                    logger.warning(
                        f"Tier '{tier_name}' purpose '{purpose}' is missing "
                        f"provider/model; skipping."
                    )
                    continue
                api_key = resolved.pop("api_key", None)
                base_url = resolved.pop("base_url", None)
                # Anything left is treated as provider-specific extra config.
                tier.models[purpose] = ModelConfig(
                    provider=provider,
                    model=model,
                    api_key=api_key,
                    base_url=base_url,
                    extra=resolved,
                )
            self._tiers[tier_name] = tier

        if not self._tiers:
            logger.warning(
                f"Model config {path} defined no valid tiers; YAML mode disabled."
            )
            return

        if default_tier and default_tier not in self._tiers:
            logger.warning(
                f"default_tier '{default_tier}' is not among defined tiers "
                f"{list(self._tiers)}; falling back to first tier."
            )
            default_tier = next(iter(self._tiers))

        if not default_tier:
            default_tier = next(iter(self._tiers))

        self._default_tier = default_tier
        self._available = True

        tier_names = list(self._tiers)
        logger.info(
            f"YAML model config loaded from {path}: "
            f"{len(tier_names)} tier(s) {tier_names}, default='{self._default_tier}'."
        )
        self._log_completeness_warnings()

    def _resolve_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve ${ENV_VAR} references in every string value of an entry."""
        resolved: Dict[str, Any] = {}
        for key, value in entry.items():
            resolved[key] = self._resolve_value(value)
        return resolved

    def _resolve_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self._resolve_env_refs(value)
        if isinstance(value, dict):
            return {k: self._resolve_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve_value(v) for v in value]
        return value

    def _resolve_env_refs(self, text: str) -> Any:
        """
        Replace ${ENV_VAR} tokens with os.environ values.

        If the whole string is a single ${VAR} reference and the var is unset,
        we return None so downstream code treats the field as "not configured"
        rather than an empty string.
        """
        full_match = _ENV_REF_PATTERN.fullmatch(text.strip())
        if full_match:
            var = full_match.group(1)
            return os.environ.get(var)

        def _sub(match: re.Match) -> str:
            return os.environ.get(match.group(1), "")

        return _ENV_REF_PATTERN.sub(_sub, text)

    def _log_completeness_warnings(self) -> None:
        """Warn about tiers that are missing required purposes or api keys."""
        for tier_name, tier in self._tiers.items():
            for purpose in ("language", "embedding"):
                cfg = tier.get(purpose)
                if cfg is None:
                    logger.warning(
                        f"Tier '{tier_name}' has no '{purpose}' model configured. "
                        f"Requests for this purpose will fall back to default tier."
                    )
                elif not cfg.api_key and cfg.provider not in ("ollama",):
                    logger.warning(
                        f"Tier '{tier_name}' purpose '{purpose}' has no api_key "
                        f"resolved (provider={cfg.provider}). "
                        f"Set the referenced environment variable."
                    )

    # ------------------------------------------------------------------ #
    # Public read API
    # ------------------------------------------------------------------ #

    def is_available(self) -> bool:
        """True when a valid yaml config is loaded."""
        return self._available

    def get_default_tier(self) -> Optional[str]:
        return self._default_tier

    def list_tiers(self) -> List[str]:
        return list(self._tiers.keys())

    def get_model_config(
        self, purpose: str, tier: Optional[str] = None
    ) -> Optional[ModelConfig]:
        """
        Return the ModelConfig for a purpose within a tier.

        Falls back to the default tier when:
        - tier is not specified, or
        - the requested tier doesn't exist, or
        - the requested tier exists but has no config for this purpose.
        """
        if not self._available:
            return None

        # Map a few "usage" aliases onto the atomic purposes so callers can
        # pass chat/tools/transformation and still resolve to a language model.
        purpose_key = purpose
        if purpose in ("chat", "tools", "transformation"):
            purpose_key = "language"

        if purpose_key not in SUPPORTED_PURPOSES:
            return None

        tier_name = tier or self._default_tier
        if tier_name and tier_name in self._tiers:
            cfg = self._tiers[tier_name].get(purpose_key)
            if cfg is not None:
                return cfg

        # Fall back to default tier.
        if self._default_tier and self._default_tier in self._tiers:
            return self._tiers[self._default_tier].get(purpose_key)

        return None

    def health_check(self) -> Dict[str, Any]:
        """
        Return a per-tier, per-purpose status report for /models/health.

        Secrets are never included — only whether the api_key resolved.
        """
        report: Dict[str, Any] = {
            "enabled": self._available,
            "default_tier": self._default_tier,
            "tiers": {},
        }
        for tier_name, tier in self._tiers.items():
            entry: Dict[str, Any] = {}
            for purpose in SUPPORTED_PURPOSES:
                cfg = tier.get(purpose)
                if cfg is None:
                    entry[purpose] = {"configured": False}
                else:
                    entry[purpose] = {
                        "configured": True,
                        "provider": cfg.provider,
                        "model": cfg.model,
                        "has_api_key": bool(cfg.api_key),
                    }
            report["tiers"][tier_name] = entry
        return report
