import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def create_tuning_pdf(input_pdf, output_pdf):
    # Base: Na(439, 805), Ko(439, 774)
    # User feedback: "Too Low" (Visual Down) -> Need Visual Up (Storage +X)
    # User feedback: "Na Gone" -> Need Visual Right? (Storage -Y) or just Fix Clipping
    
    reader = PdfReader(input_pdf)
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont('HeiseiMin-W3', 10)
    
    # Tuning "Ko" (Height Adjustment)
    # Current X=439 (Too Low). Try increasing X.
    base_x = 439
    base_y_ko = 774
    
    for offset_x in [0, 10, 20, 30, 40]:
        test_x = base_x + offset_x
        
        can.saveState()
        can.translate(test_x, base_y_ko)
        can.rotate(270)
        
        # Draw "Ko" and the X value
        can.setFillColorRGB(1, 0, 0) # Red
        can.drawString(0, 0, f"古(+{offset_x})")
        can.rect(0, -2, 30, 30, stroke=1, fill=0) # Box approx
        can.restoreState()

    # Tuning "Na" (Y Adjustment)
    # Current Y=805 (Gone). Try decreasing Y (Visual Right).
    base_y_na = 805
    # Use X offset of +30 as a guess for visibility if X was the issue too
    test_x_na = base_x + 30 
    
    for offset_y in [0, -5, -10, -15, -20]:
        test_y = base_y_na + offset_y
        
        can.saveState()
        can.translate(test_x_na, test_y)
        can.rotate(270)
        
        can.setFillColorRGB(0, 0, 1) # Blue
        can.drawString(0, 0, f"名({offset_y})")
        can.restoreState()

    can.save()
    packet.seek(0)
    
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]
    
    writer = PdfWriter()
    page.merge_page(overlay_page)
    writer.add_page(page)
    
    with open(output_pdf, "wb") as f:
        writer.write(f)
    print(f"Created tuning file: {output_pdf}")

if __name__ == "__main__":
    create_tuning_pdf("OCR_第１号様式_記入済み.pdf", "OCR_tuning.pdf")
