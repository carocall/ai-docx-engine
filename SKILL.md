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

- 这里注意，所有标签均为style.json中定义的标签。
- 如果需要拓展标签，你需要先在style.json中定义标签，才能在XML中使用。

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

具体属性样式参考style_table.md文件

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
