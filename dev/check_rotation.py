from pypdf import PdfReader

def check_rotation(path):
    reader = PdfReader(path)
    page = reader.pages[0]
    print(f"Page Rotation: {page.get('/Rotate', 0)}")
    print(f"MediaBox: {page.mediabox}")

if __name__ == "__main__":
    check_rotation("OCR_第１号様式_記入済み.pdf")
