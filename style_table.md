# 书写规范
- 本项目支持4种标签，分别为:
- p：段落标签
- image：图片标签
- table：表格标签
- page-break：换页标签
## 注意
- 其中除了page-break标签，其他标签都支持style属性。
- 下面介绍个标签的书写
- 每一个xml标签有且只能有一个样式
## p标签

### 样式书写

#### font_name 可选样式
- 功能：指定西文字体名称
- 可以取值 Times New Roman，Arial，Calibri，Courier New等字体名称
- 默认值：Times New Roman
比如：
```json
{
    "font_name": "Times New Roman",
}
```

#### font_name_east_asia 可选样式
- 功能：指定东亚字体名称
- 可以取值 黑体，宋体，楷体，微软雅黑，仿宋等字体名称
- 默认值：宋体
比如：
```json
{
    "font_name_east_asia": "黑体",
}
```

#### font_size 可选样式
- 功能：指定字体大小
- 单位：磅（pt）
- 可以取值 数字，如 12、14、16、18、22 等
- 默认值：12
比如：
```json
{
    "font_size": 12,
}
```
- 注意映射关系 
- 22磅对应2号字体
- 18磅对应小2号字体
- 16磅对应3号字体 
- 14磅对应4号字体
- 12磅对应小四号字体


#### bold 可选样式
- 功能：设置字体是否加粗
- 可以取值 true 或 false
- 默认值：false
比如：
```json
{
    "bold": true,
}
```

#### alignment 可选样式
- 功能：设置段落对齐方式
- 可以取值：
  - "left" - 左对齐
  - "center" - 居中对齐
  - "right" - 右对齐
  - "justify" - 两端对齐
- 默认值："left"
比如：
```json
{
    "alignment": "center",
}
```

#### space_before 可选样式
- 功能：设置段前间距
- 格式：字典类型，包含 units 和 value
- units 可以取值：
  - "pt" - 磅值单位
  - "line" - 行数单位
- value：数值，根据 units 的不同表示磅值或行数
- 默认值：0（不设置段前间距）
比如：
```json
{
    "space_before": {"units": "pt", "value": 24},
}
```
或
```json
{
    "space_before": {"units": "line", "value": 2},
}
```

#### space_after 可选样式
- 功能：设置段后间距
- 格式：字典类型，包含 units 和 value
- units 可以取值：
  - "pt" - 磅值单位
  - "line" - 行数单位
- value：数值，根据 units 的不同表示磅值或行数
- 默认值：0（不设置段后间距）
比如：
```json
{
    "space_after": {"units": "pt", "value": 12},
}
```
或
```json
{
    "space_after": {"units": "line", "value": 1.5},
}
```

#### firstLineChars 可选样式
- 功能：设置首行缩进的字符数
- 单位：字符宽度的 1/100，即 100 等于 1 个字符宽度
- 可以取值 数字，如 200（表示缩进 2 个字符）
- 默认值：无（不设置首行缩进）
比如：
```json
{
    "firstLineChars": 200,
}
```

#### line_spacing 可选样式
- 功能：设置行间距
- 格式：字典类型，包含 units 和 value
- units 可以取值：
  - "pt" - 固定磅值行距
  - "line" - 倍数行距
- value：数值，根据 units 的不同表示磅值或倍数
- 默认值：无（不设置行间距）
比如：
```json
{
    "line_spacing": {"units": "pt", "value": 22},
}
```
或
```json
{
    "line_spacing": {"units": "line", "value": 1.5},
}
```
#### 实际用例
- 对于样式文件的写法，参考下面一个p样式
```json
  "default_style_p": {
    "font_name": "Times New Roman",
    "font_name_east_asia": "宋体",
    "font_size": 12,
    "bold": false,
    "alignment": "left",
    "line_spacing": {"units": "pt", "value": 22},
    "space_before": {"units": "pt", "value": 0},
    "space_after": {"units": "pt", "value": 0},
    "firstLineChars": 200
  },
```
### xml标签使用
- 对于标签的应用，可以这样
```xml
<p style="default_style_p">
    这是一个段落
</p>
```
## image标签

### 样式书写

#### alignment 可选样式
- 功能：设置图片对齐方式
- 可以取值：
  - "left" - 左对齐
  - "center" - 居中对齐
  - "right" - 右对齐
- 默认值："center"
比如：
```json
{
    "alignment": "center",
}
```

#### width_cm 可选样式
- 功能：设置图片宽度
- 单位：厘米（cm）
- 可以取值 数字，如 8、10、12、15 等
- 默认值：10
比如：
```json
{
    "width_cm": 10,
}
```

#### space_before 可选样式
- 功能：设置图片前间距
- 格式：字典类型，包含 units 和 value
- units 可以取值：
  - "pt" - 磅值单位
  - "line" - 行数单位
- value：数值，根据 units 的不同表示磅值或行数
- 默认值：0（不设置前间距）
比如：
```json
{
    "space_before": {"units": "pt", "value": 12},
}
```
或
```json
{
    "space_before": {"units": "line", "value": 1},
}
```

#### space_after 可选样式
- 功能：设置图片后间距
- 格式：字典类型，包含 units 和 value
- units 可以取值：
  - "pt" - 磅值单位
  - "line" - 行数单位
- value：数值，根据 units 的不同表示磅值或行数
- 默认值：0（不设置后间距）
比如：
```json
{
    "space_after": {"units": "pt", "value": 6},
}
```
或
```json
{
    "space_after": {"units": "line", "value": 0.5},
}
```

#### 实际用例
- 对于样式文件的写法，参考下面一个image样式
```json
  "图片": {
    "alignment": "center",
    "width_cm": 10,
    "space_before": {"units": "pt", "value": 12},
    "space_after": {"units": "pt", "value": 6}
  },
```
### xml标签使用
- 对于标签的应用，可以这样
```xml
<image src="image.png" style="图片"/>
```

## table标签

### 样式书写

#### header_style 必选样式
- 功能：指定表头行使用的样式名称
- 可以取值：已定义的样式名称，如 "表头"、"标题1" 等
- 注意：该样式必须在样式文件中已定义
比如：
```json
{
    "header_style": "表头",
}
```

#### body_style 必选样式
- 功能：指定表体行使用的样式名称
- 可以取值：已定义的样式名称，如 "表内文字"、"正文" 等
- 注意：该样式必须在样式文件中已定义
比如：
```json
{
    "body_style": "表内文字",
}
```

#### border 可选样式
- 功能：设置表格边框样式
- 可以取值：
  - "none" - 无边框
  - "grid" - 网格边框（所有边框都显示）
  - "three_line" - 三线表（仅显示顶线、底线和表头底线）
- 默认值："none"
比如：
```json
{
    "border": "three_line",
}
```

#### space_after 可选样式
- 功能：设置表格后间距
- 格式：字典类型，包含 units 和 value
- units 可以取值：
  - "pt" - 磅值单位
  - "line" - 行数单位
- value：数值，根据 units 的不同表示磅值或行数
- 默认值：0（不设置后间距）
比如：
```json
{
    "space_after": {"units": "pt", "value": 12},
}
```
或
```json
{
    "space_after": {"units": "line", "value": 1},
}
```

#### 实际用例
- 对于样式文件的写法，参考下面一个table样式
```json
  "表格": {
    "header_style": "表头",
    "body_style": "表内文字",
    "border": "three_line",
    "space_after": {"units": "pt", "value": 12}
  },
  "网格表": {
    "header_style": "表头",
    "body_style": "表内文字",
    "border": "grid",
    "space_after": {"units": "pt", "value": 12}
  },
```
### xml标签使用
- 对于标签的应用，可以这样
```xml
<table style="表格" rows="3" cols="3">
    表头1;表头2;表头3|
    单元格1;单元格2;单元格3|
    单元格4;单元格5;单元格6
</table>
```
- rows 属性：指定表格行数
- cols 属性：指定表格列数
- 表格内容格式：使用 `|` 分隔行，使用 `;` 分隔单元格
