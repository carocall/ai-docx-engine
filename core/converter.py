"""
JSON to DOCX 转换器
主入口文件，负责命令行参数处理和调用核心模块
"""
import sys
from pathlib import Path

from .renderer import DocxRenderer


def main():
    if len(sys.argv) < 2:
        print("用法: python -m core.converter <json文件路径> [输出docx路径] [style.json路径]")
        print("示例: python -m core.converter input.json output.docx my_style.json")
        return

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    style_path = sys.argv[3] if len(sys.argv) > 3 else str(Path(__file__).parent.parent / "style.json")

    try:
        renderer = DocxRenderer(style_path)
        result_path = renderer.render_file(json_path, output_path)
        print(f"文档已生成: {result_path}")
    except Exception as e:
        print(f"转换失败: {e}")
        raise


if __name__ == "__main__":
    main()
