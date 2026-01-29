from pypdf import PdfReader
import sys

def analyze_pdf(path):
    try:
        reader = PdfReader(path)
        print(f"File: {path}")
        print(f"Number of Pages: {len(reader.pages)}")
        
        if len(reader.pages) > 0:
            page = reader.pages[0]
            # Page dimension
            box = page.mediabox
            print(f"Page 1 Size: Width={box.width}, Height={box.height}")
            
            # Try extracting text
            text = page.extract_text()
            print("\n--- Extracted Text Preview (First 200 chars) ---")
            print(text[:200] if text else "(No text extracted)")
            print("-----------------------------------------------")
            
            return True
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return False

if __name__ == "__main__":
    path = "/Users/imashukuhiroaki/Antigravity/04_at-cars/re-start/OCR_第１号様式_記入済み.pdf"
    analyze_pdf(path)
