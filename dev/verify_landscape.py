import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter, PageObject, Transformation

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def verify_landscape_coords(input_pdf, output_pdf):
    # A4 Landscape: ~842 x 595 points
    # User coordinates: X=805, Y=439 (Likely Landscape Bottom-Left Origin)

    packet = io.BytesIO()
    # Create Landscape Canvas
    can = canvas.Canvas(packet, pagesize=landscape(A4))
    can.setFont('HeiseiMin-W3', 20)
    can.setFillColorRGB(1, 0, 0) # Red

    # Plot User Coordinates exactly
    # Na (名)
    can.drawString(805, 439, "名")
    can.circle(805 + 15, 439 + 15, 15, stroke=1, fill=0) # Circle the 30x30 box area

    # Ko (古)
    can.drawString(774, 439, "古")
    
    # Ya (屋)
    can.drawString(742, 439, "屋")

    can.save()
    packet.seek(0)
    
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0] # This is 842x595
    
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    source_page = reader.pages[0]
    
    # Check rotation to decide strategy
    # If source is rotated 270, and we want to overlay 'Landscape' content...
    # We might need to rotate our overlay to match the storage, OR just merge.
    # Trying simple merge first, but considering pypdf behavior.
    # If we merge a Landscape page onto a Portrait(Rotated) page,
    # pypdf usually aligns (0,0).
    
    # Let's try explicit merge with no manual rotation first, 
    # as ReportLab landscape == Visual Landscape usually.
    source_page.merge_page(overlay_page)
    
    writer.add_page(source_page)
    
    with open(output_pdf, "wb") as f:
        writer.write(f)
    print(f"Created: {output_pdf}")

if __name__ == "__main__":
    verify_landscape_coords("OCR_第１号様式_記入済み.pdf", "OCR_verify_landscape.pdf")
