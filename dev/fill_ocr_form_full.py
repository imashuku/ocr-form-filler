import os
from pdf_utils import embed_text_to_pdf

# ==========================================
# 設定エリア (ここに教えてもらった値を入れます)
# ==========================================
# 共通補正値 (地域名で確定したもの)
OFFSET_VERT = 7   # User Y -> Storage X
OFFSET_HORIZ = -3 # User X -> Storage Y

# 1. 自動車登録番号（地域名） - 確定済み
# 基準: 名(805, 439), 古(774, 439), 屋(742, 439)...
AREA_NAME_START_X = 805
AREA_NAME_START_Y = 439
AREA_NAME_PITCH = 32 # およそ

# 2. 分類番号 (Class Number) - 3桁
CLASS_NUM_CONFIG = {
    # start_x: 674 -> 672 (中央の「3」を維持しつつ、ピッチを狭めて左右を寄せる)
    "start_x": 672, 
    # start_y: 441 -> 440 (全体に1pt下へ)
    "start_y": 440, 
    # pitch: 19 -> 17 (左右が広がっていたため狭める)
    "pitch": 17,    
}

# 3. かな (Kana) - 1文字
KANA_CONFIG = {
    "x": 611,
    "y": 439,
}

# 4. 一連指定番号 (Serial Number) - 4桁
SERIAL_NUM_CONFIG = {
    # start_x: 574 -> 572 (文字「1」が少し左寄りだったため、右へ2pt補正)
    "start_x": 572,
    # start_y: 441 -> 440 (全体に1pt下へ)
    "start_y": 440,
    # pitch: 16 -> 17 (狭すぎたため広げる。分類番号と同じピッチにする)
    "pitch": 17,    
}

# ==========================================

def get_coords_for_box(index, start_x, start_y, pitch):
    """
    指定されたインデックス(0始まり)のボックス座標を計算する
    ※ このPDFは「左に行くほどXが減る（数値が小さくなる）」座標系であることに注意
    """
    # 左のボックス(index 0)が一番Xが大きい (805)
    # 右のボックス(index 1)はXが小さい (774)
    # つまり、indexが増えるごとに X は「減る」
    user_x = start_x - (index * pitch)
    user_y = start_y
    
    # 変換: StorageX = UserY + OffsetV, StorageY = UserX + OffsetH
    storage_x = user_y + OFFSET_VERT
    storage_y = user_x + OFFSET_HORIZ
    return storage_x, storage_y

def fill_full_form(area_name, class_num, kana, serial_num):
    input_pdf = "OCR_第１号様式_記入済み.pdf"
    output_pdf = "OCR_Full_Filled.pdf"
    
    pdf_fields = []

    # 1. 地域名 (Area Name)
    for i, char in enumerate(area_name):
        sx, sy = get_coords_for_box(i, AREA_NAME_START_X, AREA_NAME_START_Y, AREA_NAME_PITCH)
        pdf_fields.append({
            "text": char, "x": sx, "y": sy, "font_size": 20, "rotate": 270
        })

    # 2. 分類番号 (Class Number)
    if CLASS_NUM_CONFIG["start_x"] > 0:
        for i, char in enumerate(class_num):
            sx, sy = get_coords_for_box(i, CLASS_NUM_CONFIG["start_x"], CLASS_NUM_CONFIG["start_y"], CLASS_NUM_CONFIG["pitch"])
            pdf_fields.append({
                "text": char, "x": sx, "y": sy, "font_size": 20, "rotate": 270
            })

    # 3. かな (Kana)
    if KANA_CONFIG["x"] > 0:
        # 1文字だけ
        sx = KANA_CONFIG["y"] + OFFSET_VERT
        sy = KANA_CONFIG["x"] + OFFSET_HORIZ
        pdf_fields.append({
            "text": kana, "x": sx, "y": sy, "font_size": 20, "rotate": 270
        })

    # 4. 一連指定番号 (Serial Number)
    if SERIAL_NUM_CONFIG["start_x"] > 0:
        for i, char in enumerate(serial_num):
            sx, sy = get_coords_for_box(i, SERIAL_NUM_CONFIG["start_x"], SERIAL_NUM_CONFIG["start_y"], SERIAL_NUM_CONFIG["pitch"])
            pdf_fields.append({
                "text": char, "x": sx, "y": sy, "font_size": 20, "rotate": 270 # 30->20に変更
            })

    print(f"Generating Full PDF...")
    embed_text_to_pdf(input_pdf, output_pdf, pdf_fields, pagesize=(595, 836))

if __name__ == "__main__":
    # テストデータ
    fill_full_form("尾張小牧", "330", "さ", "1234")
