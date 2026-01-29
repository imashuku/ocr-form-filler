import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf_utils import embed_text_to_pdf

# テスト用のダミーPDFを作成する関数
def create_dummy_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 20)
    c.drawString(100, 700, "Original PDF Content")
    c.drawString(100, 600, "Name Field: ____________________")
    c.drawString(100, 500, "Chassis No: ____________________")
    c.save()
    print(f"ダミーPDFを作成しました: {filename}")

def main():
    # ファイルパスの設定
    input_pdf = "sample_form.pdf"
    output_pdf = "completed_form.pdf"

    # まだPDFがない場合は作成する
    if not os.path.exists(input_pdf):
        create_dummy_pdf(input_pdf)

    # 埋め込むデータの定義
    # 座標 (x, y) は左下が原点のポイント単位です (1ポイント = 1/72インチ)
    # 調整しながら正しい位置を見つけてください
    input_data = [
        {
            "text": "山田 太郎",   # 日本語名
            "x": 230,              # X座標
            "y": 600,              # Y座標 (「Name Field: ...」の線のあたり)
            "font_size": 14
        },
        {
            "text": "ABC-1234567", # 車体番号
            "x": 230,
            "y": 500,
            "font_size": 14
        }
    ]

    print("PDFへの書き込みを開始します...")
    
    # 関数を呼び出して実行
    success = embed_text_to_pdf(input_pdf, output_pdf, input_data)

    if success:
        print("完了しました。出力ファイルを確認してください。")

if __name__ == "__main__":
    main()
