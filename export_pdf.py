from fpdf import FPDF
from PySide6.QtWidgets import QTableWidget

def truncate_text(pdf: FPDF, text: str, col_width: float):
    max_width = col_width - 2  
    if pdf.get_string_width(text) > max_width:
        while pdf.get_string_width(text + "...") > max_width and len(text) > 0:
            text = text[:-1]  
        return text + "..."
    return text

def export_to_pdf(table: QTableWidget, filename: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font('Arial', '', 'arial.ttf', uni=True)
    pdf.set_font('Arial', '', 12)

    
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    
    num_columns = table.columnCount()

    
    col_width = page_width / num_columns

    
    for col in range(num_columns):
        header_text = table.horizontalHeaderItem(col).text() if table.horizontalHeaderItem(col) else ""
        truncated_header = truncate_text(pdf, header_text, col_width)
        pdf.cell(col_width, 10, truncated_header, border=1, align='C')
    pdf.ln()

    
    for row in range(table.rowCount()):
        for col in range(num_columns):
            cell_text = table.item(row, col).text() if table.item(row, col) else ""
            truncated_text = truncate_text(pdf, cell_text, col_width)
            pdf.cell(col_width, 10, truncated_text, border=1, align='C')
        pdf.ln()

    
    pdf.output(filename)
    print(f"Exported to '{filename}'.")
