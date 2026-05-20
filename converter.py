import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class XML2DOCXConverter:
    def __init__(self, style_path):
        with open(style_path, 'r', encoding='utf-8') as f:
            self.styles = json.load(f)
        self.doc = Document()
        self._register_styles()

    def _register_styles(self):
        for tag, style in self.styles.items():
            if style.get("type") == "horizontal":
                continue

            style_name = tag
            if style_name in [s.name for s in self.doc.styles]:
                continue

            font_name = style.get("font_name", "宋体")
            font_size = style.get("font_size", 12)
            bold = style.get("bold", False)
            alignment = style.get("alignment", "left")

            para_style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            para_style.font.name = font_name
            para_style.font.size = Pt(font_size)
            para_style.font.bold = bold
            para_style.font.color.rgb = RGBColor(0, 0, 0)

            para_style.paragraph_format.alignment = self._get_alignment(alignment)
            if style.get("space_before"):
                para_style.paragraph_format.space_before = Pt(style["space_before"])
            if style.get("space_after"):
                para_style.paragraph_format.space_after = Pt(style["space_after"])

    def convert(self, xml_path, output_path=None):
        self.xml_dir = str(Path(xml_path).parent.resolve())
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for element in root:
            tag_name = element.tag
            text = element.text or ''
            attrs = element.attrib

            self._process_element(tag_name, text, attrs)

        if output_path is None:
            output_path = str(Path(xml_path).with_suffix('.docx'))
        self.doc.save(output_path)
        print(f"文档已生成: {output_path}")

    def _process_element(self, tag, text, attrs):
        if tag not in self.styles:
            print(f"警告: 未知标签 '{tag}'，将作为正文处理")
            tag = "正文"

        style = self.styles[tag]

        if style.get("type") == "horizontal":
            self._add_horizontal_line()
            return

        if tag == "图片":
            self._add_image(text, style)
        elif tag == "表格":
            self._add_table(text, style, attrs)
        else:
            self._add_paragraph(tag, text, style)

    def _add_paragraph(self, tag, text, style):
        para = self.doc.add_paragraph(style=tag)
        para.add_run(text)
        return para

    def _add_image(self, url, style):
        para = self.doc.add_paragraph()
        para.alignment = self._get_alignment(style.get("alignment", "center"))

        if style.get("space_before"):
            para.paragraph_format.space_before = Pt(style["space_before"])
        if style.get("space_after"):
            para.paragraph_format.space_after = Pt(style["space_after"])

        img_path = url
        if not Path(url).is_absolute():
            img_path = str(Path(self.xml_dir) / url)

        try:
            para.add_run().add_picture(img_path, width=Cm(10))
        except Exception as e:
            para.add_run(f"[图片加载失败: {url}]")

    def _add_table(self, text, style, attrs):
        rows = int(attrs.get("rows", 0))
        cols = int(attrs.get("cols", 0))

        if rows <= 0 or cols <= 0:
            return

        table = self.doc.add_table(rows=rows, cols=cols)
        table.style = 'Table Grid'

        cells = text.split(";")
        idx = 0
        for i in range(rows):
            for j in range(cols):
                if idx < len(cells):
                    cell = table.cell(i, j)
                    cell.text = cells[idx].strip()
                    cell_style = "表头" if i == 0 else "表内文字"
                    if cell_style in self.styles:
                        for para in cell.paragraphs:
                            para.style = cell_style
                    idx += 1

        para = self.doc.add_paragraph()
        if style.get("space_after"):
            para.paragraph_format.space_after = Pt(style["space_after"])

    def _add_horizontal_line(self):
        para = self.doc.add_paragraph()
        pPr = para._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), 'auto')
        pBdr.append(bottom)
        pPr.append(pBdr)

    def _get_alignment(self, align_str):
        mapping = {
            "left": WD_ALIGN_PARAGRAPH.LEFT,
            "center": WD_ALIGN_PARAGRAPH.CENTER,
            "right": WD_ALIGN_PARAGRAPH.RIGHT,
            "justify": WD_ALIGN_PARAGRAPH.JUSTIFY
        }
        return mapping.get(align_str, WD_ALIGN_PARAGRAPH.LEFT)


def main():
    if len(sys.argv) < 2:
        print("用法: python converter.py <xml文件路径> [输出docx路径]")
        print("示例: python converter.py input.xml output.docx")
        return

    xml_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    style_path = Path(__file__).parent / "style.json"
    converter = XML2DOCXConverter(style_path)
    converter.convert(xml_path, output_path)


if __name__ == "__main__":
    main()
