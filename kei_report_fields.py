# -*- coding: utf-8 -*-
"""
軽自動車税環境性能割（報告書）フィールド定義

このファイルは、軽自動車税環境性能割（報告書）の各入力フィールドの
座標情報を定義しています。

座標系: PDF座標（左下原点、ポイント単位）
PDFサイズ: 841.2 x 595.2 pt（A4横向き相当）
"""

# PDFページサイズ
PAGE_SIZE = (841.2, 595.2)

# フォント設定
DEFAULT_FONT = "HeiseiMin-W3"
DEFAULT_FONT_SIZE = 12
SMALL_FONT_SIZE = 10
TINY_FONT_SIZE = 8

# ============================================================
# Aエリア: 旧車両番号
# ============================================================
FIELD_A_OLD_VEHICLE = {
    "A1_office": {  # 運輸支局等
        "x": 324, "y": 509,
        "font_size": 12,
        "char_width": 15,
        "spaced": True,
        "label": "運輸支局等"
    },
    "A2_class_number": {  # 分類番号
        "x": 392, "y": 509,
        "font_size": 12,
        "char_width": 15,
        "spaced": True,
        "label": "分類番号"
    },
    "A3_kana": {  # かな
        "x": 446, "y": 509,
        "font_size": 12,
        "label": "かな"
    },
    "A4_serial": {  # 一連番号
        "x": 468, "y": 509,
        "font_size": 12,
        "char_width": 15,
        "spaced": True,
        "label": "一連番号"
    },
    "A5_era": {  # 年号（令和=5）
        "x": 710, "y": 509,
        "font_size": 12,
        "label": "年号"
    },
    "A6_year": {  # 年
        "x": 745, "y": 509,
        "font_size": 12,
        "char_width": 15,
        "spaced": True,
        "label": "年"
    },
    "A7_month": {  # 月
        "x": 784, "y": 509,
        "font_size": 12,
        "char_width": 15,
        "spaced": True,
        "label": "月"
    },
    "A8_usage": {  # 用途コード
        "x": 790, "y": 488,
        "font_size": 10,
        "char_width": 15,
        "spaced": True,
        "label": "用途コード"
    },
}

# ============================================================
# Bエリア: 車両情報
# ============================================================
FIELD_B_VEHICLE_INFO = {
    "B1_category": {  # 種別（軽=4）
        "x": 360, "y": 453,
        "font_size": 12,
        "label": "種別"
    },
    "B2_private": {  # 営・自区分
        "x": 419, "y": 453,
        "font_size": 12,
        "label": "営・自区分"
    },
    "B3_body_type": {  # 車体の形状
        "x": 440, "y": 453,
        "font_size": 10,
        "max_width": 130,
        "label": "車体の形状"
    },
    "B4_maker": {  # 車名
        "x": 580, "y": 453,
        "font_size": 12,
        "max_width": 160,
        "label": "車名"
    },
    "B5_model": {  # 型式
        "x": 745, "y": 453,
        "font_size": 10,
        "max_width": 90,
        "label": "型式"
    },
    "B6_capacity": {  # 乗車定員
        "x": 330, "y": 425,
        "font_size": 12,
        "label": "乗車定員"
    },
    "B7_weight": {  # 車両重量
        "x": 525, "y": 425,
        "font_size": 12,
        "label": "車両重量"
    },
    "B8_total_weight": {  # 車両総重量
        "x": 585, "y": 425,
        "font_size": 12,
        "label": "車両総重量"
    },
    "B9_chassis": {  # 車台番号
        "x": 640, "y": 425,
        "font_size": 10,
        "label": "車台番号"
    },
    "B10_category_code": {  # 類別区分番号
        "x": 760, "y": 425,
        "font_size": 12,
        "label": "類別区分番号"
    },
    "B11_engine": {  # 原動機型式
        "x": 330, "y": 400,
        "font_size": 12,
        "label": "原動機型式"
    },
    "B12_length": {  # 長さ
        "x": 410, "y": 400,
        "font_size": 12,
        "label": "長さ"
    },
    "B13_width": {  # 幅
        "x": 460, "y": 400,
        "font_size": 12,
        "label": "幅"
    },
    "B14_height": {  # 高さ
        "x": 515, "y": 400,
        "font_size": 12,
        "label": "高さ"
    },
    "B15_displacement": {  # 総排気量
        "x": 590, "y": 400,
        "font_size": 12,
        "label": "総排気量"
    },
    "B16_fuel": {  # 燃料の種類
        "x": 810, "y": 400,
        "font_size": 12,
        "label": "燃料の種類"
    },
}

# ============================================================
# Cエリア: 納税義務者
# ============================================================
FIELD_C_TAXPAYER = {
    "C1_zip_upper": {  # 郵便番号（上3桁）
        "x": 69, "y": 489,
        "font_size": 10,
        "char_width": 12,
        "spaced": True,
        "label": "郵便番号（上3桁）"
    },
    "C2_zip_lower": {  # 郵便番号（下4桁）
        "x": 112, "y": 489,
        "font_size": 10,
        "char_width": 12,
        "spaced": True,
        "label": "郵便番号（下4桁）"
    },
    "C3_address": {  # 住所
        "x": 65, "y": 462,
        "font_size": 10,
        "max_width": 235,  # X=300まで
        "label": "住所"
    },
    "C4_name": {  # 氏名または名称
        "x": 65, "y": 370,
        "font_size": 10,
        "label": "氏名または名称"
    },
    "C5_phone": {  # 電話番号
        "x": 61, "y": 323,
        "font_size": 10,
        "char_width": 15,
        "spaced": True,
        "label": "電話番号"
    },
    "C6_owner_check": {  # 所有者チェック
        "x": 245, "y": 311,
        "type": "checkbox",
        "width": 6,
        "height": 6,
        "label": "所有者（納税義務者に同じ）"
    },
    "C7_user_check": {  # 使用者チェック
        "x": 245, "y": 251,
        "type": "checkbox",
        "width": 6,
        "height": 6,
        "label": "使用者（納税義務者に同じ）"
    },
}

# ============================================================
# Dエリア: 旧所有者・旧使用者
# ============================================================
FIELD_D_FORMER = {
    "D1_former_owner_address": {  # 旧所有者住所
        "x": 65, "y": 173,
        "font_size": 9,
        "max_width": 235,
        "label": "旧所有者住所"
    },
    "D2_former_owner_name": {  # 旧所有者氏名
        "x": 65, "y": 150,
        "font_size": 10,
        "label": "旧所有者氏名"
    },
    "D3_former_user_address": {  # 旧使用者住所
        "x": 65, "y": 124,
        "font_size": 9,
        "label": "旧使用者住所"
    },
    "D4_former_user_name": {  # 旧使用者氏名
        "x": 65, "y": 100,
        "font_size": 10,
        "label": "旧使用者氏名"
    },
    "D5_principal_location": {  # 主たる定置場（市町村名）
        "x": 755, "y": 350,
        "font_size": 10,
        "max_width": 65,
        "label": "主たる定置場"
    },
}

# ============================================================
# Eエリア: 申告に関わる者
# ============================================================
FIELD_E_APPLICANT = {
    "E1_ownership": {  # 所有形態
        "x": 809, "y": 290,
        "font_size": 12,
        "char_width": 15,
        "char_height": 20,
        "label": "所有形態"
    },
    "E2_address": {  # 住所
        "x": 632, "y": 270,
        "font_size": 8,
        "max_width": 193,  # X=825まで
        "label": "住所"
    },
    "E3_name": {  # 氏名名称
        "x": 632, "y": 250,
        "font_size": 8,
        "label": "氏名名称"
    },
    "E4_phone_area": {  # 電話番号・市外局番
        "x": 632, "y": 235,
        "font_size": 10,
        "label": "市外局番"
    },
    "E5_phone_local": {  # 電話番号・局番
        "x": 685, "y": 235,
        "font_size": 10,
        "label": "局番"
    },
    "E6_phone_number": {  # 電話番号・番号
        "x": 745, "y": 235,
        "font_size": 10,
        "label": "番号"
    },
}

# ============================================================
# 全フィールドを統合
# ============================================================
ALL_FIELDS = {
    **FIELD_A_OLD_VEHICLE,
    **FIELD_B_VEHICLE_INFO,
    **FIELD_C_TAXPAYER,
    **FIELD_D_FORMER,
    **FIELD_E_APPLICANT,
}

def get_field_list_for_pdf(data: dict) -> list:
    """
    入力データからPDF生成用のフィールドリストを作成する
    
    Args:
        data: フィールドID -> 値 の辞書
    
    Returns:
        pdf_utils.create_overlay_pdf() に渡せる形式のリスト
    """
    result = []
    
    for field_id, value in data.items():
        if field_id not in ALL_FIELDS or not value:
            continue
        
        field_def = ALL_FIELDS[field_id]
        field_type = field_def.get("type", "text")
        
        if field_type == "checkbox":
            if value:  # チェックがある場合
                result.append({
                    "type": "rect",
                    "x": field_def["x"],
                    "y": field_def["y"],
                    "width": field_def.get("width", 6),
                    "height": field_def.get("height", 6),
                    "stroke": 0,
                    "fill": 1
                })
        elif field_def.get("spaced", False):
            # 1文字ずつ間隔を空けて描画
            char_width = field_def.get("char_width", 15)
            x = field_def["x"]
            y = field_def["y"]
            font_size = field_def.get("font_size", DEFAULT_FONT_SIZE)
            
            for i, char in enumerate(str(value)):
                result.append({
                    "type": "text",
                    "text": char,
                    "x": x + (i * char_width),
                    "y": y,
                    "font_size": font_size,
                    "font_name": DEFAULT_FONT
                })
        else:  # 通常のテキスト
            result.append({
                "type": "text",
                "text": str(value),
                "x": field_def["x"],
                "y": field_def["y"],
                "font_size": field_def.get("font_size", DEFAULT_FONT_SIZE),
                "font_name": DEFAULT_FONT
            })
    
    return result


def extract_city_from_address(address: str) -> str:
    """
    住所から市町村名を抽出する
    
    対応パターン:
    - 〇〇県〇〇市... → 〇〇市
    - 〇〇県〇〇郡〇〇町... → 〇〇町
    - 〇〇県〇〇郡〇〇村... → 〇〇村
    - 〇〇府〇〇市... → 〇〇市
    - 東京都〇〇区... → 〇〇区
    - 東京都〇〇市... → 〇〇市
    
    Args:
        address: 住所文字列
    
    Returns:
        市町村名（見つからない場合は空文字）
    """
    import re
    
    if not address:
        return ""
    
    # パターン1: 〇〇市
    match = re.search(r'([^都道府県]+?市)', address)
    if match:
        return match.group(1)
    
    # パターン2: 〇〇区（東京23区）
    match = re.search(r'([^都道府県]+?区)', address)
    if match:
        return match.group(1)
    
    # パターン3: 〇〇郡〇〇町
    match = re.search(r'([^郡]+?町)', address)
    if match:
        return match.group(1)
    
    # パターン4: 〇〇郡〇〇村
    match = re.search(r'([^郡]+?村)', address)
    if match:
        return match.group(1)
    
    return ""
