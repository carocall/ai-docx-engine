# JSON to DOCX 书写规范

本项目将内容文件从 XML 改为 JSON 格式，样式文件保持 JSON 不变。

## 内容文件结构（JSON）

内容文件采用扁平化的 Block + Run 架构：

```json
{
  "blocks": [
    {"type": "toc", "levels": [1, 2, 3]},
    {"type": "heading", "level": 1, "runs": [...]},
    {"type": "text", "style": "正文", "runs": [...]},
    {"type": "image", "style": "图片", "src": "..."},
    {"type": "table", "rows": 3, "cols": 3, "cells": [...], ...},
    {"type": "page-break"}
  ]
}
```

## Block 类型

支持6种 Block 类型：

| 类型 | 说明 | 职责 |
|------|------|------|
| `heading` | 结构化标题 | 定义文档结构（level） |
| `toc` | 目录 | 收集 heading 结构生成目录 |
| `text` | 文本段落 | 普通段落内容 |
| `image` | 图片 | 插入图片 |
| `table` | 表格 | 插入表格 |
| `page-break` | 换页符 | 分页 |

### 三层分离原则

- **heading** = 结构（定义标题级别）
- **toc** = 结构选择（收录哪些级别的标题）
- **style.json** = 外观（字体、字号、间距等样式）

三者必须分离，互不耦合。

---

## heading 类型

### 基本结构

```json
{
  "type": "heading",
  "level": 1,
  "id": "intro",
  "runs": [
    {"text": "绪论"}
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 固定值 `"heading"` |
| `level` | number | 是 | 标题级别：1 / 2 / 3 / 4 |
| `style` | string | 否 | 指定样式名称，覆盖默认映射 |
| `id` | string | 否 | 书签ID，用于内部跳转引用 |
| `runs` | array | 否 | Run 数组，支持内联富文本 |

### 说明

- `level` 对应 Word 的 Heading 1/2/3/4
- renderer 会自动设置 `outlineLevel`，无需在 JSON 中指定
- **样式优先级**：`style` 字段 > 中文样式名（"标题1"等）> 默认样式（heading1等）

### 示例

```json
// 使用默认样式映射
{
  "type": "heading",
  "level": 2,
  "runs": [{"text": "2.1 研究背景"}]
}

// 指定自定义样式
{
  "type": "heading",
  "level": 2,
  "style": "我的二级标题",
  "runs": [{"text": "2.1 研究背景"}]
}

// 带书签和内联样式
{
  "type": "heading",
  "level": 1,
  "id": "intro",
  "runs": [
    {"text": "第1章 "},
    {"text": "绪论", "bold": true}
  ]
}
```

---

## toc 类型

### 基本结构

```json
{
  "type": "toc",
  "levels": [1, 2, 3],
  "style_level_one": "目录一级",
  "style_level_two": "目录二级",
  "style_level_three": "目录三级"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 固定值 `"toc"` |
| `levels` | array | 否 | 收录哪些级别的标题，默认 `[1, 2, 3]` |
| `style_level_one` | string | 否 | TOC 1级样式名称，默认 `"TOC1"` |
| `style_level_two` | string | 否 | TOC 2级样式名称，默认 `"TOC2"` |
| `style_level_three` | string | 否 | TOC 3级样式名称，默认 `"TOC3"` |

### 说明

- toc 负责"收集结构"和"指定各级别样式"
- 生成后会在文档中插入 TOC 域，显示提示文字"点击更新域来更新目录"
- 用户需要在 Word 中手动更新域（右键 → 更新域）来生成实际目录内容
- 目录各级别的外观由 `style_level_one/two/three` 指定的样式控制

### 示例

```json
// 使用默认样式
{
  "type": "toc",
  "levels": [1, 2, 3]
}

// 指定自定义样式
{
  "type": "toc",
  "levels": [1, 2],
  "style_level_one": "目录一级",
  "style_level_two": "目录二级",
  "style_level_three": "目录三级"
}
```

---

## text 类型

### 基本结构

```json
{
  "type": "text",
  "style": "正文",
  "runs": [
    {"text": "普通文字"},
    {"text": "粗体文字", "bold": true},
    {"text": "斜体文字", "italic": true}
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 固定值 `"text"` |
| `style` | string | 否 | 引用的样式名称，不存在则使用默认样式 |
| `runs` | array | 否 | Run 数组，每个 Run 是一段带有格式的文字 |

### Run 内联样式

每个 Run 支持以下内联样式：

| 样式 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `text` | string | 文字内容 | `{"text": "Hello"}` |
| `bold` | boolean | 粗体 | `{"text": "粗体", "bold": true}` |
| `italic` | boolean | 斜体 | `{"text": "斜体", "italic": true}` |
| `underline` | boolean | 下划线 | `{"text": "下划线", "underline": true}` |
| `superscript` | boolean | 上标 | `{"text": "上标", "superscript": true}` |
| `subscript` | boolean | 下标 | `{"text": "下标", "subscript": true}` |
| `color` | string | 文字颜色（HEX格式） | `{"text": "红色", "color": "FF0000"}` |
| `highlight` | string | 高亮背景色（HEX格式） | `{"text": "高亮", "highlight": "FFFF00"}` |

### 完整示例

```json
{
  "type": "text",
  "style": "正文",
  "runs": [
    {"text": "这是一个"},
    {"text": "粗体", "bold": true},
    {"text": "、"},
    {"text": "斜体", "italic": true},
    {"text": "和"},
    {"text": "红色", "color": "FF0000"},
    {"text": "文字的示例。"}
  ]
}
```

---

## image 类型

### 基本结构

```json
{
  "type": "image",
  "style": "图片",
  "src": "images/example.png"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 固定值 `"image"` |
| `style` | string | 否 | 引用的样式名称 |
| `src` | string | 是 | 图片路径（相对或绝对） |

---

## table 类型

### 基本结构

```json
{
  "type": "table",
  "style": "表格",
  "rows": 3,
  "cols": 3,
  "cells": [
    ["表头1", "表头2", "表头3"],
    ["数据1", "数据2", "数据3"],
    ["数据4", "数据5", "数据6"]
  ],
  "header_style": "表头",
  "body_style": "表内文字",
  "border": "three_line",
  "space_after": {"units": "pt", "value": 12}
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 固定值 `"table"` |
| `style` | string | 否 | 引用的样式名称（主要用于段落样式） |
| `rows` | number | 是 | 表格行数 |
| `cols` | number | 是 | 表格列数 |
| `cells` | array | 是 | 二维数组，表示单元格内容 |
| `header_style` | string | 否 | 表头行使用的样式名称，默认 `"default_style_text"` |
| `body_style` | string | 否 | 表体行使用的样式名称，默认 `"default_style_text"` |
| `border` | string | 否 | 边框样式：`"none"`、`"grid"`、`"three_line"`，默认 `"three_line"` |
| `space_after` | object | 否 | 表格后间距 |

### 边框样式说明

| 样式值 | 说明 |
|--------|------|
| `"none"` | 无边框 |
| `"grid"` | 网格边框（所有边框都显示） |
| `"three_line"` | 三线表（仅显示顶线、底线和表头底线） |

---

## page-break 类型

### 基本结构

```json
{
  "type": "page-break"
}
```

无需其他字段，直接插入换页符。

---

## 样式文件（style.json）

样式文件定义段落级别的样式，供内容文件引用。

### 基本结构

```json
{
  "样式名称1": {
    "font_name": "Times New Roman",
    "font_size": 12,
    ...
  }
}
```

### 可选样式属性

#### font_name
- 功能：指定西文字体名称
- 取值：Times New Roman, Arial, Calibri, Courier New 等
- 默认值：Times New Roman

#### font_name_east_asia
- 功能：指定东亚字体名称
- 取值：黑体, 宋体, 楷体, 微软雅黑, 仿宋 等
- 默认值：宋体

#### font_size
- 功能：指定字体大小（磅）
- 默认值：12

字体大小映射：
- 22磅 = 2号字体
- 18磅 = 小2号字体
- 16磅 = 3号字体
- 14磅 = 4号字体
- 12磅 = 小四号字体

#### bold
- 功能：设置字体是否加粗
- 取值：true 或 false
- 默认值：false

#### alignment
- 功能：设置段落对齐方式
- 取值："left", "center", "right", "justify"
- 默认值："left"

#### space_before / space_after
- 功能：设置段前/段后间距
- 格式：`{"units": "pt"|"line", "value": number}`

#### firstLineChars
- 功能：设置首行缩进的字符数
- 单位：字符宽度的 1/100，200 表示缩进 2 个字符

#### line_spacing
- 功能：设置行间距
- 格式：`{"units": "pt"|"line", "value": number}`

---

## 完整示例

### 内容文件 (document.json)

```json
{
  "blocks": [
    {
      "type": "heading",
      "level": 1,
      "runs": [{"text": "1 引言"}]
    },
    {
      "type": "text",
      "style": "正文",
      "runs": [
        {"text": "本文研究了"},
        {"text": "重要问题", "bold": true},
        {"text": "的解决方案。"}
      ]
    },
    {
      "type": "heading",
      "level": 2,
      "runs": [{"text": "1.1 研究背景"}]
    },
    {
      "type": "text",
      "style": "正文",
      "runs": [{"text": "正文内容..."}]
    },
    {
      "type": "table",
      "rows": 2,
      "cols": 2,
      "cells": [
        ["方法", "效果"],
        ["方法A", "优秀"]
      ],
      "header_style": "表头",
      "body_style": "表内文字",
      "border": "three_line"
    },
    {
      "type": "image",
      "style": "图片",
      "src": "images/fig1.png"
    }
  ]
}
```

### 样式文件 (style.json)

```json
{
  "标题1": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "黑体",
    "font_size": 22,
    "bold": true,
    "alignment": "center",
    "line_spacing": {"units": "line", "value": 1.5}
  },
  "标题2": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "黑体",
    "font_size": 16,
    "bold": true,
    "line_spacing": {"units": "line", "value": 1.5}
  },
  "正文": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "宋体",
    "font_size": 12,
    "firstLineChars": 200
  },
  "表头": {
    "font_name": "Arial",
    "font_name_east_asia": "宋体",
    "font_size": 11,
    "bold": true,
    "alignment": "center"
  },
  "表内文字": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "宋体",
    "font_size": 11,
    "alignment": "center"
  },
  "图片": {
    "alignment": "center",
    "width_cm": 10
  }
}
```

---

## 转换命令

```bash
python -m core.converter <content.json> <style.json> <output.docx>
```

示例：
```bash
python -m core.converter document.json style.json output.docx
```

**注意：三个参数都必须提供。**
