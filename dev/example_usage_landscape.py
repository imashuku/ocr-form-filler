import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from pdf_utils import embed_text_to_pdf

# テスト用のダミーPDF (A4横向き) を作成する関数
def create_dummy_pdf_a4_landscape(filename):
    # landscape(A4) で横向きに設定
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    
    # A4横は約 842 x 595 ポイント
    width, height = landscape(A4)
    print(f"A4横向きサイズ: 幅={width}, 高さ={height}")
    
    c.setFont("Helvetica", 20)
    c.drawString(100, 500, "Landscape A4 Document")
    c.drawString(100, 400, "Project Name: ____________________")
    c.drawString(400, 400, "Date: ____________________")
    c.save()
    print(f"ダミーPDF(A4横)を作成しました: {filename}")

def main():
    # ファイルパスの設定
    input_pdf = "sample_form_landscape.pdf"
    output_pdf = "completed_form_landscape.pdf"

    # まだPDFがない場合は作成する
    if not os.path.exists(input_pdf):
        create_dummy_pdf_a4_landscape(input_pdf)

    # 埋め込むデータの定義
    input_data = [
        {
            "text": "新規プロジェクトA", 
            "x": 240,              
            "y": 400,              
            "font_size": 14
        },
        {
            "text": "2026/01/24", 
            "x": 460,
            "y": 400,
            "font_size": 14
        }
    ]

    print("A4横向きPDFへの書き込みを開始します...")
    
    # pagesize=landscape(A4) を指定するのがポイント
    success = embed_text_to_pdf(
        input_pdf, 
        output_pdf, 
        input_data, 
        pagesize=landscape(A4)
    )

    if success:
        print("完了しました。出力ファイルを確認してください。")

if __name__ == "__main__":
    main()
