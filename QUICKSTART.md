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
# 1. 确保安装了 Python 3.12
pyenv install 3.12.0

# 2. 设置项目的 Python 版本
pyenv local 3.12.0

# 3. 创建虚拟环境
cd backend
python -m venv venv

# 4. 激活虚拟环境
source venv/bin/activate  # macOS/Linux

# 5. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 6. 配置环境变量
cd ..
cp .env.example .env
# 编辑 .env 文件添加 OPENAI_API_KEY
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

### 启动服务

**终端1 - 后端：**
```bash
cd backend
source venv/bin/activate
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

## 常见问题

### Q: pyenv install requirements.txt 报错

**错误原因：** `pyenv install` 只用于安装 Python 版本，不能用来安装包。

**正确做法：**
```bash
# 错误 ❌
pyenv install requirements.txt

# 正确 ✅
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Q: command not found: python

**解决方法：**
```bash
# 重新加载 shell 配置
source ~/.zshrc  # 或 ~/.bashrc

# 或者手动设置路径
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
```

### Q: 找不到 venv/bin/activate

**原因：** 虚拟环境未创建

**解决方法：**
```bash
cd backend
python -m venv venv
```

### Q: pip install 缓慢或失败

**使用国内镜像：**
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Q: npm install 失败

**清理并重试：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps
```

## 项目结构

```
ai_comic/
├── backend/              # Python 后端
│   ├── src/             # 源代码
│   ├── venv/            # 虚拟环境（创建后）
│   └── requirements.txt # Python 依赖
├── frontend/            # Vue 3 前端
│   ├── src/            # 源代码
│   ├── node_modules/   # npm 依赖（创建后）
│   └── package.json   # npm 配置
├── .env               # 环境变量（从 .env.example 创建）
└── setup-local.sh     # 自动设置脚本
```

## 开发流程

1. 修改代码
2. 后端自动重载（使用 `--reload` 参数）
3. 前端自动重载（Vite 热更新）
4. 查看日志输出调试

## 下一步

查看 [LOCAL_DEV.md](LOCAL_DEV.md) 获取更详细的开发文档。