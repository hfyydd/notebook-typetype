from __future__ import annotations

from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field, field_validator

from open_notebook.domain.base import ObjectModel, RecordModel
from open_notebook.domain.transformation_defaults import (
    LOCALE_FALLBACKS,
    get_default_prompt_translations,
    get_system_transformation_translations,
)

DEFAULT_TRANSFORMATION_LOCALE = "en-US"


def _normalize_locale(locale: Optional[str]) -> str:
    return locale or DEFAULT_TRANSFORMATION_LOCALE


def _has_text(value: Optional[str]) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _to_translation_dict(entry: Any) -> dict[str, Any]:
    if isinstance(entry, BaseModel):
        return entry.model_dump(exclude_none=True)
    if isinstance(entry, dict):
        return {key: value for key, value in entry.items() if value is not None}
    return {}


def _merge_translation_maps(*maps: dict[str, Any]) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for current_map in maps:
        for locale, fields in (current_map or {}).items():
            bucket = merged.setdefault(locale, {})
            bucket.update(_to_translation_dict(fields))
    return merged


def _build_locale_candidates(
    locale: Optional[str], source_locale: Optional[str]
) -> list[str]:
    current_locale = _normalize_locale(locale)
    candidates = [current_locale]

    fallback_locale = LOCALE_FALLBACKS.get(current_locale)
    if fallback_locale and fallback_locale not in candidates:
        candidates.append(fallback_locale)

    source = _normalize_locale(source_locale)
    if source not in candidates:
        candidates.append(source)

    if DEFAULT_TRANSFORMATION_LOCALE not in candidates:
        candidates.append(DEFAULT_TRANSFORMATION_LOCALE)

    return candidates


def _resolve_field(
    translations: dict[str, Any],
    locale: Optional[str],
    source_locale: Optional[str],
    field_name: str,
    fallback_value: str,
) -> str:
    for candidate in _build_locale_candidates(locale, source_locale):
        value = _to_translation_dict(translations.get(candidate)).get(field_name)
        if _has_text(value):
            return value
    return fallback_value


class TransformationTranslation(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None


class DefaultPromptTranslation(BaseModel):
    transformation_instructions: Optional[str] = None


class Transformation(ObjectModel):
    table_name: ClassVar[str] = "transformation"
    name: str
    title: str
    description: str
    prompt: str
    apply_default: bool
    source_locale: str = DEFAULT_TRANSFORMATION_LOCALE
    system_key: Optional[str] = None
    translations: dict[str, TransformationTranslation] = Field(default_factory=dict)

    @field_validator("translations", mode="before")
    @classmethod
    def _ensure_translation_map(cls, value: Any) -> dict[str, Any]:
        return value or {}

    def get_effective_translations(self) -> dict[str, TransformationTranslation]:
        merged = _merge_translation_maps(
            get_system_transformation_translations(self.system_key),
            self.translations,
        )
        return {
            locale: TransformationTranslation(**fields)
            for locale, fields in merged.items()
        }

    def resolve_localized_fields(self, locale: Optional[str]) -> dict[str, str]:
        translations = self.get_effective_translations()
        return {
            "name": _resolve_field(
                translations, locale, self.source_locale, "name", self.name
            ),
            "title": _resolve_field(
                translations, locale, self.source_locale, "title", self.title
            ),
            "description": _resolve_field(
                translations,
                locale,
                self.source_locale,
                "description",
                self.description,
            ),
            "prompt": _resolve_field(
                translations, locale, self.source_locale, "prompt", self.prompt
            ),
        }


class DefaultPrompts(RecordModel):
    record_id: ClassVar[str] = "open_notebook:default_prompts"
    transformation_instructions: Optional[str] = Field(
        None, description="Instructions for executing a transformation"
    )
    source_locale: str = DEFAULT_TRANSFORMATION_LOCALE
    translations: dict[str, DefaultPromptTranslation] = Field(default_factory=dict)

    @field_validator("translations", mode="before")
    @classmethod
    def _ensure_prompt_translation_map(cls, value: Any) -> dict[str, Any]:
        return value or {}

    def get_effective_translations(self) -> dict[str, DefaultPromptTranslation]:
        merged = _merge_translation_maps(
            get_default_prompt_translations(),
            self.translations,
        )
        return {
            locale: DefaultPromptTranslation(**fields)
            for locale, fields in merged.items()
        }

    def resolve_transformation_instructions(self, locale: Optional[str]) -> str:
        translations = self.get_effective_translations()
        return _resolve_field(
            translations,
            locale,
            self.source_locale,
            "transformation_instructions",
            self.transformation_instructions or "",
        )
