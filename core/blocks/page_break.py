"""
分页块处理器 - 支持 page / column / line 三种类型
"""
from docx.enum.text import WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from .base import BlockHandler
from ..parser import PageBreakBlock

# page-break 的合法 break_type
_PAGE_BREAK_TYPES = {"page", "column", "line"}


class PageBreakHandler(BlockHandler):
    """分页块处理器"""

    def can_handle(self, block) -> bool:
        return isinstance(block, PageBreakBlock)

    def handle(self, block: PageBreakBlock):
        """处理分页块"""
        break_type = block.break_type

        # 校验合法值
        if break_type not in _PAGE_BREAK_TYPES:
            raise ValueError(
                f"page-break: 无效的 break_type '{break_type}'，"
                f"可选值: {', '.join(sorted(_PAGE_BREAK_TYPES))}"
            )

        para = self.doc.add_paragraph()

        if break_type == "line":
            # 行内换行：w:br w:type="textWrapping"
            self._add_br(para, "textWrapping")
        else:
            # page / column：w:br w:type="page" 或 w:br w:type="column"
            self._add_br(para, break_type)

        return para

    @staticmethod
    def _add_br(para, br_type: str):
        """向段落添加 w:br 元素"""
        run = para.add_run()
        br = OxmlElement('w:br')
        br.set(qn('w:type'), br_type)
        run._element.append(br)
