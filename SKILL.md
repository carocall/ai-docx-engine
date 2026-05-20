---
name: xml-to-docx
description: 将自定义XML标签转换为Word文档，支持通过style.json自定义样式。让ai生成Word文档更加可控。
---
# XML to DOCX 转换工具

将自定义XML标签转换为Word文档，支持通过style.json自定义样式。
## 你的职责
根据用户描述，生成或修改对应的xml和style.json文件。然后根据需求转换成需要的word文档。
- 建议在当前目录创建一个文件夹，要符合规范：
```
├── examples //xml-to-doxc项目文件
│   ├── sample.xml //主XML文件，包含所有内容
│   ├── style.json //自定义样式文件
│   ├── images //图片文件夹，包含所有图片文件
│       ├── 样例.png
│   ├── out //输出文件夹，包含转换后的docx文件
│       ├── sample.docx
```
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
- 标签主要分为段落标签和非段落标签，对于段落标签可以自行拓展，非段落标签只能修改样式，不能拓展。
#### 已有标签说明
- 内置的不需要设置样式的特殊标签
| 标签 | 说明 | 示例 |
|------|------|------|
| 换页 | 这是一个单独标签，不需要设置样式，直接就能用 | <换页/> |

- 非段落标签，可以在自定义style.json里面调样式。建议每个style.json内都要有这些样式。
| 标签 | 说明 | 示例 |
|------|------|------|
| 图片 | 嵌入图片 | `<图片>image.png</图片>` |
| 表格 | 数据表格 | `<表格 rows="2" cols="3">...</表格>` |

- 已有段落标签，可以在自定义style.json里面调样式。这些是基础样式，建议每个style.json内都要有这些样式。如果需要其他段落样式，自行在style.json内定义
| 标签 | 说明 | 示例 |
|------|------|------|
| 标题1~4 | 四级标题 | `<标题1>第1章 概述</标题1>` |
| 正文 | 正文段落 | `<正文>这是正文内容</正文>` |
| 图注 | 图片说明 | `<图注>图1-1 系统架构</图注>` |
| 表注 | 表格说明 | `<表注>表1-1 功能列表</表注>` |

#### 拓展段落标签的方式
- 这里注意，所有标签均为style.json中定义的标签。
- 如果需要拓展标签，你需要先在style.json中定义标签，才能在XML中使用。

### 标签规则
- **不支持嵌套**：所有标签必须是平铺的，不能嵌套
- **根节点**：`root` 标签下直接放置内容标签

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
  "标签名1": {
    "属性1": "值",
    "属性2": "值"
  },
  "标签名2": "值"
}
```
具体属性样式参考style_table.md文件


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
- 同目录下有examples文件夹。这是一个标注的xml-to-docx示例文件。
- 标准的xml-to-docx项目目录如下：
```
├── examples
│   ├── sample.xml //主XML文件，包含所有内容
│   ├── style.json //自定义样式文件
│   ├── images //图片文件夹，包含所有图片文件
│       ├── 样例.png
│   ├── out //输出文件夹，包含转换后的docx文件
│       ├── sample.docx
```
- 其中，`sample.xml`是示例XML文件，`images`文件夹下是图片文件。