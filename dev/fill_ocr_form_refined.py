import os
from pdf_utils import embed_text_to_pdf

def fill_ocr_form_refined():
    input_pdf = "OCR_第１号様式_記入済み.pdf"
    output_pdf = "OCR_BestGuess.pdf"

    # 補正値 (画像の確認結果から推測)
    # 高さ方向 (Storage X): +7 (前回+8からさらに1下げて微調整)
    offset_vert = 7
    
    # 横方向 (Storage Y): -3 (0から右に3戻す)
    offset_horiz = -3

    # ユーザー基準座標
    user_data = [
        {"text": "名", "user_x": 805, "user_y": 439},
        {"text": "古", "user_x": 774, "user_y": 439},
        {"text": "屋", "user_x": 742, "user_y": 439},
    ]

    pdf_fields = []
    for item in user_data:
        # 変換ロジック: StorageX=UserY, StorageY=UserX
        # 補正を適用
        storage_x = item["user_y"] + offset_vert
        storage_y = item["user_x"] + offset_horiz
        
        pdf_fields.append({
            "text": item["text"],
            "x": storage_x,
            "y": storage_y,
            "font_size": 20,
            "rotate": 270 # 文字回転
        })

    print(f"書き込みデータ(補正後): {pdf_fields}")

    # ERROR FIX: Default was set to 'letter' (height 792), cliping text at Y=805.
    # Must use actual page size (595, 836)
    embed_text_to_pdf(input_pdf, output_pdf, pdf_fields, pagesize=(595, 836))

if __name__ == "__main__":
    fill_ocr_form_refined()
