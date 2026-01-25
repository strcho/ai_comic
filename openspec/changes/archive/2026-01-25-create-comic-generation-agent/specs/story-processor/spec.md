# Story Processor Spec

## ADDED Requirements

### Requirement: 从文本描述中提取场景

系统MUST能够从用户提供的文本描述中提取出多个独立的场景，每个场景包含视觉描述信息。

#### Scenario: 从简单文本提取场景

**Given** 用户输入文本："一个男孩在公园里奔跑，阳光明媚。然后他遇到了一个女孩，两人握手。"

**When** 系统处理这段文本

**Then** 系统提取出2个场景：
- 场景1：一个男孩在公园里奔跑，阳光明媚
- 场景2：男孩遇到一个女孩，两人握手

#### Scenario: 处理带有明确场景标记的文本

**Given** 用户输入文本：
```
场景1：侦探进入黑暗的房间
场景2：他在桌子上发现了一把钥匙
场景3：他转动钥匙，门打开了
```

**When** 系统处理这段文本

**Then** 系统提取出3个场景，每个场景保留对应的描述

### Requirement: 清洗和标准化场景描述

系统SHALL对提取的场景描述进行清洗，去除无关信息，增强视觉元素的清晰度。

#### Scenario: 清洗包含对话的文本

**Given** 场景描述："'你好！'他说道，脸上带着微笑"

**When** 系统清洗这段描述

**Then** 系统输出："一个角色微笑着，正在说话"（去除对话文本，保留动作和表情）

#### Scenario: 提取关键视觉元素

**Given** 场景描述："红色的跑道上，穿着蓝色运动服的运动员正在冲刺"

**When** 系统提取关键元素

**Then** 系统识别出：
- 场景：红色跑道
- 人物：穿着蓝色运动服的运动员
- 动作：冲刺

### Requirement: 生成图像生成提示词

系统MUST为每个场景生成适合图像生成API的提示词（prompts）。

#### Scenario: 基础提示词生成

**Given** 场景描述："一个女孩在海边看日落"

**When** 系统生成提示词

**Then** 系统输出包含：核心描述 + 风格修饰词
- 示例："A girl watching sunset at the beach, comic style, illustration"

#### Scenario: 自定义风格提示词

**Given** 场景描述："一个女孩在海边看日落" 和用户配置风格："manga style"

**When** 系统生成提示词

**Then** 系统输出："A girl watching sunset at the beach, manga style, detailed"

#### Scenario: 支持负面提示词

**Given** 用户配置负面提示词："blurry, low quality"

**When** 系统生成提示词

**Then** 系统的API调用包含负面提示词参数

### Requirement: 处理不同输入格式

系统SHALL支持多种文本输入格式。

#### Scenario: 处理纯文本段落

**Given** 用户输入一段连续的段落文本

**When** 系统处理文本

**Then** 系统根据句子数量和长度自动分割成适当数量的场景（默认3-5个）

#### Scenario: 处理JSON格式输入

**Given** 用户输入JSON格式的结构化场景数据

**When** 系统处理文本

**Then** 系统解析JSON并使用结构化的场景信息

#### Scenario: 处理从文件读取输入

**Given** 用户指定文本文件路径（如story.txt）

**When** 系统处理文本

**Then** 系统读取文件内容并处理其中的场景描述

### Requirement: 配置和可调参数

系统SHALL提供配置项控制场景提取行为。

#### Scenario: 配置场景数量

**Given** 用户配置目标场景数量为4

**When** 系统处理文本

**Then** 系统尽量将文本分成4个场景（在合理范围内）

#### Scenario: 配置场景标记规则

**Given** 用户配置自定义场景标记："Panel X:"模式

**When** 系统处理文本

**Then** 系统按照"Panel 1:", "Panel 2:"等模式识别场景

#### Scenario: 配置文本清洗规则

**Given** 用户配置要移除的文本类型（如对话、旁白等）

**When** 系统清洗场景描述

**Then** 系统按照配置规则移除相应内容

## 交叉引用

- 依赖：image-generation（需要提供场景描述用于生成图像）
- 相关：comic-generation（场景数量影响面板布局）
