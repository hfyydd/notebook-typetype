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

- 🇨🇳 中文场景全链路优化（切块 / Embedding / Prompt）
- 🎙️ 中文双人播客生成（CosyVoice / MeloTTS）
- 🔐 私有云部署支持（多用户 / 鉴权）
- 📚 国产模型深度集成（GLM / Qwen / DeepSeek / MiniMax）

---

## 🚀 本地开发

### 前置依赖

- Python 3.11+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/)（Python 包管理）
- Docker（用于 SurrealDB）

### 启动

```bash
# 1. 启动数据库
docker compose up -d surrealdb

# 2. 安装后端依赖
uv sync

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 OPEN_NOTEBOOK_ENCRYPTION_KEY（openssl rand -hex 32 生成）

# 4. 启动后端服务（三个终端）
uv run --env-file .env python run_api.py                              # API 服务
uv run --env-file .env surreal-commands-worker --import-modules commands  # 异步任务
cd frontend && npm install && npm run dev                             # 前端
```

访问 http://localhost:3000

### 端口

| 服务 | 端口 |
|------|------|
| 前端 (Next.js) | 3000 |
| API (FastAPI) | 5055 |
| SurrealDB | 8000 |

### ⚠️ 注意：Clash/代理用户

如果机器装了 Clash/SOCKS 代理，连接本地 SurrealDB 会报 `python-socks is required`。解决办法：

```bash
# 方案 1：安装 python-socks
uv add "python-socks[asyncio]"

# 方案 2：启动时排除 localhost 走代理
NO_PROXY="localhost,127.0.0.1,::1" uv run --env-file .env python run_api.py
```

---

## 🧱 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python · FastAPI · LangChain · LangGraph |
| 前端 | Next.js 16 · React 19 · TypeScript |
| 数据库 | SurrealDB（业务数据 + 向量索引） |
| 模型抽象 | Esperanto（支持 18+ 提供商，含 Ollama / DeepSeek / Qwen / MiniMax） |

---

## 📄 License

MIT License — 保留原作者 Luis Novo 的版权声明，详见 [LICENSE](LICENSE)
