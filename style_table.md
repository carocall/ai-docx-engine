# Style 属性表

## font_name
- 功能：指定西文字体名称
- 可以取值 Times New Roman，Arial等字体名称
- 默认值：Times New Roman
比如：
```json
{
    "font_name": "Times New Roman",
}
```

## font_name_east_asia
- 功能：指定东亚字体名称
- 可以取值 黑体，宋体等字体名称
- 默认值：宋体
比如：
```json
{
    "font_name_east_asia": "黑体",
}
```

## font_size
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
### 注意映射关系 
- 22磅对应2号字体
- 18磅对应小2号字体
- 16磅对应3号字体 
- 14磅对应4号字体
- 12磅对应小四号字体


## bold
- 功能：设置字体是否加粗
- 可以取值 true 或 false
- 默认值：false
比如：
```json
{
    "bold": true,
}
```

## alignment
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

## space_before
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

## space_after
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

## firstLineChars
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

## line_spacing
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

## type
- 功能：指定特殊类型标识
- 可以取值：
  - "horizontal" - 表示这是一个水平分隔线标签
- 默认值：无
比如：
```json
{
    "type": "horizontal",
}
```