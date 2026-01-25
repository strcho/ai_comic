11# Comic Generation Spec

## ADDED Requirements

### Requirement: 组合多张图像为漫画

系统MUST能够将多个场景的图像组合成标准的漫画格式。

#### Scenario: 将3张图像组合成横向漫画

**Given** 有3张已生成的场景图像

**When** 系统组合图像

**Then** 系统输出包含3个面板的横向漫画（例如1920x640像素）

#### Scenario: 将4张图像组合成2x2网格

**Given** 有4张已生成的场景图像

**And** 用户配置布局为2x2网格

**When** 系统组合图像

**Then** 系统输出2x2布局的漫画（例如1024x1024像素）

### Requirement: 支持多种面板布局

系统SHALL提供多种预设的面板布局选项。

#### Scenario: 横向布局

**Given** 用户选择横向布局（horizontal）

**When** 系统组合图像

**Then** 所有面板横向排列，高度统一

#### Scenario: 网格布局

**Given** 用户选择2x3网格布局

**When** 系统组合6张图像

**Then** 系统按照2列3行的网格排列图像

#### Scenario: 自定义布局配置

**Given** 用户提供JSON布局配置：
```json
{
  "panels": [
    {"x": 0, "y": 0, "w": 0.5, "h": 1},
    {"x": 0.5, "y": 0, "w": 0.5, "h": 0.5},
    {"x": 0.5, "y": 0.5, "w": 0.5, "h": 0.5}
  ]
}
```

**When** 系统组合图像

**Then** 系统按照自定义坐标和尺寸排列3个面板

### Requirement: 添加面板边框和间距

系统SHALL能够为面板添加边框和间距。

#### Scenario: 添加黑色边框

**Given** 用户配置边框宽度为3像素，颜色为黑色

**When** 系统组合图像

**Then** 每个面板周围有3像素的黑色边框

#### Scenario: 添加面板间距

**Given** 用户配置面板间距为10像素

**When** 系统组合图像

**Then** 面板之间有10像素的白色间距

#### Scenario: 无边框紧凑布局

**Given** 用户配置无边框和间距

**When** 系统组合图像

**Then** 面板之间紧密相连，无缝隙

### Requirement: 支持多种输出格式

系统SHALL能够将漫画输出为多种常见格式。

#### Scenario: 输出为PNG

**Given** 用户配置输出格式为PNG

**When** 系统保存漫画

**Then** 系统生成高质量PNG文件

#### Scenario: 输出为JPG

**Given** 用户配置输出格式为JPG

**And** 用户配置质量为90

**When** 系统保存漫画

**Then** 系统生成90%质量的JPG文件

#### Scenario: 输出为PDF

**Given** 用户配置输出格式为PDF

**When** 系统保存漫画

**Then** 系统生成PDF文件，适合打印或分享

### Requirement: 保存元数据

系统SHALL能够保存漫画的元数据信息。

#### Scenario: 保存JSON元数据

**Given** 系统生成漫画

**When** 系统保存文件

**Then** 系统同时创建元数据JSON文件，包含：
- 原始场景描述
- 图像生成参数
- API调用时间戳
- 各面板对应的场景索引

#### Scenario: 元数据嵌入图像

**Given** 用户配置嵌入元数据

**When** 系统保存图像

**Then** 系统将元数据作为EXIF信息嵌入图像文件

### Requirement: 支持场景标签和编号

系统SHALL能够为每个面板添加场景编号或标签。

#### Scenario: 添加场景编号

**Given** 用户配置显示场景编号

**When** 系统生成漫画

**Then** 每个面板左上角显示编号（如"1", "2", "3"）

#### Scenario: 添加场景描述标签

**Given** 场景描述为"男孩在奔跑"

**And** 用户配置显示场景标签

**When** 系统生成漫画

**Then** 面板底部显示文本："场景1：男孩在奔跑"

### Requirement: 处理不同尺寸的输入图像

系统MUST能够处理和调整不同尺寸的输入图像。

#### Scenario: 统一调整到标准尺寸

**Given** 输入图像尺寸分别为512x512, 1024x1024, 768x768

**And** 用户配置面板尺寸为512x512

**When** 系统组合图像

**Then** 系统将所有图像调整到512x512，保持宽高比（如有需要则裁剪或填充）

#### Scenario: 保持宽高比填充

**Given** 输入图像为800x600

**And** 目标面板为512x512

**When** 系统调整图像

**Then** 系统保持宽高比，使用白色或透明填充到512x512

### Requirement: 批量处理多个漫画

系统SHALL能够批量处理多个故事生成多部漫画。

#### Scenario: 批量处理3个故事

**Given** 用户提供3个故事文本文件

**When** 系统批量处理

**Then** 系统依次处理每个故事，生成3部独立的漫画

#### Scenario: 并行批量处理

**Given** 用户配置并行批量处理

**And** 有5个故事待处理

**When** 系统批量处理

**Then** 系统并行处理多个故事（受限于并发数）

### Requirement: 命令行输出控制

系统SHALL能够通过命令行参数控制输出行为。

#### Scenario: 指定输出目录

**Given** 用户使用参数 --output ./comics

**When** 系统保存漫画

**Then** 漫画文件保存到./comics目录

#### Scenario: 指定输出文件名

**Given** 用户使用参数 --name my-comic

**When** 系统保存漫画

**Then** 漫画文件命名为my-comic.png

#### Scenario: 仅生成不保存

**Given** 用户使用参数 --preview-only

**When** 系统处理完成

**Then** 系统在临时目录生成文件，预览后删除

## 交叉引用

- 依赖：image-generation（接收生成的图像作为输入）
- 依赖：story-processor（接收场景元数据用于标签生成）
- 相关：layout-engine（面板布局逻辑）
