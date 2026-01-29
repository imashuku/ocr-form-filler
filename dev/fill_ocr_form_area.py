import os
from pdf_utils import embed_text_to_pdf

def fill_with_area_name(area_name_str):
    input_pdf = "OCR_第１号様式_記入済み.pdf"
    # ファイル名にもエリア名を入れる
    output_pdf = f"OCR_{area_name_str}.pdf"

    # 確定した補正値
    # 高さ方向 (Storage X): +7
    offset_vert = 7
    # 横方向 (Storage Y): -3
    offset_horiz = -3

    # ボックスの基準座標 (User Coordinates)
    # 左から順に (X=805, X=774, X=742)
    # 4つ目のボックスは等間隔(約32pt)と仮定して X=710
    box_coords = [
        {"user_x": 805, "user_y": 439}, # Box 1 (Left)
        {"user_x": 774, "user_y": 439}, # Box 2 
        {"user_x": 742, "user_y": 439}, # Box 3 
        {"user_x": 710, "user_y": 439}, # Box 4 (Right)
    ]

    pdf_fields = []
    
    # 入力された文字列を、左のボックスから順に埋める
    # 文字数がボックス数より多い場合は切り捨て
    for i, char in enumerate(area_name_str):
        if i >= len(box_coords):
            break
            
        coords = box_coords[i]
        
        # 変換ロジック
        storage_x = coords["user_y"] + offset_vert
        storage_y = coords["user_x"] + offset_horiz
        
        pdf_fields.append({
            "text": char,
            "x": storage_x,
            "y": storage_y,
            "font_size": 20,
            "rotate": 270
        })

    print(f"Generating PDF for area_name='{area_name_str}'...")
    
    # 用紙サイズ (595, 836) を明示的に指定
    embed_text_to_pdf(input_pdf, output_pdf, pdf_fields, pagesize=(595, 836))

if __name__ == "__main__":
    # リクエスト: "尾張小牧"
    area_name = "尾張小牧"
    fill_with_area_name(area_name)
