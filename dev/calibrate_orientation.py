import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def create_calibration_pdf(input_pdf, output_pdf):
    # Storage dimensions (approx A4 Portrait)
    # Width ~595, Height ~836
    
    # User User Input: X=805, Y=439
    # Hypothesis:
    # Storage X = User Y = 439
    # Storage Y = User X = 805
    # Let's target this point (439, 805)
    
    sx = 439
    sy = 805
    
    reader = PdfReader(input_pdf)
    page = reader.pages[0]
    # Use exact media box
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont('HeiseiMin-W3', 14)
    
    # Draw a target circle
    can.setStrokeColorRGB(1, 0, 0)
    can.circle(sx, sy, 20, stroke=1, fill=0)
    
    # 0 Degrees (Normal in Storage)
    can.setFillColorRGB(1, 0, 0) # Red
    can.drawString(sx, sy, "0度(名)")
    
    # 90 Degrees
    can.saveState()
    can.translate(sx, sy)
    can.rotate(90)
    can.setFillColorRGB(0, 1, 0) # Green
    can.drawString(0, 0, "90度(名)")
    can.restoreState()

    # 180 Degrees
    can.saveState()
    can.translate(sx, sy)
    can.rotate(180)
    can.setFillColorRGB(0, 0, 1) # Blue
    can.drawString(0, 0, "180度(名)")
    can.restoreState()

    # 270 Degrees
    can.saveState()
    can.translate(sx, sy)
    can.rotate(270)
    can.setFillColorRGB(1, 0, 1) # Magenta
    can.drawString(0, 0, "270度(名)")
    can.restoreState()
    
    # Also test proper spacing for "Ko" (774) and "Ya" (742)
    # If X maps to Y.
    # Ko: sy = 774
    # Ya: sy = 742
    
    # Visual check using 270 degree text (Magenta) - Just a guess
    # (Since Page is 270, Text often needs 90 or 270 to align?)
    
    can.saveState()
    can.translate(sx, 774) # Ko
    can.rotate(90) # Try 90 for these
    can.setFillColorRGB(0, 0, 0)
    can.drawString(0, 0, "古(90?)")
    can.restoreState()

    can.saveState()
    can.translate(sx, 742) # Ya
    can.rotate(90)
    can.drawString(0, 0, "屋(90?)")
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
    print(f"Created calibration file: {output_pdf}")

if __name__ == "__main__":
    create_calibration_pdf("OCR_第１号様式_記入済み.pdf", "OCR_calibrate.pdf")
