from pypdf import PdfReader

def check_boxes(path):
    reader = PdfReader(path)
    page = reader.pages[0]
    print(f"MediaBox: {page.mediabox}")
    print(f"CropBox: {page.cropbox}")
    print(f"ArtBox: {page.artbox}")
    print(f"BleedBox: {page.bleedbox}")
    print(f"TrimBox: {page.trimbox}")

if __name__ == "__main__":
    check_boxes("OCR_第１号様式_記入済み.pdf")
