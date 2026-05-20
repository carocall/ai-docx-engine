---
name: xml-to-docx
description: 将自定义XML标签转换为Word文档，支持通过style.json自定义样式。让ai生成Word文档更加可控。
---
# XML to DOCX 转换工具

将自定义XML标签转换为Word文档，支持通过style.json自定义样式。
## 你的职责
根据用户描述，生成或修改对应的xml和style.json文件。然后根据需求转换成需要的word文档。
## 快速开始

### 转换命令

```bash
python converter.py <xml文件路径> [输出docx路径] [style.json路径]
```

- 如果不指定输出路径，则自动在XML同目录下生成同名.docx文件
- 如果不指定style.json路径，则默认使用converter.py同目录下的style.json

---

## 项目结构

```
xml-to-docx/
├── converter.py          # 核心转换脚本
├── style.json            # 默认样式配置文件
├── requirements.txt      # Python依赖列表
├── SKILL.md              # 项目文档
└── examples/             # 示例文件目录
    ├── sample.xml        # 示例XML文件
    ├── sample.docx       # 生成的示例文档（运行后生成）
    └── 样例.png          # 示例图片资源
```

### 文件说明

| 文件 | 说明 |
|------|------|
| `converter.py` | 主转换程序，解析XML并生成DOCX |
| `style.json` | 默认样式配置文件，定义标签对应的Word样式 |
| `requirements.txt` | 项目依赖，包含python-docx等库 |
| `SKILL.md` | 项目文档，包含使用说明和API文档 |
| `examples/` | 存放示例文件和测试资源 |

---

## XML 书写规范

### 基本结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <!-- 在此添加内容标签 -->
</root>
```

### 标签列表

| 标签 | 说明 | 示例 |
|------|------|------|
| 标题1~4 | 四级标题 | `<标题1>第1章 概述</标题1>` |
| 正文 | 正文段落 | `<正文>这是正文内容</正文>` |
| 图片 | 嵌入图片 | `<图片>image.png</图片>` |
| 图注 | 图片说明 | `<图注>图1-1 系统架构</图注>` |
| 表格 | 数据表格 | `<表格 rows="2" cols="3">...</表格>` |
| 表注 | 表格说明 | `<表注>表1-1 功能列表</表注>` |

### 标签规则

1. **不支持嵌套**：所有标签必须是平铺的，不能嵌套
2. **换行处理**：在XML中写入标签内容时，换行会被忽略
3. **根节点**：`root` 标签下直接放置内容标签

### 表格格式

表格使用 `|` 分隔行，`;` 分隔列：

```xml
<表格 rows="3" cols="3">
  表头1;表头2;表头3|内容1;内容2;内容3|内容4;内容5;内容6
</表格>
```

也可以写在同一行：

```xml
<表格 rows="3" cols="3">表头1;表头2;表头3|内容1;内容2;内容3|内容4;内容5;内容6</表格>
```

### 图片路径

图片路径支持：
- **相对路径**：相对于XML文件所在目录
- **绝对路径**：完整的文件路径
- **URL**：网络图片URL

```xml
<图片>image.png</图片>           <!-- 相对路径 -->
<图片>C:\images\photo.jpg</图片>  <!-- 绝对路径 -->
<图片>https://example.com/img.png</图片>  <!-- URL -->
```

---

## style.json 书写规范

### 文件位置

与 `converter.py` 同目录

### 基本结构

```json
{
  "标签名": {
    "属性1": "值",
    "属性2": "值"
  }
}
```

### 支持的属性

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `font_name` | 字符串 | 西文字体名称 | `"Arial"` |
| `font_name_east_asia` | 字符串 | 中文字体名称 | `"黑体"` |
| `font_size` | 数字 | 字号（磅） | `12` |
| `bold` | 布尔值 | 是否加粗 | `true` / `false` |
| `alignment` | 字符串 | 对齐方式 | `"left"` / `"center"` / `"right"` / `"justify"` |
| `line_spacing` | 数字 | 行间距倍数 | `1.5` |
| `first_line_indent` | 数字 | 首行缩进（磅） | `21.75`（约2字符） |
| `space_before` | 数字 | 段前间距（磅） | `24` |
| `space_after` | 数字 | 段后间距（磅） | `12` |
| `type` | 字符串 | 特殊类型 | `"horizontal"`（分隔线） |

### 字体设置

中文字体使用 `font_name_east_asia`，西文字体使用 `font_name`：

```json
{
  "正文": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "宋体",
    "font_size": 12
  }
}
```

### 对齐方式

| 值 | 说明 |
|------|------|
| `left` | 左对齐 |
| `center` | 居中 |
| `right` | 右对齐 |
| `justify` | 两端对齐 |

### 行间距

使用数字表示倍数：

```json
"line_spacing": 1.5
```

### 首行缩进

约21.75磅 = 2字符宽度：

```json
"first_line_indent": 21.75
```

---

## 添加自定义样式

### 步骤1：在XML中添加新标签

```xml
<root>
  <自定义标题>这是自定义标题</自定义标题>
  <特别注释>这是一段需要特别说明的文字</特别注释>
</root>
```

### 步骤2：在style.json中添加样式定义

```json
{
  "自定义标题": {
    "font_name": "Arial",
    "font_name_east_asia": "黑体",
    "font_size": 18,
    "bold": true,
    "alignment": "center",
    "line_spacing": 1.5,
    "space_before": 24,
    "space_after": 12
  },
  "特别注释": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "楷体",
    "font_size": 11,
    "italic": true,
    "alignment": "left",
    "space_before": 12,
    "space_after": 6
  }
}
```

### 步骤3：重新转换

```bash
python converter.py input.xml
```

---

## 完整示例

### 示例XML文件 (document.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <标题1>第1章 项目概述</标题1>
  <正文>本文档介绍XML到DOCX转换工具的设计与实现。该工具支持自定义标签和样式配置。</正文>
  <图片>architecture.png</图片>
  <图注>图1-1 系统架构图</图注>
  <正文>上图为系统整体架构，展示了主要组件之间的关系。</正文>

  <标题2>第2章 功能说明</标题2>
  <标题3>核心功能</标题3>
  <正文>本工具支持多种自定义标签的转换。</正文>

  <表格 rows="3" cols="3">功能名称;支持情况;说明|文本转换;是;基础功能|图片嵌入;是;支持相对路径|表格生成;是;行列式布局</表格>
  <表注>表2-1 功能支持列表</表注>
</root>
```

### 示例样式文件 (style.json)

```json
{
  "标题1": {
    "font_name": "Arial",
    "font_name_east_asia": "黑体",
    "font_size": 22,
    "bold": true,
    "line_spacing": 1.5,
    "space_before": 24,
    "space_after": 12
  },
  "标题2": {
    "font_name": "Arial",
    "font_name_east_asia": "黑体",
    "font_size": 18,
    "bold": true,
    "line_spacing": 1.5,
    "space_before": 18,
    "space_after": 10
  },
  "标题3": {
    "font_name": "Arial",
    "font_name_east_asia": "黑体",
    "font_size": 16,
    "bold": true,
    "line_spacing": 1.5,
    "space_before": 14,
    "space_after": 8
  },
  "正文": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "宋体",
    "font_size": 12,
    "line_spacing": 1.5,
    "first_line_indent": 21.75,
    "space_after": 6
  },
  "图注": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "楷体",
    "font_size": 10.5,
    "alignment": "center",
    "space_before": 6,
    "space_after": 12
  },
  "表注": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "楷体",
    "font_size": 10.5,
    "alignment": "center",
    "space_before": 6,
    "space_after": 12
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
    "space_before": 12,
    "space_after": 6
  },
  "表格": {
    "space_after": 12
  }
}
```

---

## 常用字体参考

### 中文字体

| 字体名 | 说明 |
|--------|------|
| 宋体 | 正式文档、正文 |
| 黑体 | 标题、粗体强调 |
| 楷体 | 注释、说明文字 |
| 仿宋 | 法律/政府文档 |
| 微软雅黑 | 现代感强的正文 |

### 西文字体

| 字体名 | 说明 |
|--------|------|
| Times New Roman | 正式文档、学术论文 |
| Arial | 现代感强、清晰易读 |
| Calibri | Office默认字体 |
| Courier New | 代码、等宽字体 |

## 参考文档

- `examples/sample.md` — 演示XML文件转换为DOCX文档的示例
- `examples/样例.png` — 演示XML文件内配套引用的图片