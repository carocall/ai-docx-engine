"""
分页块处理器
"""
from docx.enum.text import WD_BREAK

from .base import BlockHandler
from ..parser import PageBreakBlock


class PageBreakHandler(BlockHandler):
    """分页块处理器"""

    def can_handle(self, block) -> bool:
        return isinstance(block, PageBreakBlock)

    def handle(self, block: PageBreakBlock):
        """处理分页块"""
        para = self.doc.add_paragraph()
        para.add_run().add_break(WD_BREAK.PAGE)
        return para
