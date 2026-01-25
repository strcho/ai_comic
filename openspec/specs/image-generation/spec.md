# image-generation Specification

## Purpose
TBD - created by archiving change create-comic-generation-agent. Update Purpose after archive.
## Requirements
### Requirement: 集成图像生成API

系统MUST能够调用外部图像生成API（如OpenAI DALL-E）生成图像。

#### Scenario: 调用DALL-E API生成单张图像

**Given** 系统配置了有效的OpenAI API密钥

**And** 场景提示词："A warrior standing on a mountain peak, comic style"

**When** 系统发起图像生成请求

**Then** 系统从API接收生成的图像数据并保存为PNG文件

#### Scenario: 处理API认证错误

**Given** 系统配置了无效的API密钥

**When** 系统尝试调用API

**Then** 系统捕获认证错误并提供清晰的错误消息
- 示例："API认证失败：请检查API密钥配置"

#### Scenario: 处理API限流

**Given** API返回速率限制错误

**When** 系统检测到限流

**Then** 系统等待适当时间后自动重试（最多3次）

### Requirement: 异步并行生成多个图像

系统SHALL能够并行生成多个场景的图像以提高效率。

#### Scenario: 并行生成3张图像

**Given** 有3个场景需要生成图像

**When** 系统发起并行请求

**Then** 系统同时处理3个API调用，而不是顺序执行

**And** 总耗时接近单个请求的时间（而非3倍）

#### Scenario: 控制并发数量

**Given** 有10个场景需要生成

**And** 系统配置最大并发数为3

**When** 系统发起并行请求

**Then** 系统最多同时处理3个请求，其他请求等待

### Requirement: 支持多个图像生成服务

系统SHALL提供接口支持接入不同的图像生成服务。

#### Scenario: 切换到Stability AI API

**Given** 系统当前使用DALL-E API

**When** 用户配置切换到Stability AI

**Then** 系统使用Stability AI的API客户端和参数格式

**And** 生成流程保持一致

#### Scenario: 添加自定义图像生成器

**Given** 开发者想要添加新的图像生成服务

**When** 实现ImageGenerator接口

**Then** 新服务可以无缝集成到系统中

### Requirement: 图像生成参数配置

系统MUST允许用户配置图像生成的各种参数。

#### Scenario: 配置图像尺寸

**Given** 用户配置图像尺寸为1024x1024

**When** 系统生成图像

**Then** API请求使用指定的尺寸参数

#### Scenario: 配置图像质量

**Given** 用户配置图像质量为"high"

**When** 系统生成图像

**Then** API请求包含高质量参数

#### Scenario: 配置生成数量

**Given** 某个场景用户配置生成3个候选图像

**When** 系统生成该场景的图像

**Then** 系统返回3张图像供用户选择

### Requirement: 错误处理和重试机制

系统MUST能够处理各种错误情况并实现自动重试。

#### Scenario: 网络超时重试

**Given** API请求超时

**When** 系统检测到超时

**Then** 系统自动重试（最多3次），每次间隔递增（1s, 2s, 4s）

#### Scenario: 服务器错误重试

**Given** API返回5xx错误

**When** 系统检测到服务器错误

**Then** 系统进行指数退避重试

#### Scenario: 客户端错误不重试

**Given** API返回4xx错误（如400 Bad Request）

**When** 系统检测到客户端错误

**Then** 系统不重试，直接返回错误消息

### Requirement: 图像缓存机制

系统SHALL能够缓存已生成的图像以避免重复调用API。

#### Scenario: 基于输入hash缓存

**Given** 系统之前已为提示词P生成过图像

**When** 用户再次请求生成提示词P的图像

**Then** 系统直接从缓存返回图像，不调用API

#### Scenario: 缓存命中验证

**Given** 系统有缓存文件

**When** 用户使用--force参数强制重新生成

**Then** 系统忽略缓存，重新调用API

#### Scenario: 缓存过期策略

**Given** 系统配置缓存过期时间为7天

**And** 某个缓存文件创建于10天前

**When** 用户请求该提示词的图像

**Then** 系统识别缓存过期，重新调用API

### Requirement: 进度跟踪和状态报告

系统SHALL能够实时报告图像生成的进度。

#### Scenario: 显示生成进度

**Given** 系统正在生成5张图像

**When** 每完成一张图像

**Then** 系统显示进度：例如"[2/5] 生成场景2..."

#### Scenario: 显示预计剩余时间

**Given** 系统已完成3张图像，总共5张

**And** 前3张平均耗时15秒

**When** 系统更新进度

**Then** 系统显示预计剩余时间（例如："预计剩余：30秒"）

### Requirement: 内容安全过滤

系统MUST能够检测和过滤不当内容。

#### Scenario: 检测敏感内容

**Given** 用户提示词包含敏感词（如暴力、色情等）

**When** 系统准备生成图像

**Then** 系统拒绝生成并提示："提示词包含不当内容，请修改后重试"

#### Scenario: 自定义过滤规则

**Given** 管理员配置了自定义敏感词列表

**When** 用户提交提示词

**Then** 系统检查提示词是否包含自定义的敏感词

