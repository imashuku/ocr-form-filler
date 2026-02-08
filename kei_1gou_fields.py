# kei_1gou_fields.py
# 軽自動車 第1号様式 OCR申請書用フィールド定義

"""
軽1号様式はランドスケープ（横向き）のフォームです。
PDFサイズ: 838 x 595 pt

座標系:
- ランドスケープ画像（0.7度傾き補正 + 90度回転）から座標を取得
- 画像は300dpi、px_to_pt = 72/300 = 0.24
- 原点は左上、Xは右方向、Yは下方向
"""

# ==========================================
# 座標・補正値 定義 (Golden Configs)
# ==========================================

# 各フィールドの設定
# 座標はPDFポイント (pt) 単位
# グリッド画像からの読み取り値を基に設定

FIELD_CONFIGS = {
    # ========================================
    # 左上エリア: 業務種別・申請区分等
    # ========================================
    
    # 1. 業務種別コード (例: 0012) - 左上の4マス
    "business_code": {
        "start_x": 28,
        "start_y": 68,
        "pitch_x": 22,
        "font_size": 18,
        "max_length": 4
    },
    
    # 2. 申請区分 (例: 4) - 業務種別の右隣
    "application_type": {
        "x": 120,
        "y": 68,
        "font_size": 18
    },
    
    # ========================================
    # 車両番号エリア（2行目）
    # ========================================
    
    # 3. 車両番号 - プレート記号 (例: -B)
    "plate_code": {
        "start_x": 28,
        "start_y": 125,
        "pitch_x": 22,
        "font_size": 18,
        "max_length": 2
    },
    
    # 4. 車両番号 - 分類番号 (例: 580)
    "class_num": {
        "start_x": 120,
        "start_y": 125,
        "pitch_x": 22,
        "font_size": 18,
        "max_length": 3
    },
    
    # 5. 車両番号 - かな (例: こ)
    "kana": {
        "x": 200,
        "y": 125,
        "font_size": 18
    },
    
    # 6. 車両番号 - 一連番号 (例: 6528)
    "serial_num": {
        "start_x": 235,
        "start_y": 125,
        "pitch_x": 22,
        "font_size": 18,
        "max_length": 4
    },
    
    # 7. 有効期間 (例: 20140416)
    "expiry_date": {
        "start_x": 390,
        "start_y": 125,
        "pitch_x": 22,
        "font_size": 18,
        "max_length": 8
    },
    
    # ========================================
    # 右端エリア: 届出区分等
    # ========================================
    
    # 8. 届出区分1 (例: 7)
    "notification_type_1": {
        "x": 760,
        "y": 115,
        "font_size": 18
    },
    
    # 9. 届出区分2 (例: 7)
    "notification_type_2": {
        "x": 760,
        "y": 160,
        "font_size": 18
    },
    
    # ========================================
    # 中段エリア: 届出年月日、主務所コード等
    # ========================================
    
    # 10. 届出年月日 (例: 4.07.04)
    "notification_date": {
        "start_x": 705,
        "start_y": 210,
        "pitch_x": 18,
        "font_size": 18,
        "max_length": 7
    },
    
    # 11. 主務所コード (例: 47774)
    "office_code": {
        "start_x": 705,
        "start_y": 255,
        "pitch_x": 18,
        "font_size": 18,
        "max_length": 5
    },
    
    # ========================================
    # 下段エリア: 車台番号
    # ========================================
    
    # 12. 車台番号 (例: 19008 0008)
    "chassis_num": {
        "start_x": 28,
        "start_y": 408,
        "pitch_x": 22,
        "font_size": 18,
        "max_length": 17
    },
    
    # ========================================
    # 氏名・住所エリア（フリー記述）
    # ========================================
    
    # 13. 使用者氏名 (例: 株式会社アットカーズ)
    "user_name": {
        "start_x": 70,
        "start_y": 480,
        "pitch_x": 10,
        "font_size": 10
    },
    
    # 14. 使用者住所
    "user_address": {
        "start_x": 70,
        "start_y": 495,
        "pitch_x": 8,
        "font_size": 9
    },
    
    # 15. 所有者氏名
    "owner_name": {
        "start_x": 70,
        "start_y": 530,
        "pitch_x": 10,
        "font_size": 10
    },
    
    # 16. 所有者住所
    "owner_address": {
        "start_x": 70,
        "start_y": 545,
        "pitch_x": 8,
        "font_size": 9
    },
}


# ==========================================
# ヘルパー関数
# ==========================================

def to_half_width(text):
    """全角英数字・記号を半角に変換"""
    table = str.maketrans({
        '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
        '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
        'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E',
        'Ｆ': 'F', 'Ｇ': 'G', 'Ｈ': 'H', 'Ｉ': 'I', 'Ｊ': 'J',
        'Ｋ': 'K', 'Ｌ': 'L', 'Ｍ': 'M', 'Ｎ': 'N', 'Ｏ': 'O',
        'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R', 'Ｓ': 'S', 'Ｔ': 'T',
        'Ｕ': 'U', 'Ｖ': 'V', 'Ｗ': 'W', 'Ｘ': 'X', 'Ｙ': 'Y', 'Ｚ': 'Z',
        'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e',
        'ｆ': 'f', 'ｇ': 'g', 'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j',
        'ｋ': 'k', 'ｌ': 'l', 'ｍ': 'm', 'ｎ': 'n', 'ｏ': 'o',
        'ｐ': 'p', 'ｑ': 'q', 'ｒ': 'r', 'ｓ': 's', 'ｔ': 't',
        'ｕ': 'u', 'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x', 'ｙ': 'y', 'ｚ': 'z',
        '　': ' ', '－': '-', 'ー': '-'
    })
    return text.translate(table)


def is_half_width(char):
    """半角文字判定 (ASCII範囲)"""
    return ord(char) < 128


def _get_horizontal_fields(text, config_key, max_len=None):
    """
    横書きテキストフィールド生成 (左から右へ)
    """
    pdf_fields = []
    cfg = FIELD_CONFIGS[config_key]
    limit = max_len or cfg.get("max_length", 100)
    
    for i, char in enumerate(text):
        if i >= limit:
            break
        
        x = cfg["start_x"] + (i * cfg["pitch_x"])
        y = cfg["start_y"]
        
        pdf_fields.append({
            "text": char,
            "x": x,
            "y": y,
            "font_size": cfg["font_size"],
            "rotate": 0
        })
    
    return pdf_fields


def _get_single_char(char, config_key):
    """単一文字フィールド生成"""
    cfg = FIELD_CONFIGS[config_key]
    return [{
        "text": char,
        "x": cfg["x"],
        "y": cfg["y"],
        "font_size": cfg["font_size"],
        "rotate": 0
    }]


def _get_proportional_fields(text, config_key, half_ratio=0.6):
    """
    プロポーショナル配置（半角文字は狭いピッチ）
    """
    pdf_fields = []
    cfg = FIELD_CONFIGS[config_key]
    base_pitch = cfg["pitch_x"]
    
    current_x = cfg["start_x"]
    y = cfg["start_y"]
    
    for char in text:
        pdf_fields.append({
            "text": char,
            "x": current_x,
            "y": y,
            "font_size": cfg["font_size"],
            "rotate": 0
        })
        
        if is_half_width(char):
            current_x += base_pitch * half_ratio
        else:
            current_x += base_pitch
    
    return pdf_fields


# ==========================================
# 公開関数: 各フィールドのデータ生成
# ==========================================

def get_business_code_data(code_str):
    """業務種別コード (4桁)"""
    return _get_horizontal_fields(code_str, "business_code")


def get_application_type_data(type_str):
    """申請区分 (1桁)"""
    return _get_single_char(type_str, "application_type")


def get_plate_code_data(code_str):
    """プレート記号 (例: -B)"""
    return _get_horizontal_fields(code_str, "plate_code")


def get_class_num_data(class_str):
    """分類番号 (3桁)"""
    return _get_horizontal_fields(class_str, "class_num")


def get_kana_data(kana_str):
    """かな (1文字)"""
    return _get_single_char(kana_str, "kana")


def get_serial_num_data(serial_str):
    """一連番号 (4桁)"""
    return _get_horizontal_fields(serial_str, "serial_num")


def get_vehicle_number_data(plate_code, class_num, kana, serial_num):
    """
    車両番号の全要素を一括生成
    """
    fields = []
    fields += get_plate_code_data(plate_code)
    fields += get_class_num_data(class_num)
    fields += get_kana_data(kana)
    fields += get_serial_num_data(serial_num)
    return fields


def get_expiry_date_data(date_str):
    """有効期間 (8桁: YYYYMMDD)"""
    return _get_horizontal_fields(date_str, "expiry_date")


def get_notification_type_1_data(type_str):
    """届出区分1 (1桁)"""
    return _get_single_char(type_str, "notification_type_1")


def get_notification_type_2_data(type_str):
    """届出区分2 (1桁)"""
    return _get_single_char(type_str, "notification_type_2")


def get_notification_date_data(date_str):
    """届出年月日 (例: 4.07.04)"""
    text = to_half_width(date_str)
    return _get_horizontal_fields(text, "notification_date")


def get_office_code_data(code_str):
    """主務所コード (5桁)"""
    return _get_horizontal_fields(code_str, "office_code")


def get_chassis_data(chassis_str):
    """車台番号 (最大17桁)"""
    text = to_half_width(chassis_str.upper().replace("-", " "))
    return _get_horizontal_fields(text, "chassis_num")


def get_user_name_data(name_str):
    """使用者氏名"""
    return _get_proportional_fields(name_str, "user_name")


def get_user_address_data(address_str):
    """使用者住所"""
    text = to_half_width(address_str)
    return _get_proportional_fields(text, "user_address")


def get_owner_name_data(name_str):
    """所有者氏名"""
    return _get_proportional_fields(name_str, "owner_name")


def get_owner_address_data(address_str):
    """所有者住所"""
    text = to_half_width(address_str)
    return _get_proportional_fields(text, "owner_address")
