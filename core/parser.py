"""
JSON 解析器 - 解析内容文件
"""
import json
from pathlib import Path
from typing import List, Dict, Any


class Block:
    """内容块基类"""

    def __init__(self, block_type: str, style: str = None, raw_data: dict = None):
        self.type = block_type
        self.style = style or ""
        self.raw_data = raw_data or {}

    def __repr__(self):
        return f"Block(type={self.type}, style={self.style})"


class TextBlock(Block):
    """文本块"""

    def __init__(self, style: str = None, runs: List[Dict] = None, raw_data: dict = None):
        super().__init__("text", style, raw_data)
        self.runs = runs or []


class ImageBlock(Block):
    """图片块"""

    def __init__(self, style: str = None, src: str = "", raw_data: dict = None):
        super().__init__("image", style, raw_data)
        self.src = src


class TableBlock(Block):
    """表格块"""

    def __init__(self, style: str = None, rows: int = 0, cols: int = 0,
                 cells: List[List] = None, header_style: str = None,
                 body_style: str = None, border: str = "three_line",
                 space_after: Dict = None, raw_data: dict = None):
        super().__init__("table", style, raw_data)
        self.rows = rows
        self.cols = cols
        self.cells = cells or []
        self.header_style = header_style or "default_style_text"
        self.body_style = body_style or "default_style_text"
        self.border = border or "three_line"
        self.space_after = space_after or {"units": "pt", "value": 12}


class HeadingBlock(Block):
    """标题块"""

    def __init__(self, level: int = 1, block_id: str = None, style: str = None,
                 runs: List[Dict] = None, raw_data: dict = None):
        super().__init__("heading", style, raw_data)
        self.level = level
        self.id = block_id or ""
        self.runs = runs or []


class TocBlock(Block):
    """目录块"""

    def __init__(self, levels: List[int] = None,
                 style_level_one: str = None,
                 style_level_two: str = None,
                 style_level_three: str = None,
                 raw_data: dict = None):
        super().__init__("toc", None, raw_data)
        self.levels = levels or [1, 2, 3]
        self.style_level_one = style_level_one
        self.style_level_two = style_level_two
        self.style_level_three = style_level_three


class PageBreakBlock(Block):
    """分页块"""

    def __init__(self, raw_data: dict = None):
        super().__init__("page-break", None, raw_data)


class ContentParser:
    """内容解析器，将JSON解析为Block对象"""

    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self.base_dir = self.json_path.parent.resolve()
        self.data = self._load_json()

    def _load_json(self) -> dict:
        """加载JSON文件"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse(self) -> List[Block]:
        """解析所有blocks"""
        blocks_data = self.data.get("blocks", [])
        return [self._parse_block(block_data) for block_data in blocks_data]

    def _parse_block(self, block_data: dict) -> Block:
        """解析单个block"""
        block_type = block_data.get("type", "text")

        parsers = {
            "text": self._parse_text_block,
            "heading": self._parse_heading_block,
            "image": self._parse_image_block,
            "table": self._parse_table_block,
            "toc": self._parse_toc_block,
            "page-break": self._parse_page_break_block,
        }

        parser = parsers.get(block_type, self._parse_text_block)
        return parser(block_data)

    def _parse_text_block(self, data: dict) -> TextBlock:
        """解析文本块"""
        return TextBlock(
            style=data.get("style"),
            runs=data.get("runs", []),
            raw_data=data
        )

    def _parse_heading_block(self, data: dict) -> HeadingBlock:
        """解析标题块"""
        return HeadingBlock(
            level=data.get("level", 1),
            block_id=data.get("id"),
            style=data.get("style"),
            runs=data.get("runs", []),
            raw_data=data
        )

    def _parse_image_block(self, data: dict) -> ImageBlock:
        """解析图片块"""
        return ImageBlock(
            style=data.get("style"),
            src=data.get("src", ""),
            raw_data=data
        )

    def _parse_table_block(self, data: dict) -> TableBlock:
        """解析表格块"""
        return TableBlock(
            style=data.get("style"),
            rows=data.get("rows", 0),
            cols=data.get("cols", 0),
            cells=data.get("cells", []),
            header_style=data.get("header_style", "default_style_text"),
            body_style=data.get("body_style", "default_style_text"),
            border=data.get("border", "three_line"),
            space_after=data.get("space_after", {"units": "pt", "value": 12}),
            raw_data=data
        )

    def _parse_toc_block(self, data: dict) -> TocBlock:
        """解析目录块"""
        return TocBlock(
            levels=data.get("levels", [1, 2, 3]),
            style_level_one=data.get("style_level_one"),
            style_level_two=data.get("style_level_two"),
            style_level_three=data.get("style_level_three"),
            raw_data=data
        )

    def _parse_page_break_block(self, data: dict) -> PageBreakBlock:
        """解析分页块"""
        return PageBreakBlock(raw_data=data)

    def get_base_dir(self) -> Path:
        """获取基础目录（用于解析相对路径）"""
        return self.base_dir
