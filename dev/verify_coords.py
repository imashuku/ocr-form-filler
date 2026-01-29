import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter

# Register Font
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def verify_coordinates(input_pdf, output_pdf):
    # Based on deduction: User X = Stored Y, User Y = Stored X.
    # And the page is stored as Portrait (595x836) but rotated 270.
    
    # We create a PORTRAIT overlay (595x836)
    # Note: 836 points is roughly 11.6 inches. 595 is 8.27 inches. (A4)
    # Let's use the explicit size verification from the input PDF
    reader = PdfReader(input_pdf)
    page = reader.pages[0]
    width = float(page.mediabox.width)  # 595
    height = float(page.mediabox.height) # 836
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont('HeiseiMin-W3', 12)
    can.setFillColorRGB(1, 0, 0) # Red color for visibility

    # Test Case 1: "Mei" (名)
    # User said: X=805 -> Stored Y=805
    # User said: Y=439 -> Stored X=439
    can.drawString(439, 805, "名(Check)")
    can.circle(439, 805, 5, stroke=1, fill=0)

    # Test Case 2: "Ko" (古)
    # X=774 -> Y=774
    can.drawString(439, 774, "古(Check)")

    # Test Case 3: "Ya" (屋)
    # X=742 -> Y=742
    can.drawString(439, 742, "屋(Check)")
    
    can.save()
    packet.seek(0)
    
    # Merge
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]
    
    writer = PdfWriter()
    page.merge_page(overlay_page)
    # Note: merge_page preserves the original page's rotation
    writer.add_page(page)
    
    with open(output_pdf, "wb") as f:
        writer.write(f)
    print(f"Saved verification file: {output_pdf}")

if __name__ == "__main__":
    verify_coordinates("OCR_第１号様式_記入済み.pdf", "OCR_verify_coords.pdf")
