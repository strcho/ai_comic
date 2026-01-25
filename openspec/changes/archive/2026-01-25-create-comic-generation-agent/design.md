# 设计文档

## 架构概述

### 系统组件
```
┌───────────────────────────────────────────────────────────────┐
│                        Vue 3 Web UI                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Text Input│ │ Settings │ │ Preview  │ │  History         │ │
│  │ Component│ │ Panel    │ │ Component│ │  Manager         │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘ │
└───────────────────────────────────────────────────────────────┘
                           │ RESTful API
                           ▼
┌───────────────────────────────────────────────────────────────┐
│                     FastAPI Backend Service                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              API Gateway & Controller                     │ │
│  └────────────────────┬─────────────────────────────────────┘ │
│                       │                                        │
│       ┌───────────────┼───────────────┬───────────────┐       │
│       ▼               ▼               ▼               ▼       │
│  ┌─────────┐    ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ Story   │    │ Image    │   │ Comic    │   │ Cache    │   │
│  │Processor│    │Generator │   │Composer  │   │ Manager  │   │
│  └─────────┘    └──────────┘   └──────────┘   └──────────┘   │
│                                          │                    │
│                                          ▼                    │
│                                    ┌──────────┐               │
│                                    │ Image    │               │
│                                    │ Storage  │               │
│                                    └──────────┘               │
└───────────────────────────────────────────────────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  External APIs   │
                  │  (DALL-E, etc.)  │
                  └──────────────────┘
```

### 数据流

#### CLI流程
1. **输入阶段**：用户通过CLI提供文本描述或脚本
2. **处理阶段**：Story Processor解析文本，提取场景信息
3. **生成阶段**：Image Generator为每个场景生成图像
4. **组合阶段**：Comic Compositor将图像组合为多格漫画
5. **输出阶段**：保存为图像文件（PNG/JPG/PDF）

#### Web流程
1. **前端输入**：用户在Web界面输入文本，配置参数
2. **API请求**：前端向后端发送RESTful API请求
3. **任务处理**：后端创建异步任务，返回任务ID
4. **进度轮询**：前端轮询任务进度，实时更新UI
5. **结果返回**：后端生成完成，返回漫画URL或Base64
6. **前端展示**：前端显示生成的漫画，提供下载功能

### 前后端通信

#### API端点设计
- `POST /api/generate` - 创建生成任务
- `GET /api/task/{task_id}` - 查询任务状态
- `GET /api/task/{task_id}/result` - 获取生成结果
- `GET /api/history` - 获取历史记录
- `DELETE /api/history/{id}` - 删除历史记录
- `GET /api/config` - 获取配置信息
- `PUT /api/config` - 更新配置

#### WebSocket支持（可选）
- 对于实时性要求高的场景，可升级为WebSocket推送进度

## 技术选择

### 后端技术栈
- **编程语言**：Python
- **Web框架**：FastAPI（高性能、自动API文档、异步支持）
- **文本处理**：NLTK或spaCy（可选，基础功能可使用原生字符串操作）
- **图像处理**：Pillow (PIL) 用于图像操作和组合
- **API客户端**：HTTPX（异步HTTP客户端）
- **配置管理**：Pydantic或YAML
- **CLI框架**：Click或Typer
- **异步处理**：asyncio（用于并行生成）

### 前端技术栈
- **框架**：Vue 3（Composition API）
- **构建工具**：Vite（快速开发构建）
- **路由**：Vue Router 4
- **状态管理**：Pinia
- **UI组件库**：Element Plus 或 Naive UI
- **HTTP客户端**：Axios
- **本地存储**：IndexedDB（使用Dexie.js）
- **测试**：Vitest（单元测试）+ Playwright（E2E测试）
- **样式**：TailwindCSS 或 CSS Modules

### 图像生成API
**选项1**：OpenAI DALL-E
- 优点：质量稳定，API简单
- 缺点：有费用，生成速度一般

**选项2**：Stability AI
- 优点：开源模型支持，灵活性高
- 缺点：可能需要更多配置

**选项3**：Midjourney（通过Discord API）
- 优点：艺术质量高
- 缺点：API集成复杂

**推荐**：先实现DALL-E集成，预留接口支持其他API

## 关键设计决策

### 1. 场景提取策略
**决策**：使用简单的规则+启发式方法
- 基于句子分割识别场景
- 支持明确的场景标记（如"场景1:"、"Panel 1:"等）
- 默认将长文本分成3-5个场景

**理由**：简单实用，避免过度工程化

### 2. 图像提示词构建
**决策**：自动增强提示词
- 提取关键词（人物、动作、环境）
- 添加漫画风格修饰词（"comic style", "illustration"等）
- 支持用户自定义风格参数

**理由**：提高生成质量和一致性

### 3. 布局算法
**决策**：预设几种常用布局
- 网格布局（2x2, 3x2等）
- 横向长条布局
- 自定义JSON布局配置

**理由**：满足基本需求，避免复杂的布局计算

### 4. 错误处理
**决策**：优雅降级
- API失败时跳过该场景或使用占位图
- 超时重试3次后放弃
- 记录详细的错误日志

**理由**：提高系统的鲁棒性

### 5. 缓存策略
**决策**：基于输入hash的文件缓存
- 使用场景描述hash作为缓存键
- 保存生成参数和图像
- 支持强制重新生成

**理由**：避免重复调用昂贵API，加快调试速度

### 6. 前端状态管理
**决策**：使用Pinia进行全局状态管理
- 管理生成任务状态、历史记录、用户配置
- 模块化store设计（story.ts, generation.ts, config.ts, history.ts）
- 支持持久化存储（pinia-plugin-persistedstate）

**理由**：集中管理应用状态，组件间通信更简单

### 7. 前端路由设计
**决策**：单页面应用，使用Vue Router
- `/` - 主页面（生成漫画）
- `/history` - 历史记录
- `/settings` - 配置页面
- `/preview/:id` - 漫画预览页面

**理由**：清晰的页面结构，用户体验流畅

### 8. API任务队列
**决策**：后端使用异步任务队列
- 使用FastAPI的BackgroundTasks或Celery
- 任务状态持久化到数据库（SQLite或Redis）
- 支持任务取消和重试

**理由**：处理长时间运行的图像生成任务，避免请求超时

## 扩展性考虑

### 插件化设计
- 图像生成器接口可扩展支持多个API
- 布局引擎可添加新布局类型
- 文本处理器可支持新的输入格式
- 前端组件可复用和扩展

### 配置驱动
- 所有参数（API密钥、生成参数、布局等）通过配置文件
- 支持环境变量覆盖
- 多环境配置（dev, test, prod）
- 前端配置可通过API动态更新

### 前端组件化
- 每个功能模块独立封装成组件
- 使用props和events进行组件通信
- 支持组件slot灵活定制

## 性能考虑

### 后端优化
- 使用asyncio并行生成多个场景的图像
- 限制并发数避免API限流
- 图像生成后及时保存，避免内存堆积
- 支持流式处理大量场景
- 使用Redis缓存热点数据（可选）

### 前端优化
- 使用Vite的HMR加快开发速度
- 组件懒加载和代码分割
- 图片懒加载和缩略图预览
- 使用Web Worker处理密集计算（可选）
- 虚拟滚动处理长列表（历史记录）

## 安全考虑

### API密钥管理
- 使用环境变量存储敏感信息
- 配置文件不包含密钥
- 提供加密存储选项（前端使用localStorage + 加密）
- 后端密钥仅存储在服务器端

### 内容过滤
- 检测和拒绝敏感内容
- 支持自定义过滤规则
- 生成前验证提示词

### 前端安全
- API密钥不在前端暴露（仅通过后端调用）
- CSRF防护
- XSS防护（Vue自动转义）
- HTTPS强制使用（生产环境）
- 内容安全策略（CSP）

## 测试策略

### 后端测试
- **单元测试**：文本处理逻辑、提示词构建、布局计算
- **集成测试**：API调用（使用mock）、完整流程测试、错误场景测试
- **端到端测试**：真实API调用（限制频率）、生成质量验证（人工审核）

### 前端测试
- **单元测试**：组件逻辑、状态管理（使用Vitest）
- **集成测试**：组件交互、API调用（使用MSW mock）
- **E2E测试**：完整用户流程（使用Playwright）
- **性能测试**：首屏加载、交互响应时间

## 已知限制

1. **字符一致性**：不同场景的同一角色可能不一致
2. **风格统一**：API返回的图像风格可能有差异
3. **复杂场景**：多角色、复杂动作描述可能生成质量下降
4. **成本控制**：需要监控API调用次数和费用

## 未来改进方向

1. 引入角色embedding实现一致性
2. 支持自定义模型微调
3. 添加对话气泡和文本排版
4. 实现交互式编辑界面
5. 支持动态分镜和动画

## 容器化部署架构

### 容器编排设计
```
┌──────────────────────────────────────────────────────────┐
│                    Docker Compose                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │ Frontend        │  │ Backend         │  │ Optional   │ │
│  │ (Nginx + Vue)   │  │ (FastAPI)       │  │ Database   │ │
│  │ Port: 80/443    │  │ Port: 8000      │  │ (SQLite/   │ │
│  └─────────────────┘  └─────────────────┘  │  Redis)    │ │
│         │                    │              └────────────┘ │
│         └────────────────────┼─────────────────┐          │
│                              ▼                 ▼          │
│                    ┌──────────────────────────────────┐   │
│                    │         Shared Volumes           │   │
│                    │  /app/cache /app/output /logs   │   │
│                    └──────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### Docker文件组织
```
project/
├── Dockerfile.backend          # 后端多阶段构建
├── Dockerfile.frontend         # 前端多阶段构建
├── docker-compose.yml          # 生产环境编排
├── docker-compose.dev.yml      # 开发环境编排
├── nginx.conf                  # Nginx配置
├── .env.example                # 环境变量模板
├── start.sh                    # 快速启动脚本
└── deploy/
    └── docker-init/            # 初始化脚本
```

### 容器镜像构建策略

#### 后端Dockerfile（多阶段）
```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 前端Dockerfile（多阶段）
```dockerfile
# Stage 1: Build
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 环境变量管理

#### .env.example
```env
# Backend Configuration
BACKEND_PORT=8000
LOG_LEVEL=INFO

# API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=dall-e-3

# Image Generation
IMAGE_SIZE=1024
MAX_CONCURRENT=3

# Volume Paths
CACHE_DIR=/app/cache
OUTPUT_DIR=/app/output

# Frontend Configuration
FRONTEND_PORT=80
```

### Docker Compose配置

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./cache:/app/cache
      - ./output:/app/output
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "${FRONTEND_PORT:-80}:80"
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  cache:
  output:
  logs:
```

### 开发环境配置

#### docker-compose.dev.yml特点
- 前端支持热重载（HMR）
- 后端支持代码自动重载（uvicorn --reload）
- 挂载源码目录到容器
- 包含开发调试工具
- 使用dev依赖

### 生产环境配置

#### 生产环境额外配置
- Nginx反向代理
- SSL/TLS证书支持
- 资源限制（CPU、内存）
- 日志轮转配置
- 静态文件缓存优化
- Gzip压缩
- 安全头配置

### 部署脚本

#### start.sh功能
```bash
#!/bin/bash
# 检查Docker和Docker Compose
# 复制.env.example到.env（如不存在）
# 提示用户配置环境变量
# 构建镜像
# 启动容器
# 显示服务状态和访问URL
```
