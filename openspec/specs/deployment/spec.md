# deployment Specification

## Purpose
TBD - created by archiving change create-comic-generation-agent. Update Purpose after archive.
## Requirements
### Requirement: 支持Docker容器化部署

系统MUST支持使用Docker进行容器化部署。

#### Scenario: 构建后端Docker镜像

**Given** 项目包含Dockerfile.backend

**When** 运行命令 `docker build -f Dockerfile.backend -t comic-backend .`

**Then** 系统成功构建包含Python运行时和依赖的后端镜像

#### Scenario: 构建前端Docker镜像

**Given** 项目包含Dockerfile.frontend

**When** 运行命令 `docker build -f Dockerfile.frontend -t comic-frontend .`

**Then** 系统成功构建包含Nginx和前端静态文件的镜像

#### Scenario: 验证镜像大小合理

**Given** 后端和前端镜像构建完成

**When** 检查镜像大小

**Then** 后端镜像不超过1GB，前端镜像不超过200MB

### Requirement: 使用Docker Compose编排服务

系统SHALL提供Docker Compose配置文件用于一键部署。

#### Scenario: 一键启动所有服务

**Given** 项目包含docker-compose.yml

**When** 运行命令 `docker-compose up -d`

**Then** 系统启动后端服务、前端服务和数据库（如需要）

**And** 所有服务正常运行

#### Scenario: 服务健康检查

**Given** Docker Compose启动所有服务

**When** 系统启动完成

**Then** 后端API健康检查端点返回200状态码
**And** 前端页面可正常访问

#### Scenario: 一键停止所有服务

**Given** Docker Compose正在运行

**When** 运行命令 `docker-compose down`

**Then** 系统停止所有容器并删除网络

### Requirement: 环境变量配置管理

系统MUST支持通过环境变量配置应用参数。

#### Scenario: 使用.env文件配置

**Given** 项目包含.env.example模板文件

**When** 用户复制并修改.env文件

**Then** Docker Compose读取.env文件中的配置并注入到容器中

#### Scenario: 配置API密钥

**Given** 用户在.env文件中设置API_KEY

**When** 容器启动

**Then** 后端服务可以访问到正确的API密钥

#### Scenario: 配置服务端口

**Given** 用户修改.env文件中的端口映射

**When** Docker Compose启动

**Then** 服务监听指定的端口

### Requirement: 数据持久化

系统SHALL支持容器重启后数据不丢失。

#### Scenario: 挂载缓存目录

**Given** 用户配置了卷挂载

**When** 容器生成图像并缓存

**Then** 缓存数据持久化到宿主机目录
**And** 容器重启后缓存仍然存在

#### Scenario: 挂载输出目录

**Given** 用户配置了输出目录挂载

**When** 用户生成漫画并下载

**Then** 生成的漫画保存在宿主机目录

#### Scenario: 数据库持久化（可选）

**Given** 系统使用数据库存储历史记录

**When** 容器重启

**Then** 历史记录数据仍然存在

### Requirement: 多阶段构建优化

系统SHALL使用多阶段构建优化镜像大小。

#### Scenario: 后端多阶段构建

**Given** 后端使用多阶段构建

**When** 构建Docker镜像

**Then** 最终镜像仅包含运行时依赖
**And** 构建工具和源码被排除

#### Scenario: 前端多阶段构建

**Given** 前端使用多阶段构建（构建阶段 + Nginx阶段）

**When** 构建Docker镜像

**Then** 最终镜像仅包含Nginx和静态文件
**And** Node.js和构建工具被排除

### Requirement: 健康检查和重启策略

系统SHALL配置容器健康检查和自动重启策略。

#### Scenario: 后端健康检查

**Given** 后端容器配置了健康检查

**When** 容器运行

**Then** Docker定期检查/health端点
**And** 服务不健康时标记容器为unhealthy

#### Scenario: 自动重启

**Given** 容器配置了restart: always策略

**When** 容器意外退出

**Then** Docker自动重启容器

#### Scenario: 前端健康检查

**Given** 前端Nginx配置了健康检查

**When** 容器运行

**Then** Docker检查Nginx是否响应

### Requirement: 日志管理

系统SHALL支持容器日志管理和查看。

#### Scenario: 查看实时日志

**Given** 容器正在运行

**When** 运行命令 `docker-compose logs -f`

**Then** 显示所有服务的实时日志输出

#### Scenario: 配置日志级别

**Given** 用户在.env中设置LOG_LEVEL=DEBUG

**When** 容器启动

**Then** 应用输出DEBUG级别的日志

#### Scenario: 日志轮转（可选）

**Given** 长期运行的应用

**When** 日志文件增长

**Then** 日志自动轮转避免占用过多磁盘

### Requirement: 生产环境部署

系统MUST支持生产环境部署配置。

#### Scenario: 使用Nginx反向代理

**Given** 生产环境部署

**When** 配置Nginx反向代理

**Then** Nginx处理SSL终止和静态文件服务

#### Scenario: SSL/HTTPS配置

**Given** 用户配置了SSL证书

**When** Nginx启动

**Then** 应用使用HTTPS协议

#### Scenario: 资源限制

**Given** 用户配置资源限制（CPU、内存）

**When** Docker Compose启动

**Then** 容器资源使用被限制在配置范围内

### Requirement: 开发环境支持

系统SHALL提供开发环境的容器化配置。

#### Scenario: 热重载开发

**Given** 开发者使用docker-compose.dev.yml

**When** 修改代码

**Then** 容器自动重新加载代码（后端）或HMR（前端）

#### Scenario: 开发工具集成

**Given** 开发环境容器

**When** 容器启动

**Then** 包含调试工具和开发依赖

#### Scenario: 开发环境隔离

**Given** 开发者使用开发环境配置

**When** 启动开发容器

**Then** 不影响生产环境数据

### Requirement: 快速开始指南

系统MUST提供Docker快速开始文档。

#### Scenario: 快速启动脚本

**Given** 项目包含start.sh脚本

**When** 用户运行 `./start.sh`

**Then** 系统自动执行构建和启动命令

#### Scenario: 文档说明

**Given** 项目README包含Docker部署说明

**When** 开发者阅读文档

**Then** 文档清晰说明：
  - 前置要求（Docker, Docker Compose）
  - 环境配置步骤
  - 启动和停止命令
  - 常见问题解决

