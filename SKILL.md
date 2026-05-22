---
name: ai-docx-engineer
description: 将自定义JSON内容转换为Word文档，支持通过style.json自定义样式。让AI生成Word文档更加可控。
---

# AI DOCX Engine 转换工具

将自定义JSON内容转换为Word文档，支持通过style.json自定义样式。

## 项目结构

```
ai-docx-engineer/
├── SKILL.md              # 本文件 - 项目介绍和使用说明
├── style_table.md        # 详细的书写规范参考
├── default_style.json    # 默认样式定义
├── style.json            # 用户自定义样式（示例）
├── examples/             # 示例项目
│   ├── sample.json       # 示例内容文件
│   ├── sample_style.json # 示例样式文件
│   ├── images/           # 图片资源
│   └── out/              # 输出目录
└── core/                 # 核心代码目录
    ├── converter.py      # CLI入口
    ├── styles.py         # 样式引擎
    ├── parser.py         # JSON解析器
    ├── renderer.py       # DOCX渲染器
    ├── blocks/           # Block处理器
    │   ├── text.py
    │   ├── image.py
    │   ├── table.py
    │   └── page_break.py
    └── utils/            # 工具函数
        ├── borders.py
        └── spacing.py
```

## 你的职责

根据用户描述，生成或修改对应的JSON内容文件和style.json样式文件，然后转换成Word文档。

### 标准项目目录规范

建议为每个文档创建独立文件夹：

```
my_document/
├── content.json          # 内容文件（必须）
├── style.json            # 样式文件（必须）
├── images/               # 图片资源（可选）
│   ├── fig1.png
│   └── fig2.png
└── output.docx           # 输出文件（生成）
```

## 快速开始

### 转换命令

```bash
python -m core.converter <content.json> <style.json> <output.docx>
```

**注意：三个参数都必须提供**

### 示例

```bash
python -m core.converter examples/sample.json examples/sample_style.json examples/output.docx
```

## 内容文件格式 (content.json)

```json
{
  "blocks": [
    {
      "type": "text",
      "style": "标题1",
      "runs": [{"text": "第一章 绪论"}]
    },
    {
      "type": "text",
      "style": "正文",
      "runs": [
        {"text": "这是"},
        {"text": "粗体", "bold": true},
        {"text": "文字示例。"}
      ]
    },
    {
      "type": "image",
      "style": "图片",
      "src": "images/fig1.png"
    },
    {
      "type": "table",
      "rows": 3,
      "cols": 2,
      "cells": [
        ["名称", "数值"],
        ["A", "100"],
        ["B", "200"]
      ],
      "header_style": "表头",
      "body_style": "表内文字",
      "border": "three_line"
    },
    {
      "type": "page-break"
    }
  ]
}
```

## 支持的Block类型

| 类型 | 说明 | 必需字段 |
|------|------|----------|
| `text` | 文本段落 | `runs` |
| `image` | 图片 | `src` |
| `table` | 表格 | `rows`, `cols`, `cells` |
| `page-break` | 分页符 | 无 |

## Run内联样式

在 `runs` 数组中，每个run支持：

- `bold`: 粗体
- `italic`: 斜体
- `underline`: 下划线
- `superscript`: 上标
- `subscript`: 下标
- `color`: 文字颜色 (如 "FF0000")
- `highlight`: 高亮背景 (如 "FFFF00")

## 样式文件格式 (style.json)

```json
{
  "标题1": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "黑体",
    "font_size": 22,
    "bold": true,
    "alignment": "left",
    "line_spacing": {"units": "line", "value": 1.5},
    "space_before": {"units": "pt", "value": 6},
    "space_after": {"units": "pt", "value": 12}
  },
  "正文": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "宋体",
    "font_size": 12,
    "firstLineChars": 200
  }
}
```

## 详细规范

具体书写规范参考同目录下 `style_table.md` 文件。

## 完整示例

参见 `examples/` 目录：
- `sample.json` - 示例内容文件
- `sample_style.json` - 示例样式文件
- `images/` - 示例图片资源
