---
name: ai-docx-engineer
description: 将自定义json数据转换为Word文档，支持通过style.json自定义样式。让ai生成Word文档更加可控。
---
# AI DOCX ENGIN 转换工具
将自定义json数据转换为Word文档，支持通过style.json自定义样式。
## 你的职责
根据用户描述，生成或修改对应的json和style.json文件。然后根据需求转换成需要的word文档。
- 建议在当前目录创建一个文件夹，要符合规范：
```
├── examples //ai-docx-engineer项目文件
│   ├── sample.json //主json文件，包含所有内容
│   ├── style.json //自定义样式文件
│   ├── images //图片文件夹，包含所有图片文件
│       ├── 样例.png
│   ├── out //输出文件夹，包含转换后的docx文件
│       ├── sample.docx
```
## 快速开始

### 转换命令

```bash
python converter.py <json文件路径> [输出docx路径] [style.json路径]
```

- 如果不指定输出路径，则自动在json同目录下生成同名.docx文件
- 如果不指定style.json路径，则默认使用converter.py同目录下的style.json

---

### 书写规范

- 具体书写规范参考同目录下style_table.md文件


## 完整示例
- 同目录下有examples文件夹。这是一个标注的xml-to-docx示例文件。
- 标准的xml-to-docx项目目录如下：
```
├── examples
│   ├── sample.json //主json文件，包含所有内容
│   ├── style.json //自定义样式文件
│   ├── images //图片文件夹，包含所有图片文件
│       ├── 样例.png
│   ├── out //输出文件夹，包含转换后的docx文件
```
- 其中，`sample.json`是示例json文件，`images`文件夹下是图片文件。
