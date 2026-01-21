# 快速入门指南

## 方法1：使用自动化脚本（推荐）

```bash
# 1. 一键设置环境
./setup-local.sh

# 2. 配置 OpenAI API Key
# 编辑 .env 文件，添加你的 OPENAI_API_KEY

# 3. 启动开发服务器
./start-local.sh
```

## 方法2：手动步骤（如果脚本有问题）

### 后端设置

```bash
# 1. 确保 Python 3.12 已安装
python3 --version

# 2. 进入后端目录
cd backend

# 3. 使用 pipenv 安装依赖
pipenv install --dev

# 这会自动创建虚拟环境并安装所有依赖
```

### 前端设置

```bash
# 1. 安装依赖
cd frontend
npm install

# 2. 创建前端环境变量
echo "VITE_API_URL=http://localhost:8000" > .env

cd ..
```

### 配置环境变量

```bash
# 创建后端环境变量文件
cp .env.example .env

# 编辑 .env 文件添加 OPENAI_API_KEY
# OPENAI_API_KEY=your_actual_api_key_here
```

### 启动服务

**终端1 - 后端：**
```bash
cd backend

# 方式1：使用 pipenv run（推荐）
pipenv run dev

# 方式2：激活 pipenv shell 后运行
pipenv shell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**终端2 - 前端：**
```bash
cd frontend
npm run dev
```

## 验证安装

- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 前端界面: http://localhost:5173

## 常用 pipenv 命令

```bash
cd backend

# 激活虚拟环境
pipenv shell

# 运行开发服务器
pipenv run dev

# 运行测试
pipenv run test

# 运行 CLI 命令
pipenv run cli generate "你的故事..." -o output.png

# 查看依赖
pipenv graph

# 添加新依赖
pipenv install <package>        # 生产依赖
pipenv install <package> --dev  # 开发依赖

# 更新依赖
pipenv update

# 移除虚拟环境
pipenv --rm

# 重新安装所有依赖
pipenv install --dev --force
```

## 常见问题

### Q: pipenv install 缓慢

**使用国内镜像：**

创建或编辑 `~/.pip/pip.conf`:
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

或使用 pipenv 自带的 --verbose 查看详细日志：
```bash
pipenv install --dev --verbose
```

### Q: 找不到 pipenv 命令

**解决方法：**
```bash
# 安装 pipenv
pip install pipenv

# 重新加载 shell
source ~/.zshrc  # 或 ~/.bashrc
```

### Q: 虚拟环境激活失败

**解决方法：**
```bash
cd backend

# 移除并重建虚拟环境
pipenv --rm
pipenv install --dev
```

### Q: pipenv run dev 报错

**检查 Pipfile 中的 scripts：**
```bash
pipenv run --list
```

手动运行命令：
```bash
pipenv shell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Q: npm install 失败

**清理并重试：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps
```

### Q: .env 文件配置不生效

**检查：**
1. 确保在项目根目录或 backend 目录下有 `.env` 文件
2. 不要提交 `.env` 文件到 git（已添加到 .gitignore）
3. 重启开发服务器使环境变量生效

## 项目结构

```
ai_comic/
├── backend/              # Python 后端
│   ├── src/             # 源代码
│   ├── .venv/           # pipenv 虚拟环境（创建后）
│   ├── Pipfile          # pipenv 依赖配置
│   ├── Pipfile.lock     # 锁定的依赖版本
│   └── requirements.txt # 用于 Docker/向后兼容
├── frontend/            # Vue 3 前端
│   ├── src/            # 源代码
│   ├── node_modules/   # npm 依赖（创建后）
│   └── package.json   # npm 配置
├── .env               # 环境变量（从 .env.example 创建）
├── .env.example       # 环境变量模板
├── setup-local.sh     # 自动设置脚本
└── start-local.sh     # 启动开发服务器脚本
```

## 开发流程

1. 修改代码
2. 后端自动重载（使用 `--reload` 参数）
3. 前端自动重载（Vite 热更新）
4. 查看日志输出调试

## pipenv vs venv 对比

| 特性 | pipenv | venv |
|------|---------|------|
| 依赖管理 | ✅ 自动 | ❌ 手动 |
| 锁定文件 | ✅ Pipfile.lock | ❌ 无 |
| 开发/生产分离 | ✅ 原生支持 | ❌ 手动管理 |
| 脚本支持 | ✅ 内置 | ❌ 无 |
| 安装简单 | ✅ 一条命令 | ❌ 多步骤 |

## 下一步

查看 [LOCAL_DEV.md](LOCAL_DEV.md) 获取更详细的 pipenv 开发文档。

## 相关链接

- [pipenv 官方文档](https://pipenv.pypa.io/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Vue 3 文档](https://vuejs.org/)
- [OpenAI API 文档](https://platform.openai.com/docs)