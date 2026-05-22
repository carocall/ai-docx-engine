"""
间距工具 - 处理段落间距
"""
from docx.shared import Pt


class SpacingHelper:
    """间距辅助类"""

    @staticmethod
    def set_spacing(paragraph_format, attr_name: str, spacing_config: dict):
        """
        设置段落间距
        attr_name: "space_before" 或 "space_after"
        spacing_config: {"units": "pt"|"line", "value": number}
        """
        if spacing_config:
            units = spacing_config.get("units", "pt")
            value = spacing_config.get("value", 0)
            if units == "line":
                setattr(paragraph_format, attr_name, Pt(value * 12))  # 1行≈12磅
            else:
                setattr(paragraph_format, attr_name, Pt(value))
        else:
            setattr(paragraph_format, attr_name, Pt(0))

    @staticmethod
    def get_pt_value(spacing_config: dict, default: int = 0) -> Pt:
        """获取磅值"""
        if not spacing_config:
            return Pt(default)
        units = spacing_config.get("units", "pt")
        value = spacing_config.get("value", default)
        if units == "line":
            return Pt(value * 12)
        return Pt(value)
