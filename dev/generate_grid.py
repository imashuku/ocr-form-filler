import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader, PdfWriter

def create_grid_pdf(input_pdf_path, output_pdf_path):
    # Read the text PDF source to get size
    reader = PdfReader(input_pdf_path)
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    
    print(f"Generating grid for size: {width}x{height}")

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    
    # Draw Grid
    can.setFont("Helvetica", 8)
    can.setStrokeColor(colors.red)
    can.setFillColor(colors.red)
    
    # Draw vertical lines (X) every 50 points
    for x in range(0, int(width), 50):
        can.line(x, 0, x, height)
        can.drawString(x + 2, 10, str(x))
        can.drawString(x + 2, height - 20, str(x))

    # Draw horizontal lines (Y) every 50 points
    for y in range(0, int(height), 50):
        can.line(0, y, width, y)
        can.drawString(10, y + 2, str(y))
        can.drawString(width - 30, y + 2, str(y))

    # Draw finer grid lines (every 10 points) in light grey
    can.setStrokeColor(colors.lightgrey)
    for x in range(0, int(width), 10):
        if x % 50 != 0: can.line(x, 0, x, height)
    for y in range(0, int(height), 10):
        if y % 50 != 0: can.line(0, y, width, y)

    can.save()
    packet.seek(0)
    
    # Merge
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]
    
    writer = PdfWriter()
    page.merge_page(overlay_page)
    writer.add_page(page)
    
    with open(output_pdf_path, "wb") as f:
        writer.write(f)
    
    print(f"Grid overlay saved to: {output_pdf_path}")

if __name__ == "__main__":
    input_path = "OCR_第１号様式_記入済み.pdf"
    output_path = "OCR_check_grid.pdf"
    create_grid_pdf(input_path, output_path)
