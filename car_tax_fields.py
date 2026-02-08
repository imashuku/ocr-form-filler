# -*- coding: utf-8 -*-
"""
普通乗用車 自動車税申告書（発・異）フィールド定義

PDFサイズ: 840 x 593 pt (発), 840 x 592 pt (異)
座標系: PDF座標（左下原点、ポイント単位）
"""

# PDFページサイズ（概算）
PAGE_SIZE = (840, 593)

# フォント設定
DEFAULT_FONT = "HeiseiMin-W3"
DEFAULT_FONT_SIZE = 12
SMALL_FONT_SIZE = 10
TINY_FONT_SIZE = 8

# ============================================================
# 基本情報・車両番号・日付
# ============================================================
FIELD_BASIC = {
    # --------------------------------------------------------
    # 登録番号（現在のナンバー）
    # --------------------------------------------------------
    "reg_num_kanji": {  # 漢字 (滋賀): X=47, Y=509(504+5) 幅=30,高さ=20 隙間=1
        "x": 47, "y": 509,
        "box_width": 16, "box_height": 20, "spacing": 1, # box_widthは文字数やフォントによる
        "font_size": 12, "alignment": "center",
        "label": "登録番号(漢字)"
    },
    "reg_num_class": {  # 分類番号 (500): X=132, Y=514(509+5) 幅=13,高さ=16 隙間=1 三文字
        "x": 132, "y": 514,
        "box_width": 13, "box_height": 16, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "登録番号(分類)"
    },
    "reg_num_kana": {  # かな (あ): X=196, Y=509(504+5) 幅=18,高さ=20 一文字
        "x": 196, "y": 509,
        "box_width": 18, "box_height": 20,
        "font_size": 12, "alignment": "center",
        "label": "登録番号(かな)"
    },
    "reg_num_serial": {  # 一連番号 (12-34): X=225, Y=514(509+5) 幅=13,高さ=16 隙間=1 四文字
        "x": 225, "y": 514,
        "box_width": 13, "box_height": 16, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "登録番号(番号)"
    },

    # --------------------------------------------------------
    # 申告区分
    # --------------------------------------------------------
    "declaration_type": {  # 申告区分: X=308+1, Y=548+2
        "x": 309, "y": 550,
        "box_width": 13, "box_height": 16, "alignment": "center",
        "font_size": 12,
        "label": "申告区分"
    },

    # --------------------------------------------------------
    # 旧登録番号
    # --------------------------------------------------------
    "old_reg_num_kanji": {  # 漢字: X=326, Y=509
        "x": 326, "y": 509,
        "box_width": 16, "box_height": 20, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "旧登録番号(漢字)"
    },
    "old_reg_num_class": {  # 分類: X=396, Y=514 (411-15) 間隔広げる
        "x": 396, "y": 514,
        "box_width": 13, "box_height": 16, "spacing": 3,
        "font_size": 12, "alignment": "center",
        "label": "旧登録番号(分類)"
    },
    "old_reg_num_kana": {  # かな: X=450, Y=509 (475-25)
        "x": 450, "y": 509,
        "box_width": 18, "box_height": 20,
        "font_size": 12, "alignment": "center",
        "label": "旧登録番号(かな)"
    },
    "old_reg_num_serial": {  # 一連番号: X=474, Y=514 (504-30) 間隔広げる
        "x": 474, "y": 514,
        "box_width": 13, "box_height": 16, "spacing": 3,
        "font_size": 12, "alignment": "center",
        "label": "旧登録番号(番号)"
    },

    # --------------------------------------------------------
    # 登録年月日
    # --------------------------------------------------------
    "reg_year_era": {  # 年号: X=550+2, Y=509(504+5)
        "x": 552, "y": 509,
        "font_size": 12,
        "label": "登録年月日(年号)"
    },
    "reg_year": {  # 年: X=585, Y=509(504+5) 幅=15,高さ=20 二文字
        "x": 585, "y": 509,
        "box_width": 15, "box_height": 20, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "登録年月日(年)"
    },
    "reg_month": {  # 月: X=625, Y=509(504+5) 幅=15,高さ=20 二文字
        "x": 625, "y": 509,
        "box_width": 15, "box_height": 20, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "登録年月日(月)"
    },
    "reg_day": {  # 日: X=663, Y=509(504+5) 幅=15,高さ=20 二文字
        "x": 663, "y": 509,
        "box_width": 15, "box_height": 20, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "登録年月日(日)"
    },

    # --------------------------------------------------------
    # 初度登録年月 (年号: 数字1文字)
    # --------------------------------------------------------
    "first_reg_era_code": {  # 年号: X=715, Y=509(504+5) ※数字1文字
        "x": 715, "y": 509,
        "box_width": 15, "alignment": "center",
        "font_size": 12,
        "label": "初度登録年号"
    },
    "first_reg_year": {  # 年: X=750, Y=509(504+5) 幅=15,高さ=20 二文字
        "x": 750, "y": 509,
        "box_width": 15, "box_height": 20, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "初度登録年月(年)"
    },
    "first_reg_month": {  # 月: X=790, Y=509(504+5) 幅=15,高さ=20 二文字
        "x": 790, "y": 509,
        "box_width": 15, "box_height": 20, "spacing": 1,
        "font_size": 12, "alignment": "center",
        "label": "初度登録年月(月)"
    },
}

# ============================================================
# 納税義務者
# ============================================================
FIELD_TAXPAYER = {
    # 郵便番号
    "taxpayer_zip1": {  # 上3桁 X=71, Y=485 -> X+2, Y+2
        "x": 73, "y": 487,
        "box_width": 12, "spacing": 0, 
        "font_size": 12,
        "label": "郵便番号(3桁)"
    },
    "taxpayer_zip2": {  # 下4桁 X=116, Y=485 -> X+2, Y+2
        "x": 118, "y": 487,
        "box_width": 12, "spacing": 0, 
        "font_size": 12,
        "label": "郵便番号(4桁)"
    },
    
    # 住所 X=70, Y=462 X=300までの幅におさまるように
    "taxpayer_address": {
        "x": 70, "y": 462,
        "font_size": 10,
        "max_width": 230, # 300 - 70 = 230
        "label": "住所"
    },
    
    # 氏名 X=70, Y=380 X=300までの幅におさまるように
    "taxpayer_name": {
        "x": 70, "y": 370, # ユーザー指摘により修正
        "font_size": 10,  # 氏名なので少し大きくてもいいかもだが一旦10
        "max_width": 230,
        "label": "氏名"
    },
    
    # 電話番号 X=66, Y=325 幅15 高さ19 隙間1.5 (X+3, Y-5 -> Y+10)
    "taxpayer_phone": {
        "x": 66, "y": 325, # Y+10
        "box_width": 15, "spacing": 1.5,
        "font_size": 12,
        "label": "電話番号"
    },
}

# ============================================================
# 所有者・使用者（現在の情報）
# ============================================================
FIELD_OWNER_USER = {
    # 所有者 住所: X=70, Y=303
    "owner_address": {
        "x": 70, "y": 303,
        "font_size": 10,
        "max_width": 230,
        "label": "所有者住所"
    },
    # 所有者 氏名: X=70, Y=275
    "owner_name": {
        "x": 70, "y": 275,
        "font_size": 10,
        "max_width": 230,
        "label": "所有者氏名"
    },
    # 使用者 住所: X=70, Y=243
    "user_address": {
        "x": 70, "y": 243,
        "font_size": 10,
        "max_width": 230,
        "label": "使用者住所"
    },
    # 使用者 氏名: X=70, Y=215
    "user_name": {
        "x": 70, "y": 215,
        "font_size": 10,
        "max_width": 230,
        "label": "使用者氏名"
    },
}

FIELD_OWNER_USER_CHECK = {
    # 所有者チェックボックス 納税義務者に同じ X=247 Y=309
    "owner_same_check": {
        "x": 247, "y": 310, # 少し上に調整
        "font_size": 14,
        "label": "所有者（同上）"
    },
    
    # 使用者チェックボックス 納税義務者に同じ X=247 Y=250
    "user_same_check": {
        "x": 247, "y": 250, # 少し上に調整
        "font_size": 14,
        "label": "使用者（同上）"
    },
}


# ============================================================
# 申告に関わる者（その他欄）
# ============================================================
FIELD_OTHER_PERSON = {
    # 住所 X=635, Y=266 X=820までの幅におさまるように
    "other_address": {
        "x": 635, "y": 266,
        "font_size": 10,
        "max_width": 185, # 820 - 635 = 185
        "label": "その他住所"
    },
    
    # 氏名 X=635, Y=246 X=820までの幅におさまるように
    "other_name": {
        "x": 635, "y": 246,
        "font_size": 10,
        "max_width": 185,
        "label": "その他氏名"
    },
    
    # 電話番号
    "other_phone_area": {  # 市外局番 X=635, Y=230
        "x": 635, "y": 230,
        "font_size": 10,
        "label": "その他電話(市外)"
    },
    "other_phone_local": {  # 局番 X=685, Y=230
        "x": 685, "y": 230,
        "font_size": 10,
        "label": "その他電話(局番)"
    },
    "other_phone_number": {  # 番号 X=750, Y=230
        "x": 750, "y": 230,
        "font_size": 10,
        "label": "その他電話(番号)"
    },
}

# ============================================================
# 車両情報
# ============================================================
# ============================================================
# 車両情報
# ============================================================
FIELD_VEHICLE = {
    # 用途 (01): X=796, Y=480 -> X+2, Y+3
    "usage_code": {
        "x": 798, "y": 483,
        "box_width": 15, "spacing": 0.5,
        "font_size": 12, # 高さ18なので12でOK
        "label": "用途"
    },
    
    # 自動車の種別 (1:普通...): X=361, Y=450 -> X+1, Y+3
    "category_code": {
        "x": 362, "y": 453,
        "box_width": 17, "spacing": 0, # 1桁想定だが念のため
        "font_size": 12,
        "alignment": "center",
        "label": "自動車の種別"
    },
    
    # 営業用・自家用の区分: X=422, Y=450 -> X+1, Y+3
    "business_private_code": {
        "x": 423, "y": 453,
        "box_width": 17, "spacing": 0,
        "font_size": 12,
        "alignment": "center",
        "label": "営・自区分"
    },
    
    # 車体の形状: X=450, Y=450 X=575におさまるように
    "body_type": {
        "x": 450, "y": 450,
        "font_size": 10,
        "max_width": 125, # 575 - 450 = 125
        "label": "車体の形状"
    },
    
    # 車名: X=590, Y=450 X=735におさまるように
    "maker_name": {
        "x": 590, "y": 450,
        "font_size": 10,
        "max_width": 145, # 735 - 590 = 145
        "label": "車名"
    },
    
    # 型式: X=745, Y=450 X=825におさまるように
    "model": {
        "x": 745, "y": 450,
        "font_size": 10,
        "max_width": 80, # 825 - 745 = 80
        "label": "型式"
    },
    
    # 車台番号: X=650, Y=425 X=755までにおさまるように
    "chassis_number": {  
        "x": 650, "y": 425, # Y+10
        "font_size": 10,
        "max_width": 105, # 755 - 650 = 105
        "label": "車台番号"
    },
    
    # 乗車定員: X=330, Y=425
    "capacity": {
        "x": 330, "y": 425, # Y+10
        "font_size": 10,
        "alignment": "right", # 数字なので右寄せが綺麗かもだが一旦左で
        "label": "乗車定員"
    },
    
    # 最大積載量: X=420, Y=425
    "max_loading": {
        "x": 420, "y": 425, # Y+10
        "font_size": 10,
        "label": "最大積載量"
    },
    
    # 車両重量: X=520, Y=425
    "vehicle_weight": {
        "x": 520, "y": 425, # Y+10
        "font_size": 10,
        "label": "車両重量"
    },
    
    # 車両総重量: X=590, Y=425
    "gross_weight": {
        "x": 590, "y": 425, # Y+10
        "font_size": 10,
        "label": "車両総重量"
    },
    
    # 類別区分番号: X=765, Y=425
    "classification_number": {
        "x": 765, "y": 425, # Y+10
        "font_size": 10,
        "label": "類別区分番号"
    },
    
    # 原動機の型式: X=310, Y=397
    "engine_model": {
        "x": 310, "y": 397,
        "font_size": 10,
        "label": "原動機の型式"
    },
    
    # 長さ: X=415, Y=397
    "length": {
        "x": 415, "y": 397,
        "font_size": 10,
        "label": "長さ"
    },
    
    # 幅: X=460, Y=397
    "width": {
        "x": 460, "y": 397,
        "font_size": 10,
        "label": "幅"
    },
    
    # 高さ: X=520, Y=397
    "height": {
        "x": 520, "y": 397,
        "font_size": 10,
        "label": "高さ"
    },
    
    # 総排気量・定格出力: X=590, Y=397
    "displacement": {
        "x": 590, "y": 397,
        "font_size": 10,
        "label": "総排気量"
    },
    
    # ローター数: X=680, Y=397
    # ※ロータリーエンジンの場合など。通常は空欄か
    "rotor_count": {
        "x": 680, "y": 397,
        "font_size": 10,
        "label": "ローター数"
    },
    
    # 燃料の種類 (1:ガソリン...): X=813, Y=395 -> X+1, Y+3
    "fuel_code": {
        "x": 814, "y": 398,
        "box_width": 13, "box_height": 16, # Y調整は現状していないが定義として
        "font_size": 10,
        "alignment": "center",
        "label": "燃料の種類"
    },

}

# ============================================================
# 旧所有者・旧使用者・その他
# ============================================================
FIELD_OLD_OWNER_USER = {
    # 旧所有者 住所: X=65, Y=173 幅X=300まで
    "old_owner_address": {
        "x": 65, "y": 173,
        "font_size": 10,
        "max_width": 235, # 300 - 65 = 235
        "label": "旧所有者住所"
    },
    # 旧所有者 氏名: X=65, Y=149 幅X=300まで
    "old_owner_name": {
        "x": 65, "y": 149,
        "font_size": 10,
        "max_width": 235,
        "label": "旧所有者氏名"
    },
    # 旧使用者 住所: X=65, Y=122 幅X=300まで
    "old_user_address": {
        "x": 65, "y": 122,
        "font_size": 10,
        "max_width": 235,
        "label": "旧使用者住所"
    },
    # 旧使用者 氏名: X=65, Y=99 幅X=300まで
    "old_user_name": {
        "x": 65, "y": 99,
        "font_size": 10,
        "max_width": 235,
        "label": "旧使用者氏名"
    },
    
    # 主たる定置場（旧）: X=765, Y=343 幅X=820まで
    "old_parking_place": {
        "x": 765, "y": 343,
        "font_size": 10,
        "max_width": 55, # 820 - 765 = 55
        "label": "主たる定置場（旧）"
    },
    
    # 取得前の用途 (数字1文字): X=716, Y=315 -> X+2, Y+3
    "prev_usage_code": {
        "x": 718, "y": 318,
        "box_width": 14, "spacing": 0,
        "font_size": 12, # 高さ17なので12でOK
        "alignment": "center",
        "label": "取得前の用途"
    },
    
    # 所有形態 (数字1文字): X=812, Y=284 -> X+3, Y+3
    "ownership_code": {
        "x": 815, "y": 287,
        "box_width": 14, "spacing": 0,
        "font_size": 12,
        "alignment": "center",
        "label": "所有形態"
    },
}

# ============================================================
# 全フィールド統合
# ============================================================
ALL_FIELDS = {
    **FIELD_BASIC,
    **FIELD_TAXPAYER,
    **FIELD_OWNER_USER,  # 追加
    **FIELD_OWNER_USER_CHECK,
    **FIELD_OTHER_PERSON,
    **FIELD_VEHICLE,
    **FIELD_OLD_OWNER_USER,
}

def get_car_tax_field_list(data: dict) -> list:
    """
    入力データからPDF生成用のフィールドリストを作成する
    
    Args:
        data: フィールドID -> 値 の辞書
    
    Returns:
        pdf_utils.create_overlay_pdf() に渡せる形式のリスト
    """
    result = []
    
    for field_id, value in data.items():
        if field_id not in ALL_FIELDS:
            continue
            
        # 値がない場合は基本スキップ（Falseも含む）
        # ただしチェックボックスの場合は別途処理
        if not value and field_id not in ["owner_same_check", "user_same_check"]:
            continue
            
        field_def = ALL_FIELDS[field_id].copy()
        font_name = field_def.get("font_name", DEFAULT_FONT)
        font_size = field_def.get("font_size", DEFAULT_FONT_SIZE)

        # 1. チェックボックス (黒塗り対応: type="rect")
        # --------------------------------------------------------
        if field_id in ["owner_same_check", "user_same_check"]:
            if value:
                # 黒塗りサイズの縮小 (10 -> 7)
                result.append({
                    "type": "rect",
                    "x": field_def["x"],
                    "y": field_def["y"] - 1, # 少し調整
                    "width": 7,
                    "height": 7,
                    "fill": 1,
                    "stroke": 0
                })
            continue # チェックボックスの処理はここで終了

        # 2. 値の補正 (日付の0埋め、電話番号のハイフン除去など)
        # --------------------------------------------------------
        text_value = str(value) if value is not None else ""
        
        # 納税義務者の電話番号はハイフン除去
        if field_id == "taxpayer_phone":
            text_value = text_value.replace("-", "").replace(" ", "").replace("（", "").replace("）", "").replace("(", "").replace(")", "")
        
        # 日付関連は2桁0埋め
        if any(x in field_id for x in ["year", "month", "day"]):
            # 数値1文字かつ年号フィールドでない場合のみ0埋め
            if text_value.isdigit() and len(text_value) == 1 and "era" not in field_id:
                text_value = text_value.zfill(2)

        # 3. 描画位置の計算
        # --------------------------------------------------------
        
        # ボックス配置計算 (box_width指定がある場合)
        if "box_width" in field_def:
            x_start = field_def["x"]
            y_start = field_def["y"]
            box_width = field_def["box_width"]
            spacing = field_def.get("spacing", 0)
            alignment = field_def.get("alignment", "left")

            for i, char in enumerate(text_value):
                char_box_x = x_start + (box_width + spacing) * i
                
                if alignment == "center":
                    char_x = char_box_x + (box_width - font_size) / 2
                    if char_x < char_box_x: char_x = char_box_x
                else:
                    char_x = char_box_x
                
                result.append({
                    "type": "text",
                    "text": char,
                    "x": char_x,
                    "y": y_start,
                    "font_size": font_size,
                    "font_name": font_name
                })
                
        # 通常テキスト配置
        else:
            result.append({
                "type": "text",
                "text": text_value,
                "x": field_def["x"],
                "y": field_def["y"],
                "font_size": font_size,
                "font_name": font_name
            })
        
    return result

