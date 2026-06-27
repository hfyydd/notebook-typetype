# notebook-typetype

> 基于 [Open Notebook](https://github.com/lfnovo/open-notebook) 二次开发，面向中文场景的 NotebookLM 本地化方案。

<p align="center">
  <a href="https://github.com/lfnovo/open-notebook">
    <img src="docs/assets/hero.svg" alt="Logo" width="120">
  </a>
</p>

## 📌 项目说明

本项目基于 [lfnovo/open-notebook](https://github.com/lfnovo/open-notebook)（MIT License）的架构进行中文场景优化与功能扩展。

### 致谢

- **原项目**：[Open Notebook](https://github.com/lfnovo/open-notebook) by [@lfnovo](https://github.com/lfnovo)
- **协议**：MIT License — 感谢原作者开源贡献

### 二开方向

- 🔧 **云服务托管模式**：运维一份配置文件托管所有模型，用户开箱即用，无需配置任何 API Key
- 🇨🇳 中文场景全链路优化（切块 / Embedding / Prompt）
- 🎙️ 中文双人播客生成（CosyVoice / MeloTTS）
- 🔐 私有云部署支持（多用户 / 鉴权）
- 📚 国产模型深度集成（MiniMax / GLM / Qwen / DeepSeek / 硅基流动）

---

## 🚀 快速开始

### 前置依赖

| 依赖 | 版本 | 安装方式 |
|------|------|----------|
| Python | 3.11+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| [uv](https://docs.astral.sh/uv/) | 最新 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker | 最新 | [docker.com](https://docker.com)（跑 SurrealDB 用） |

### 第 1 步：克隆并安装

```bash
git clone https://github.com/hfyydd/notebook-typetype.git
cd notebook-typetype

# 后端依赖
uv sync

# 前端依赖
cd frontend && npm install && cd ..
```

### 第 2 步：配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，**至少**填这两项：

```bash
# 1. 加密密钥（用于加密数据库中的敏感信息，必须设置）
#    终端运行下面命令生成一个:
#    openssl rand -hex 32
OPEN_NOTEBOOK_ENCRYPTION_KEY=<把上面命令的输出粘到这里>

# 2. 数据库（保持默认即可，源码运行模式用 localhost）
SURREAL_URL=ws://localhost:8000/rpc
SURREAL_USER=root
SURREAL_PASSWORD=root
SURREAL_NAMESPACE=open_notebook
SURREAL_DATABASE=open_notebook
```

### 第 3 步：配置 AI 模型（云服务托管模式）

本项目支持**云服务托管模式**：用一份 YAML 配置文件管理所有 AI 模型，用户无需在前端配置任何 API Key。

```bash
cp config/models.yaml.example config/models.yaml
```

编辑 `config/models.yaml`，配置你需要的模型档位。把 API Key 填到 `.env`（**不要直接写在 yaml 里**），yaml 通过 `${ENV_VAR}` 引用：

```yaml
# .env 文件中:
MINIMAX_API_KEY=sk-xxx          # MiniMax
SILICONFLOW_API_KEY=sk-xxx      # 硅基流动（免费送额度）

# config/models.yaml:
default_tier: standard
tiers:
  standard:
    language:                    # 对话/问答用 MiniMax
      provider: openai_compatible
      model: MiniMax-M3
      api_key: ${MINIMAX_API_KEY}
      base_url: https://api.minimaxi.com/v1
    embedding:                   # 向量化用硅基流动 bge-m3
      provider: openai_compatible
      model: BAAI/bge-m3
      api_key: ${SILICONFLOW_API_KEY}
      base_url: https://api.siliconflow.cn/v1
```

> 📖 完整配置说明见 [docs/deployment/cloud-service.md](docs/deployment/cloud-service.md)

**怎么拿 API Key：**

| 提供商 | 用途 | 获取方式 |
|--------|------|----------|
| [硅基流动 SiliconFlow](https://cloud.siliconflow.cn) | embedding（bge-m3，**新用户送 14 元**） | 注册 → 控制台 → API 密钥 → 新建 |
| [MiniMax](https://platform.minimaxi.com/) | 对话（MiniMax-M3） | 注册 → API Keys |
| [智谱 GLM](https://open.bigmodel.cn/) | 对话/embedding | 注册 → API Keys |
| [OpenAI](https://platform.openai.com/) | 全功能 | 注册 → API Keys |

> 💡 chat 和 embedding **可以分别用不同提供商**——这正是多档位 YAML 架构的优势。例如对话用 MiniMax、向量化用硅基流动。

> ⚠️ **没有 `config/models.yaml` 也能跑**——会自动回退到原版的"用户在前端自己配 Key"模式（数据库存储）。托管模式是可选增强。

### 第 4 步：启动服务

```bash
# 终端 1：启动数据库
docker compose up -d surrealdb

# 终端 2：启动 API
NO_PROXY="localhost,127.0.0.1,::1" uv run --env-file .env python run_api.py

# 终端 3：启动后台任务处理（处理文档向量化等异步任务，必须启动）
NO_PROXY="localhost,127.0.0.1,::1" uv run --env-file .env surreal-commands-worker --import-modules commands

# 终端 4：启动前端
cd frontend && npm run dev
```

看到 API 日志出现下面这行，说明托管模式生效：

```
✅ Managed model mode enabled: tiers=['standard'], default='standard'.
   Users will not see model configuration UI.
```

### 第 5 步：访问

打开 http://localhost:3000 即可使用。

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| API 文档 | http://localhost:5055/docs |
| 数据库 | localhost:8000 |

---

## 📋 端口一览

| 服务 | 端口 |
|------|------|
| 前端 (Next.js) | 3000 |
| API (FastAPI) | 5055 |
| SurrealDB | 8000 |

---

## ⚠️ 常见问题

### Clash/代理用户：连接 SurrealDB 报错 `python-socks is required`

本地 SurrealDB 走代理会失败。两种解法：

```bash
# 方案 1（推荐）：启动时排除 localhost 走代理
NO_PROXY="localhost,127.0.0.1,::1" uv run --env-file .env python run_api.py

# 方案 2：安装 python-socks
uv add "python-socks[asyncio]"
```

### 验证托管模式是否生效

```bash
# 查看托管模式状态
curl http://localhost:5055/api/models/managed

# 检查每个档位的配置完整性（不泄露 Key）
curl http://localhost:5055/api/models/health

# 修改 yaml 后热重载（无需重启）
curl -X POST http://localhost:5055/api/models/reload
```

---

## 🔒 安全说明：API Key 不会上传到 GitHub

本仓库已配置好 `.gitignore`，以下文件**永远不会**被提交：

| 文件 | 内容 | git 状态 |
|------|------|----------|
| `.env` | 加密密钥、所有 API Key | ❌ 已忽略 |
| `config/models.yaml` | 含 `${ENV_VAR}` 引用的模型配置 | ❌ 已忽略 |

提交到 GitHub 的只有：
- `.env.example`（模板，无真实 Key）
- `config/models.yaml.example`（模板，只有 `${ENV_VAR}` 占位符）

**自行检查命令**：

```bash
# 确认 .env 不会上传
git check-ignore .env

# 确认没有 Key 泄露到仓库
git ls-files | xargs grep -l "sk-" 2>/dev/null
```

---

## 🧱 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python · FastAPI · LangChain · LangGraph |
| 前端 | Next.js 16 · React 19 · TypeScript |
| 数据库 | SurrealDB（业务数据 + 向量索引） |
| 模型抽象 | Esperanto（支持 18+ 提供商，含 Ollama / DeepSeek / Qwen / MiniMax） |
| 托管配置 | YAML 多档位（MiniMax / GLM / 硅基流动 / OpenAI 等） |

---

## 📄 License

MIT License — 保留原作者 Luis Novo 的版权声明，详见 [LICENSE](LICENSE)
