"""
边框工具 - 处理表格边框
"""
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class BorderHelper:
    """表格边框辅助类"""

    @staticmethod
    def set_table_no_border(table):
        """移除表格所有边框"""
        tbl = table._element
        tblPr = tbl.tblPr

        tblBorders = OxmlElement('w:tblBorders')

        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            element = OxmlElement(f'w:{edge}')
            element.set(qn('w:val'), 'nil')
            tblBorders.append(element)

        tblPr.append(tblBorders)

    @staticmethod
    def set_cell_border(cell, **kwargs):
        """
        设置单元格边框
        kwargs: top, bottom, left, right 等，值为 "single" 或 "nil"
        """
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

    @staticmethod
    def apply_table_borders(table, border_style: str):
        """
        应用表格边框样式
        border_style: "none", "grid", "three_line"
        """
        BorderHelper.set_table_no_border(table)

        if border_style == "none":
            return

        if border_style == "grid":
            for row in table.rows:
                for cell in row.cells:
                    BorderHelper.set_cell_border(
                        cell,
                        top="single",
                        bottom="single",
                        left="single",
                        right="single"
                    )
            return

        # three_line style
        rows = len(table.rows)
        if rows >= 1:
            for cell in table.rows[0].cells:
                BorderHelper.set_cell_border(cell, top="single", bottom="single", left="nil", right="nil")

            for i in range(1, rows):
                for cell in table.rows[i].cells:
                    BorderHelper.set_cell_border(cell, left="nil", right="nil")

            if rows >= 2:
                for cell in table.rows[-1].cells:
                    BorderHelper.set_cell_border(cell, bottom="single", left="nil", right="nil")
