"""
节分隔块处理器 - 支持 nextPage / continuous / evenPage / oddPage 四种类型
"""
from docx.enum.section import WD_SECTION_START
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from .base import BlockHandler
from ..parser import SectionBreakBlock

# section-break 的合法 break_type -> WD_SECTION_START 映射
_SECTION_BREAK_MAP = {
    "nextPage":   WD_SECTION_START.NEW_PAGE,
    "continuous": WD_SECTION_START.CONTINUOUS,
    "evenPage":   WD_SECTION_START.EVEN_PAGE,
    "oddPage":    WD_SECTION_START.ODD_PAGE,
}


class SectionBreakHandler(BlockHandler):
    """节分隔块处理器"""

    def can_handle(self, block) -> bool:
        return isinstance(block, SectionBreakBlock)

    def handle(self, block: SectionBreakBlock):
        """处理节分隔块"""
        break_type = block.break_type

        # 校验合法值
        if break_type not in _SECTION_BREAK_MAP:
            raise ValueError(
                f"section-break: 无效的 break_type '{break_type}'，"
                f"可选值: {', '.join(sorted(_SECTION_BREAK_MAP.keys()))}"
            )

        section_type = _SECTION_BREAK_MAP[break_type]

        # 在当前段落上附加 sectPr，实现节分隔
        # add_section 会在文档末尾追加一个新段落，该段落包含 sectPr
        new_section = self.doc.add_section(section_type)
        return new_section
