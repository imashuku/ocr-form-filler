import os
from pdf_utils import embed_text_to_pdf

def fill_ocr_form():
    input_pdf = "OCR_第１号様式_記入済み.pdf"
    output_pdf = "OCR_Filled_Final.pdf"

    # ユーザーが計測した「見た目の座標 (横向き)」
    # 座標: [名: (805, 439), 古: (774, 439), 屋: (742, 439)]
    # 高さ30、幅30 とのことですが、まずは始点を合わせます。
    user_data = [
        {"text": "名", "user_x": 805, "user_y": 439},
        {"text": "古", "user_x": 774, "user_y": 439},
        {"text": "屋", "user_x": 742, "user_y": 439},
    ]

    # 変換ロジック
    # PDFは縦向き(Portrait)で保存され、270度回転表示されている。
    # 検証結果: StorageX = UserY, StorageY = UserX
    # 文字回転: 270度
    
    pdf_fields = []
    for item in user_data:
        # 座標変換
        storage_x = item["user_y"]
        storage_y = item["user_x"]
        
        # 微調整 (キャリブレーション結果を見て、必要ならここを直す)
        # "名"の丸がぴったりだったので、補正なしでいく
        
        pdf_fields.append({
            "text": item["text"],
            "x": storage_x,
            "y": storage_y,
            "font_size": 20,       # 枠に合わせて少し大きめに
            "rotate": 270          # 確認済みの角度
        })

    print(f"変換後の書き込みデータ: {pdf_fields}")

    embed_text_to_pdf(input_pdf, output_pdf, pdf_fields)

if __name__ == "__main__":
    fill_ocr_form()
