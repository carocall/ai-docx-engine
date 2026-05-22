"""
DOCX 渲染器 - 将 Block 对象渲染为 Word 文档
"""
from docx import Document
from pathlib import Path
from typing import List

from .styles import StyleEngine
from .parser import Block, ContentParser
from .blocks import TextHandler, HeadingHandler, ImageHandler, TableHandler, TocHandler, PageBreakHandler


class DocxRenderer:
    """DOCX渲染器"""

    def __init__(self, style_path: str = None):
        self.doc = Document()
        self.style_engine = StyleEngine(self.doc, style_path)
        self.handlers = []
        self.base_dir = ""

    def setup_handlers(self, base_dir: str):
        """设置处理器链"""
        self.base_dir = base_dir
        self.handlers = [
            TocHandler(self.doc, self.style_engine, base_dir),
            HeadingHandler(self.doc, self.style_engine, base_dir),
            TextHandler(self.doc, self.style_engine, base_dir),
            ImageHandler(self.doc, self.style_engine, base_dir),
            TableHandler(self.doc, self.style_engine, base_dir),
            PageBreakHandler(self.doc, self.style_engine, base_dir),
        ]

    def render(self, blocks: List[Block], output_path: str):
        """渲染所有blocks到Word文档"""
        for block in blocks:
            self._render_block(block)

        self.doc.save(output_path)

    def _render_block(self, block: Block):
        """渲染单个block"""
        for handler in self.handlers:
            if handler.can_handle(block):
                handler.handle(block)
                return

        print(f"警告: 未找到处理 '{block.type}' 类型的处理器")

    def render_file(self, json_path: str, output_path: str = None):
        """
        从JSON文件渲染Word文档
        便捷方法，一次性完成解析和渲染
        """
        json_path = Path(json_path)

        if output_path is None:
            output_path = str(json_path.with_suffix('.docx'))

        # 解析
        parser = ContentParser(str(json_path))
        blocks = parser.parse()

        # 设置处理器
        self.setup_handlers(str(parser.get_base_dir()))

        # 渲染
        self.render(blocks, output_path)

        return output_path
