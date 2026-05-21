import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class XML2DOCXConverter:
    def __init__(self, style_path):
        self.default_style_names = {
            "p": "default_style_p",
            "image": "default_style_image",
            "table": "default_style_table"
        }
        default_style_path = Path(__file__).parent / "default_style.json"
        self.default_styles = self._load_styles(default_style_path)
        user_styles = self._load_styles(style_path)
        self.styles = self._merge_styles(self.default_styles, user_styles)
        self.doc = Document()
        self._register_styles()

    def _load_styles(self, style_path):
        if not style_path:
            return {}
        style_path = Path(style_path)
        if not style_path.exists():
            return {}
        with open(style_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _merge_styles(self, base_styles, override_styles):
        styles = {name: value.copy() for name, value in base_styles.items()}
        for name, override in override_styles.items():
            if name in styles and isinstance(styles[name], dict) and isinstance(override, dict):
                merged = styles[name].copy()
                merged.update(override)
                styles[name] = merged
            else:
                styles[name] = override
        return styles

    def _register_styles(self):
        for tag, style in self.styles.items():

            style_name = tag
            # 检查样式是否已存在
            if style_name in [s.name for s in self.doc.styles]:
                # 如果存在，获取已有的样式对象
                para_style = self.doc.styles[style_name]
            else:
                # 如果不存在，创建新样式
                para_style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            # 设置字体
            font_name = style.get("font_name", "Times New Roman")
            font_name_east_asia = style.get("font_name_east_asia", "宋体")
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
        if tag == "page-break":
            self._add_page_break()
            return

        if tag == "p":
            style_name, style = self._resolve_style("p", attrs)
            self._add_paragraph(style_name, text, style)
            return

        if tag == "image":
            style_name, style = self._resolve_style("image", attrs)
            self._add_image(attrs.get("src", text), style)
            return

        if tag == "table":
            style_name, style = self._resolve_style("table", attrs)
            self._add_table(text, style, attrs)
            return

        print(f"警告: 不支持的标签 '{tag}'，已跳过")

    def _resolve_style(self, element_type, attrs):
        default_style_name = self.default_style_names[element_type]
        requested_style_name = attrs.get("style")
        style_name = requested_style_name if requested_style_name in self.styles else default_style_name

        default_style = self.styles.get(default_style_name, {})
        style = default_style.copy()
        style.update(self.styles.get(style_name, {}))
        return style_name, style

    def _add_paragraph(self, tag, text, style):
        para = self.doc.add_paragraph(style=tag)
        para.add_run(text)
        return para

    def _add_page_break(self):
        para = self.doc.add_paragraph()
        para.add_run().add_break(WD_BREAK.PAGE)
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
            width_cm = style.get("width_cm", 10)
            para.add_run().add_picture(img_path, width=Cm(width_cm))
        except Exception as e:
            para.add_run(f"[图片加载失败: {url}]")

    def _set_table_no_border(self, table):
        tbl = table._element
        tblPr = tbl.tblPr

        tblBorders = OxmlElement('w:tblBorders')

        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            element = OxmlElement(f'w:{edge}')
            element.set(qn('w:val'), 'nil')
            tblBorders.append(element)

        tblPr.append(tblBorders)

    def _set_cell_border(self, cell, **kwargs):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')

        for edge, val in kwargs.items():
            element = OxmlElement(f'w:{edge}')
            element.set(qn('w:val'), val)
            element.set(qn('w:sz'), "12")
            element.set(qn('w:space'), "0")
            element.set(qn('w:color'), "000000")
            tcBorders.append(element)

        tcPr.append(tcBorders)

    def _apply_table_borders(self, table, border_style):
        self._set_table_no_border(table)

        if border_style == "none":
            return

        if border_style == "grid":
            for row in table.rows:
                for cell in row.cells:
                    self._set_cell_border(
                        cell,
                        top="single",
                        bottom="single",
                        left="single",
                        right="single"
                    )
            return

        rows = len(table.rows)
        if rows >= 1:
            for cell in table.rows[0].cells:
                self._set_cell_border(cell, top="single", bottom="single", left="nil", right="nil")

            for i in range(1, rows):
                for cell in table.rows[i].cells:
                    self._set_cell_border(cell, left="nil", right="nil")

            if rows >= 2:
                for cell in table.rows[-1].cells:
                    self._set_cell_border(cell, bottom="single", left="nil", right="nil")

    def _add_table(self, text, style, attrs):
        text = text.replace('\n', '').replace('\r', '')
        rows_data = [row for row in text.split("|") if row.strip()]
        inferred_rows = len(rows_data)
        inferred_cols = max((len(row.split(";")) for row in rows_data), default=0)

        rows = int(attrs.get("rows", inferred_rows))
        cols = int(attrs.get("cols", inferred_cols))

        if rows <= 0 or cols <= 0:
            return

        table = self.doc.add_table(rows=rows, cols=cols)
        header_style = style["header_style"]
        body_style = style["body_style"]
        
        for i in range(min(rows, len(rows_data))):
            cells = rows_data[i].split(";")
            for j in range(min(cols, len(cells))):
                cell = table.cell(i, j)
                cell.text = cells[j].strip()
                cell_style = header_style if i == 0 else body_style
                for para in cell.paragraphs:
                    para.style = cell_style
                    para.paragraph_format.left_indent = 0
                    para.paragraph_format.first_line_indent = 0
                    para.paragraph_format.hanging_indent = 0

        self._apply_table_borders(table, style["border"])

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
