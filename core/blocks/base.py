"""
Block 处理器基类
"""
from abc import ABC, abstractmethod
from docx import Document
from ..styles import StyleEngine
from ..parser import Block


class BlockHandler(ABC):
    """Block处理器基类"""

    def __init__(self, doc: Document, style_engine: StyleEngine, base_dir: str):
        self.doc = doc
        self.style_engine = style_engine
        self.base_dir = base_dir

    @abstractmethod
    def can_handle(self, block: Block) -> bool:
        """判断是否处理该block"""
        pass

    @abstractmethod
    def handle(self, block: Block):
        """处理block"""
        pass
