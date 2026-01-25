# web-ui Specification

## Purpose
TBD - created by archiving change create-comic-generation-agent. Update Purpose after archive.
## Requirements
### Requirement: 提供Vue 3单页应用

系统MUST提供基于Vue 3的单页应用作为用户界面。

#### Scenario: 应用启动和路由

**Given** 用户访问Web应用的根URL

**When** 应用加载

**Then** 系统显示主页面，包含文本输入区域和生成按钮

#### Scenario: 响应式布局

**Given** 用户在不同设备上访问应用（桌面、平板、手机）

**When** 应用渲染

**Then** 界面自动适配不同屏幕尺寸，保持可用性

### Requirement: 文本输入和故事编辑

系统SHALL提供文本输入界面用于编辑故事描述。

#### Scenario: 多行文本输入

**Given** 用户在文本输入区域输入故事

**When** 用户输入多行文本

**Then** 系统支持多行输入，自动扩展输入框高度

#### Scenario: 实时场景预览

**Given** 用户输入文本："场景1：男孩在公园奔跑。场景2：他遇到了女孩。"

**When** 系统实时解析文本

**Then** 界面显示2个场景卡片，每个卡片包含对应描述

#### Scenario: 支持文件导入

**Given** 用户点击"导入文件"按钮

**And** 用户选择一个.txt文件

**When** 文件上传

**Then** 系统读取文件内容并填充到输入区域

### Requirement: 生成参数配置界面

系统MUST提供图形化界面配置生成参数。

#### Scenario: 图像尺寸配置

**Given** 用户打开"生成设置"面板

**When** 用户选择图像尺寸为1024x1024

**Then** 系统更新配置参数

#### Scenario: 布局类型选择

**Given** 用户配置面板布局

**When** 用户选择"2x2网格"布局

**Then** 系统显示布局预览图，并更新配置

#### Scenario: 风格参数配置

**Given** 用户配置图像风格

**When** 用户选择"manga style"和"高质量"

**Then** 系统将这些参数传递给后端生成服务

#### Scenario: API密钥配置

**Given** 首次使用应用

**When** 用户在设置中输入OpenAI API密钥

**Then** 系统加密保存密钥到本地存储

### Requirement: 实时生成进度显示

系统SHALL实时显示漫画生成进度。

#### Scenario: 进度条显示

**Given** 用户点击"生成漫画"按钮

**When** 系统正在生成4张图像

**Then** 界面显示进度条，当前进度为2/4

#### Scenario: 单场景生成状态

**Given** 系统正在生成第3张图像

**When** 第3张图像完成

**Then** 界面更新状态为"场景3已完成"，并显示缩略图

#### Scenario: 生成完成通知

**Given** 所有图像生成完成

**When** 漫画组装完成

**Then** 系统显示"生成完成"提示，并展示完整漫画

### Requirement: 漫画预览和交互

系统MUST提供漫画预览和基本交互功能。

#### Scenario: 漫画全屏预览

**Given** 漫画生成完成

**When** 用户点击漫画图像

**Then** 系统打开全屏预览模式

#### Scenario: 缩放和平移

**Given** 用户在全屏预览模式

**When** 用户使用鼠标滚轮或捏合手势

**Then** 系统支持缩放和平移操作

#### Scenario: 面板独立查看

**Given** 漫画包含4个面板

**When** 用户点击第2个面板

**Then** 系统放大显示第2个面板，显示对应场景描述

### Requirement: 结果下载和导出

系统SHALL支持下载和导出生成的漫画。

#### Scenario: 下载PNG格式

**Given** 漫画生成完成

**When** 用户点击"下载PNG"按钮

**Then** 浏览器下载漫画的PNG文件

#### Scenario: 下载PDF格式

**Given** 漫画生成完成

**When** 用户点击"下载PDF"按钮

**Then** 浏览器下载漫画的PDF文件

#### Scenario: 导出元数据

**Given** 用户需要保留生成信息

**When** 用户点击"导出元数据"按钮

**Then** 系统下载包含场景描述和生成参数的JSON文件

### Requirement: 历史记录管理

系统MUST保存用户的生成历史。

#### Scenario: 保存生成记录

**Given** 用户生成了一部漫画

**When** 生成完成

**Then** 系统将漫画信息保存到历史记录（存储在IndexedDB）

#### Scenario: 查看历史列表

**Given** 用户点击"历史记录"标签

**When** 历史记录页面加载

**Then** 系统显示所有生成的漫画，包括缩略图和生成时间

#### Scenario: 从历史重新生成

**Given** 用户在历史记录中点击某个漫画

**When** 用户点击"重新生成"按钮

**Then** 系统使用相同的参数重新生成漫画

#### Scenario: 删除历史记录

**Given** 用户在历史记录中删除某条记录

**When** 确认删除

**Then** 系统从本地存储中移除该记录

### Requirement: 错误处理和用户提示

系统SHALL提供友好的错误处理和提示。

#### Scenario: API密钥缺失提示

**Given** 用户未配置API密钥就点击生成

**When** 系统检测到缺失密钥

**Then** 系统显示提示："请先在设置中配置API密钥"，并打开设置面板

#### Scenario: 网络错误处理

**Given** 网络连接中断

**When** 生成过程中发生网络错误

**Then** 系统显示错误消息："网络连接失败，请检查后重试"，并提供重试按钮

#### Scenario: 生成失败提示

**Given** 某个场景生成失败

**When** 系统检测到失败

**Then** 系统标记该场景为"生成失败"，并允许用户重新生成单个场景

#### Scenario: 内容安全警告

**Given** 用户提交包含敏感内容的文本

**When** 系统检测到敏感内容

**Then** 系统显示警告："您的内容包含敏感词，请修改后重试"

### Requirement: 后端API集成

系统MUST与后端服务进行RESTful API通信。

#### Scenario: 发送生成请求

**Given** 用户点击"生成漫画"按钮

**When** 前端向后端发送POST请求

**Then** 请求包含故事文本和生成参数

#### Scenario: 接收生成进度

**Given** 后端正在处理生成任务

**When** 后端推送进度更新

**Then** 前端实时更新进度显示

#### Scenario: 轮询生成状态

**Given** 使用轮询方式而非WebSocket

**When** 前端每2秒查询一次任务状态

**Then** 系统根据状态更新UI

### Requirement: 主题和个性化

系统SHALL支持主题切换和个性化设置。

#### Scenario: 切换深色/浅色主题

**Given** 用户偏好深色模式

**When** 用户点击主题切换按钮

**Then** 应用切换到深色主题，保存用户偏好到本地

#### Scenario: 自定义界面语言

**Given** 用户选择中文界面

**When** 应用加载

**Then** 所有界面元素显示中文文本

#### Scenario: 保存用户偏好

**Given** 用户配置了多个个性化设置（主题、语言、布局等）

**When** 用户关闭并重新打开应用

**Then** 系统恢复用户的个性化设置

### Requirement: 批量生成功能

系统MUST支持批量生成多个漫画。

#### Scenario: 批量生成界面

**Given** 用户点击"批量生成"按钮

**When** 系统打开批量生成面板

**Then** 界面允许用户添加多个故事到队列

#### Scenario: 批量任务队列

**Given** 用户添加了3个故事到队列

**When** 用户点击"开始批量生成"

**Then** 系统依次处理3个故事，显示总体进度

#### Scenario: 单个任务暂停/继续

**Given** 批量生成正在进行

**When** 用户暂停某个任务

**Then** 系统暂停该任务，其他任务继续

