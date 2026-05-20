import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
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
            # 设置字体
            font_name = style.get("font_name", "Times New Roman")
            font_name_east_asia = style.get("font_name_east_asia", "宋体")
            para_style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            para_style.font.name = font_name
            para_style.font.name_east_asia = font_name_east_asia
            rFonts = para_style.font.element.rPr.rFonts
            rFonts.set(qn('w:eastAsia'), font_name_east_asia)
            # 设置字体大小
            font_size = style.get("font_size", 12)
            para_style.font.size = Pt(font_size)
            # 设置加粗
            bold = style.get("bold", False)
            para_style.font.bold = bold
            # 设置对齐方式
            alignment = style.get("alignment", "left")
            para_style.paragraph_format.alignment = self._get_alignment(alignment)
            # 设置字体颜色
            para_style.font.color.rgb = RGBColor(0, 0, 0)

            # 设置段前间距
            if style.get("space_before"):
                space_before = style["space_before"]
                units = space_before.get("units", "pt")
                value = space_before.get("value", 0)
                if units == "line":
                    para_style.paragraph_format.space_before = Pt(value * 12)  # 1行≈12磅
                else:
                    para_style.paragraph_format.space_before = Pt(value)
            else:
                para_style.paragraph_format.space_before = Pt(0)


            # 设置段后间距
            if style.get("space_after"):
                space_after = style["space_after"]
                units = space_after.get("units", "pt")
                value = space_after.get("value", 0)
                if units == "line":
                    para_style.paragraph_format.space_after = Pt(value * 12)  # 1行≈12磅
                else:
                    para_style.paragraph_format.space_after = Pt(value)
            else:
                para_style.paragraph_format.space_after = Pt(0)
            
            # 设置首行缩进
            if style.get("firstLineChars"):
                pPr = para_style.element.get_or_add_pPr()
                ind = OxmlElement('w:ind')
                ind.set(qn('w:firstLineChars'), str(int(style["firstLineChars"])))
                pPr.append(ind)


            # 设置行高
            if style.get("line_spacing"):
                line_spacing = style["line_spacing"]
                units = line_spacing.get("units", "line")
                value = line_spacing.get("value", 1.0)
                if units == "pt":
                    para_style.paragraph_format.line_spacing = Pt(value)
                    para_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                else:
                    para_style.paragraph_format.line_spacing = value



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
            space_before = style["space_before"]
            units = space_before.get("units", "pt")
            value = space_before.get("value", 0)
            if units == "line":
                para.paragraph_format.space_before = Pt(value * 12)
            else:
                para.paragraph_format.space_before = Pt(value)
        if style.get("space_after"):
            space_after = style["space_after"]
            units = space_after.get("units", "pt")
            value = space_after.get("value", 0)
            if units == "line":
                para.paragraph_format.space_after = Pt(value * 12)
            else:
                para.paragraph_format.space_after = Pt(value)

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

        text = text.replace('\n', '').replace('\r', '')
        rows_data = text.split("|")
        
        for i in range(min(rows, len(rows_data))):
            cells = rows_data[i].split(";")
            for j in range(min(cols, len(cells))):
                cell = table.cell(i, j)
                cell.text = cells[j].strip()
                cell_style = "表头" if i == 0 else "表内文字"
                if cell_style in self.styles:
                    for para in cell.paragraphs:
                        para.style = cell_style
                        para.paragraph_format.left_indent = 0
                        para.paragraph_format.first_line_indent = 0
                        para.paragraph_format.hanging_indent = 0

        para = self.doc.add_paragraph()
        if style.get("space_after"):
            space_after = style["space_after"]
            units = space_after.get("units", "pt")
            value = space_after.get("value", 0)
            if units == "line":
                para.paragraph_format.space_after = Pt(value * 12)
            else:
                para.paragraph_format.space_after = Pt(value)


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
        print("用法: python converter.py <xml文件路径> [输出docx路径] [style.json路径]")
        print("示例: python converter.py input.xml output.docx my_style.json")
        return

    xml_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    style_path = sys.argv[3] if len(sys.argv) > 3 else str(Path(__file__).parent / "style.json")

    converter = XML2DOCXConverter(style_path)
    converter.convert(xml_path, output_path)


if __name__ == "__main__":
    main()
