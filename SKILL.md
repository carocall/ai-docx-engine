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

### 书写规范

#### xml基本结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <!-- 在此添加内容标签 -->
</root>
```

#### style.json 书写规范
- 文件位置
与 `converter.py` 同目录
- 基本结构
```json
{
  "标签名1": {
    "属性1": "值",
    "属性2": "值"
  },
  "标签名2": "值"
}
```
#### 具体书写规范参考style_table.md文件


## 完整示例
- 同目录下有examples文件夹。这是一个标注的xml-to-docx示例文件。
- 标准的xml-to-docx项目目录如下：
```
├── examples
│   ├── sample.xml //主XML文件，包含所有内容
│   ├── sample_style.json //自定义样式文件
│   ├── images //图片文件夹，包含所有图片文件
│       ├── 样例.png
│   ├── out //输出文件夹，包含转换后的docx文件
```
- 其中，`sample.xml`是示例XML文件，`images`文件夹下是图片文件。