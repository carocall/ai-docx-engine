"""
代码块处理器（严格模式）

代码块是独立的 block 类型，不是 paragraph 的子类型。
- content 为纯文本，按换行拆分为多行
- 每行渲染为独立段落，保留原始缩进和空格
- 通过 style.json 中的样式控制等宽字体、背景色、缩进、行距
"""
from docx.shared import RGBColor, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from .base import BlockHandler
from ..parser import CodeBlock
from ..styles import StyleNotFoundError


class CodeHandler(BlockHandler):
    """代码块处理器"""

    def can_handle(self, block) -> bool:
        return isinstance(block, CodeBlock)

    def handle(self, block: CodeBlock):
        """处理代码块"""
        # 严格检查样式
        if block.style:
            style_name = block.style
            self.style_engine.require_style(style_name, "code")
        else:
            raise StyleNotFoundError("code: 未指定样式名称")

        # 获取样式定义（用于读取 background_color、left_indent_cm 等）
        style_props = self.style_engine.get_style(style_name)

        # 将 content 按行拆分
        lines = block.content.split('\n')

        # 获取背景色
        bg_color = style_props.get("background_color", "")

        # 获取左缩进（厘米）
        left_indent_cm = style_props.get("left_indent_cm", 0)

        for line in lines:
            self._add_code_line(line, style_name, bg_color, left_indent_cm)

    def _add_code_line(self, text: str, style_name: str,
                       bg_color: str = "", left_indent_cm: float = 0):
        """添加一行代码"""
        para = self.doc.add_paragraph(style=style_name)

        # 清除首行缩进（代码块不需要首行缩进）
        pPr = para._element.get_or_add_pPr()
        ind = pPr.find(qn('w:ind'))
        if ind is not None:
            pPr.remove(ind)

        # 设置左缩进
        if left_indent_cm > 0:
            from docx.shared import Cm
            ind = OxmlElement('w:ind')
            ind.set(qn('w:left'), str(int(left_indent_cm * 360)))  # cm -> twips (1cm ≈ 360 twips)
            pPr.append(ind)

        # 设置段落背景色
        if bg_color:
            color = bg_color.lstrip('#')
            shading = OxmlElement('w:shd')
            shading.set(qn('w:val'), 'clear')
            shading.set(qn('w:color'), 'auto')
            shading.set(qn('w:fill'), color)
            pPr.append(shading)

        # 添加文本 run（保留原始空格和缩进）
        if text:
            run = para.add_run(text)
            # 确保不自动压缩空格
            rPr = run._element.get_or_add_rPr()
            # 设置 w:specVanish 为 false 确保空格保留
            # 设置 w:space preserve 属性
            run._element.set(qn('xml:space'), 'preserve')
