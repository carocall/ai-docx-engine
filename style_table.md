# JSON to DOCX 书写规范

本项目将内容文件从 XML 改为 JSON 格式，样式文件保持 JSON 不变。

## 内容文件结构（JSON）

内容文件采用扁平化的 Block + Run 架构：

```json
{
  "blocks": [
    {"type": "text", "style": "标题1", "runs": [...]},
    {"type": "image", "style": "图片", "src": "..."},
    {"type": "table", "rows": 3, "cols": 3, "cells": [...], ...},
    {"type": "page-break"}
  ]
}
```

## Block 类型

支持4种 Block 类型：

| 类型 | 说明 |
|------|------|
| `text` | 文本段落 |
| `image` | 图片 |
| `table` | 表格 |
| `page-break` | 换页符 |

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

### 重要变更说明

**表格样式配置已从 style.json 移至内容 JSON 中。**

以前表格样式在 style.json 中配置：
```json
{
  "三线表": {
    "header_style": "表头",
    "body_style": "表内文字",
    "border": "three_line"
  }
}
```

现在表格样式直接在内容 JSON 的 table block 中配置：
```json
{
  "type": "table",
  "header_style": "表头",
  "body_style": "表内文字",
  "border": "three_line"
}
```

**优势：**
1. 每个表格可以独立配置样式
2. 样式文件只包含纯样式定义，职责更清晰
3. AI 生成内容时更直观

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
  },
  "样式名称2": {
    ...
  }
}
```

### 可选样式属性

#### font_name
- 功能：指定西文字体名称
- 取值：Times New Roman, Arial, Calibri, Courier New 等
- 默认值：Times New Roman

```json
{
  "font_name": "Times New Roman"
}
```

#### font_name_east_asia
- 功能：指定东亚字体名称
- 取值：黑体, 宋体, 楷体, 微软雅黑, 仿宋 等
- 默认值：宋体

```json
{
  "font_name_east_asia": "黑体"
}
```

#### font_size
- 功能：指定字体大小
- 单位：磅（pt）
- 默认值：12

```json
{
  "font_size": 12
}
```

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

```json
{
  "bold": true
}
```

#### alignment
- 功能：设置段落对齐方式
- 取值："left", "center", "right", "justify"
- 默认值："left"

```json
{
  "alignment": "center"
}
```

#### space_before
- 功能：设置段前间距
- 格式：`{"units": "pt"|"line", "value": number}`
- 默认值：0

```json
{
  "space_before": {"units": "pt", "value": 24}
}
```

#### space_after
- 功能：设置段后间距
- 格式：`{"units": "pt"|"line", "value": number}`
- 默认值：0

```json
{
  "space_after": {"units": "line", "value": 1.5}
}
```

#### firstLineChars
- 功能：设置首行缩进的字符数
- 单位：字符宽度的 1/100，200 表示缩进 2 个字符

```json
{
  "firstLineChars": 200
}
```

#### line_spacing
- 功能：设置行间距
- 格式：`{"units": "pt"|"line", "value": number}`

```json
{
  "line_spacing": {"units": "pt", "value": 22}
}
```
或
```json
{
  "line_spacing": {"units": "line", "value": 1.5}
}
```

---

## 完整示例

### 内容文件 (document.json)

```json
{
  "blocks": [
    {
      "type": "text",
      "style": "标题1",
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
python converter.py <json文件路径> [输出docx路径] [style.json路径]
```

示例：
```bash
python converter.py document.json output.docx style.json
```

- 如果不指定输出路径，则自动在 JSON 同目录下生成同名 .docx 文件
- 如果不指定 style.json 路径，则默认使用 converter.py 同目录下的 style.json
