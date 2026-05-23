"""
JSON to DOCX 转换器 - CLI入口（严格模式）
"""
import sys
from pathlib import Path

from .renderer import DocxRenderer
from .styles import StyleNotFoundError


def print_usage():
    """打印使用说明"""
    print("用法: python -m core.converter <json文件路径> <style.json路径> <输出docx路径>")
    print("示例: python -m core.converter input.json style.json output.docx")


def validate_file(path: str, file_type: str) -> Path:
    """验证文件路径"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{file_type} 文件不存在: {path}")
    return p


def main():
    # 强制要求三个参数
    if len(sys.argv) < 4:
        print("错误: 缺少必要参数")
        print_usage()
        sys.exit(1)

    json_path = sys.argv[1]
    style_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        # 验证输入文件存在
        validate_file(json_path, "JSON内容")
        validate_file(style_path, "样式")

        # 创建渲染器并渲染
        renderer = DocxRenderer(style_path)
        result_path = renderer.render_file(json_path, output_path)
        print(f"文档已生成: {result_path}")

    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except StyleNotFoundError as e:
        print(f"样式错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"转换失败: {e}")
        raise


if __name__ == "__main__":
    main()
