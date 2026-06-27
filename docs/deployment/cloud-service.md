# Cloud-Service Deployment (Managed Model Mode)

This guide explains how to deploy notebook-typetype as a **managed cloud service**:
the operator configures all AI models in one file, and end users never have to
touch API keys, pick models, or open a settings page.

> This is Phase 1 of the cloud-service roadmap. Multi-user authentication and
> per-tenant isolation arrive in Phase 2.

---

## How managed mode works

```
┌──────────────────────────────────────────────────────────┐
│  config/models.yaml  (operator-managed, git-ignored)     │
│  defines tiers, models, and references ${ENV} for keys   │
└──────────────────────────────────────────────────────────┘
                           │ loaded at startup
                           ▼
┌──────────────────────────────────────────────────────────┐
│  ModelConfigProvider  →  ModelManager  →  Esperanto      │
│  All chat / embedding / TTS / STT requests resolve here. │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
   End users get a clean UI — no Models page, no warnings.
```

When `config/models.yaml` is **absent**, the app falls back to the original
per-user database configuration, so existing self-hosted deployments keep
working unchanged.

---

## 1. Configure environment variables

Put your real API keys in `.env` (never in the yaml):

```bash
# .env
DASHSCOPE_API_KEY=sk-...        # Alibaba Qwen
ZHIPU_API_KEY=...               # Zhipu GLM
OPENAI_API_KEY=sk-...           # OpenAI
GOOGLE_API_KEY=...              # Google Gemini
MINIMAX_API_KEY=...             # MiniMax
```

## 2. Create config/models.yaml

Copy the template and edit it:

```bash
cp config/models.yaml.example config/models.yaml
```

Define one or more tiers. Each tier maps a *purpose* (language / embedding /
text_to_speech / speech_to_text / large_context) to a provider + model + key:

```yaml
default_tier: standard

tiers:
  free:
    language:
      provider: dashscope
      model: qwen-plus
      api_key: ${DASHSCOPE_API_KEY}
    embedding:
      provider: dashscope
      model: text-embedding-v3
      api_key: ${DASHSCOPE_API_KEY}

  standard:
    language:
      provider: openai_compatible
      model: glm-4-plus
      api_key: ${ZHIPU_API_KEY}
      base_url: https://open.bigmodel.cn/api/paas/v4
    embedding:
      provider: openai_compatible
      model: embedding-3
      api_key: ${ZHIPU_API_KEY}
      base_url: https://open.bigmodel.cn/api/paas/v4
```

Rules:
- `${ENV_VAR}` resolves against the process environment at load time.
- `chat`, `tools`, `transformation` all map onto the `language` purpose.
- A missing purpose in a tier falls back to the `default_tier`.
- Provider names must match Esperanto's AIFactory (`openai`, `anthropic`,
  `google`, `dashscope`, `openai_compatible`, `ollama`, `minimax`, ...).

## 3. Start the app

```bash
uv run --env-file .env python run_api.py
```

On startup the log will confirm managed mode:

```
Managed model mode enabled: tiers=['free', 'standard'], default='standard'.
Users will not see model configuration UI.
```

## 4. Verify

```bash
# Is managed mode on?
curl http://localhost:5055/api/models/managed
# → {"enabled": true, "default_tier": "standard", "tiers": ["free", "standard"]}

# Any tier missing a key?
curl http://localhost:5055/api/models/health
```

Open the frontend — the sidebar no longer shows a "Models" entry, and the
setup banner is suppressed. Users can upload sources and chat immediately.

---

## Hot-reloading

After editing `config/models.yaml`, reload without a restart:

```bash
curl -X POST http://localhost:5055/api/models/reload
```

## Operator reference

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/models/managed` | GET | Check if managed mode is on, list tiers |
| `/api/models/reload` | POST | Hot-reload `config/models.yaml` |
| `/api/models/health` | GET | Per-tier/per-purpose config status (no secrets) |

---

## Troubleshooting

**"Managed model mode disabled"** — `config/models.yaml` is missing or failed
to parse. Check the startup log for the exact error.

**`has_api_key: false` in /health** — the `${ENV_VAR}` referenced in the yaml
is not set in the environment. Add it to `.env` and restart (or reload after
fixing the env).

**Falls back to DB models even in managed mode** — the requested purpose has
no entry in the requested tier *and* no entry in the default tier. Add the
purpose to the default tier.
