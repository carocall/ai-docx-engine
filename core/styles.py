"""
样式引擎 - 严格模式：样式必须存在，否则报错
"""
import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class StyleNotFoundError(Exception):
    """样式不存在错误"""
    pass


class StyleEngine:
    """样式引擎，负责样式的加载和注册（严格模式）"""

    def __init__(self, doc: Document, user_style_path: str = None):
        self.doc = doc
        self.styles = self._load_styles(user_style_path)
        self._register_styles()

    def _load_styles(self, user_style_path: str = None) -> dict:
        """加载用户样式文件"""
        if not user_style_path:
            raise StyleNotFoundError("未提供样式文件路径")

        path = Path(user_style_path)
        if not path.exists():
            raise StyleNotFoundError(f"样式文件不存在: {user_style_path}")

        with open(path, 'r', encoding='utf-8') as f:
            styles = json.load(f)

        if not styles:
            raise StyleNotFoundError("样式文件为空")

        return styles

    def _register_styles(self):
        """将所有样式注册到Word文档"""
        for style_name, style_props in self.styles.items():
            self._register_paragraph_style(style_name, style_props)

    def _register_paragraph_style(self, style_name: str, style_props: dict):
        """注册单个段落样式"""
        # 检查样式是否已存在
        if style_name in [s.name for s in self.doc.styles]:
            para_style = self.doc.styles[style_name]
        else:
            para_style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)

        # 设置字体
        font_name = style_props.get("font_name", "Times New Roman")
        font_name_east_asia = style_props.get("font_name_east_asia", "宋体")
        para_style.font.name = font_name
        para_style.font.name_east_asia = font_name_east_asia

        # 设置东亚字体
        rFonts = para_style.font.element.rPr.rFonts
        rFonts.set(qn('w:eastAsia'), font_name_east_asia)

        # 设置字体大小
        font_size = style_props.get("font_size", 12)
        para_style.font.size = Pt(font_size)

        # 设置加粗
        para_style.font.bold = style_props.get("bold", False)

        # 设置对齐方式
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        alignment = style_props.get("alignment", "left")
        alignment_map = {
            "left": WD_ALIGN_PARAGRAPH.LEFT,
            "center": WD_ALIGN_PARAGRAPH.CENTER,
            "right": WD_ALIGN_PARAGRAPH.RIGHT,
            "justify": WD_ALIGN_PARAGRAPH.JUSTIFY
        }
        para_style.paragraph_format.alignment = alignment_map.get(alignment, WD_ALIGN_PARAGRAPH.LEFT)

        # 设置字体颜色
        para_style.font.color.rgb = RGBColor(0, 0, 0)

        # 设置段前间距
        self._set_spacing(para_style.paragraph_format, "space_before", style_props.get("space_before"))

        # 设置段后间距
        self._set_spacing(para_style.paragraph_format, "space_after", style_props.get("space_after"))

        # 设置首行缩进
        if style_props.get("firstLineChars"):
            pPr = para_style.element.get_or_add_pPr()
            ind = OxmlElement('w:ind')
            ind.set(qn('w:firstLineChars'), str(int(style_props["firstLineChars"])))
            pPr.append(ind)

        # 设置行高
        if style_props.get("line_spacing"):
            line_spacing = style_props["line_spacing"]
            units = line_spacing.get("units", "line")
            value = line_spacing.get("value", 1.0)
            if units == "pt":
                para_style.paragraph_format.line_spacing = Pt(value)
                para_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            else:
                para_style.paragraph_format.line_spacing = value

    def _set_spacing(self, para_format, attr_name: str, spacing_config):
        """设置段落间距"""
        if spacing_config:
            units = spacing_config.get("units", "pt")
            value = spacing_config.get("value", 0)
            if units == "line":
                setattr(para_format, attr_name, Pt(value * 12))  # 1行≈12磅
            else:
                setattr(para_format, attr_name, Pt(value))
        else:
            setattr(para_format, attr_name, Pt(0))

    def get_style(self, style_name: str) -> dict:
        """获取样式定义，不存在则报错"""
        if style_name not in self.styles:
            raise StyleNotFoundError(f"样式不存在: '{style_name}'")
        return self.styles[style_name]

    def require_style(self, style_name: str, context: str = ""):
        """要求样式必须存在，否则报错"""
        if not style_name:
            raise StyleNotFoundError(f"{context}: 样式名称为空")
        if style_name not in self.styles:
            raise StyleNotFoundError(f"{context}: 样式不存在 '{style_name}'")
        return style_name

    def has_style(self, style_name: str) -> bool:
        """检查样式是否存在"""
        return style_name in self.styles
