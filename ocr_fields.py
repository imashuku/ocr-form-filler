# ocr_fields.py

# ==========================================
# 座標・補正値 定義 (Golden Configs)
# ==========================================

# 共通補正値 (座標変換用)
# StorageX = UserY + OFFSET_VERT
# StorageY = UserX + OFFSET_HORIZ
OFFSET_VERT = 7
OFFSET_HORIZ = -3

# 各フィールドの設定
FIELD_CONFIGS = {
    # 1. 地域名 (例: 尾張小牧)
    "area_name": {
        "start_x": 805, 
        "start_y": 439, 
        "pitch": 32, # ボックス間隔
        "font_size": 20
    },
    # 2. 分類番号 (例: 330)
    "class_num": {
        "start_x": 672, 
        "start_y": 440, 
        "pitch": 17,
        "font_size": 20
    },
    # 3. かな (例: さ)
    "kana": {
        "x": 611, 
        "y": 439,
        "font_size": 20
    },
    # 4. 一連指定番号 (例: 1234)
    "serial_num": {
        "start_x": 572, 
        "start_y": 440, 
        "pitch": 17,
        "font_size": 20
    },
    # 5. 車台番号 (Chassis Number) - 英数字23桁
    "chassis_num": {
        "start_x": 492, # 493 -> 492 (右へ1pt移動)
        "start_y": 440, # 438 -> 440 (全体を上へ2pt移動)
        "pitch": 17,   
        "font_size": 20
    },
    # 6. 車台番号 下欄マーク (Mark)
    "chassis_mark": {
        "start_x": 492, 
        "start_y": 430, 
        "width": 13,    
        "height": 2.5,  
        "pitch": 17    
    },
    # 7. 所有者コード (Owner Code) - 5桁
    "owner_code": {
        "start_x": 113, 
        "start_y": 388, 
        "pitch": 17,    
        "font_size": 20 
    },
    # 8. 型式指定番号 (Model Designation) - 5桁
    "model_num": {
        "start_x": 805, 
        "start_y": 155, # 156 -> 155 (さらに下へ1pt)
        "pitch": 17,
        "font_size": 20
    },
    # 9. 類別区分番号 (Classification Code) - 4桁
    "class_code": {
        "start_x": 695, 
        "start_y": 155, # 156 -> 155 (さらに下へ1pt)
        "pitch": 17,
        "font_size": 20
    },
    # 10. 新所有者・現所有者 氏名 (Owner Name) - フリー記述
    "owner_name": {
        "start_x": 700,
        "start_y": 79,  
        "pitch": 12,    
        "font_size": 11 
    },
    # 11. 新所有者・現所有者 住所 (Owner Address) - フリー記述
    "owner_address": {
        "start_x": 700, 
        "start_y": 50,  
        "pitch": 11,    # 9 -> 11 (User指定)
        "font_size": 11 
    },
    # 12. 使用者 氏名 (User Name) - フリー記述
    "user_name": {
        "start_x": 700,
        "start_y": 37,  
        "pitch": 12,    
        "font_size": 11
    },
    # 13. 使用者 住所 (User Address) - フリー記述
    "user_address": {
        "start_x": 700,
        "start_y": 8,   
        "pitch": 11,    
        "font_size": 11
    },
    # 14-15. 旧所有者 (Old Owner) - X=465
    "old_owner_name": { "start_x": 465, "start_y": 85, "pitch": 9, "font_size": 9 }, # Font/Pitch 11->9
    "old_owner_address": { "start_x": 465, "start_y": 71, "pitch": 9, "font_size": 9 },

    # 16-17. 申請代理人 (Agent) - X=465
    "agent_name": { "start_x": 465, "start_y": 54, "pitch": 9, "font_size": 9 }, # Font/Pitch 11->9
    "agent_address": { "start_x": 465, "start_y": 40, "pitch": 9, "font_size": 9 },

    # 18-19. 受検者 (Examinee) - X=465
    "examinee_name": { "start_x": 465, "start_y": 23, "pitch": 9, "font_size": 9 }, # Font/Pitch 11->9
    "examinee_address": { "start_x": 465, "start_y": 9, "pitch": 9, "font_size": 9 },

    # 20. 所有権解除 (Owner Ownership Release Flag) - "1"
    "owner_ownership_release_flag": { "x": 797, "y": 384, "font_size": 20 },
    
    # 21. 使用者 氏名 同上フラグ (User Name Same Flag) - "1"
    "user_name_same_flag": { "x": 797, "y": 291, "font_size": 20 },
    
    # 22. 使用者 住所 同上フラグ (User Address Same Flag) - "1"
    "user_address_same_flag": { "x": 797, "y": 245, "font_size": 20 },
    
    # 23. 使用の本拠の位置 同上フラグ (Principal Place Same Flag) - "1"
    "principal_place_same_flag": { "x": 797, "y": 196, "font_size": 20 }
}

def _transform_coords(user_x, user_y):
    """
    ユーザー座標(User X, User Y)をPDFの内部ストレージ座標(Storage X, Storage Y)に変換する
    Storage X = User Y + Offset V
    Storage Y = User X + Offset H
    """
    storage_x = user_y + OFFSET_VERT
    storage_y = user_x + OFFSET_HORIZ
    return storage_x, storage_y

def _get_coords_for_box_sequence(index, start_x, start_y, pitch):
    """(Legacy) 固定ピッチ計算"""
    user_x = start_x - (index * pitch)
    user_y = start_y
    return _transform_coords(user_x, user_y)

def is_roman_letter(char):
    """ローマ字（アルファベット）か判定する"""
    return 'A' <= char.upper() <= 'Z'

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

def _get_text_fields(text, config_key, max_len=None):
    """共通のテキストフィールド生成ロジック"""
    pdf_fields = []
    cfg = FIELD_CONFIGS[config_key]
    
    for i, char in enumerate(text):
        if max_len and i >= max_len: break
        
        sx, sy = _get_coords_for_box_sequence(i, cfg["start_x"], cfg["start_y"], cfg["pitch"])
        pdf_fields.append({
            "text": char, 
            "x": sx, 
            "y": sy, 
            "font_size": cfg["font_size"], 
            "rotate": 270
        })
    return pdf_fields

def get_owner_code_data(code_str):
    return _get_text_fields(code_str, "owner_code", max_len=5)

def get_model_data(model_str):
    return _get_text_fields(model_str, "model_num", max_len=5)

def get_class_data(class_str):
    return _get_text_fields(class_str, "class_code", max_len=4)

def _get_multiline_text_fields(text_str, config_key, line_spacing=8):
    """複数行テキストの配置ロジック"""
    pdf_fields = []
    cfg = FIELD_CONFIGS[config_key]
    lines = text_str.split('\n')
    
    for line_idx, line_text in enumerate(lines):
        current_y = cfg["start_y"] - (line_idx * line_spacing)
        
        for i, char in enumerate(line_text):
            sx, sy = _get_coords_for_box_sequence(i, cfg["start_x"], current_y, cfg["pitch"])
            pdf_fields.append({
                "text": char,
                "x": sx,
                "y": sy,
                "font_size": cfg["font_size"],
                "rotate": 270
            })
    return pdf_fields

def _get_proportional_text_fields(text_str, config_key, line_spacing=8, half_width_ratio=0.55):
    """
    プロポーショナル配置ロジック
    半角文字は pitch * ratio 分だけ進める
    """
    pdf_fields = []
    cfg = FIELD_CONFIGS[config_key]
    lines = text_str.split('\n')
    base_pitch = cfg["pitch"]

    for line_idx, line_text in enumerate(lines):
        current_y = cfg["start_y"] - (line_idx * line_spacing)
        
        # X座標は累積減算
        current_x = cfg["start_x"]
        
        for char in line_text:
            # 現在位置に文字を配置
            sx, sy = _transform_coords(current_x, current_y)
            pdf_fields.append({
                "text": char,
                "x": sx,
                "y": sy,
                "font_size": cfg["font_size"],
                "rotate": 270
            })
            
            # 次の文字のためにXを進める (減算)
            if is_half_width(char):
                step = base_pitch * half_width_ratio
            else:
                step = base_pitch
            
            current_x -= step

    return pdf_fields

def get_owner_name_data(name_str):
    """新所有者・現所有者 氏名"""
    return _get_multiline_text_fields(name_str, "owner_name", line_spacing=8)

def get_owner_address_data(address_str):
    """新所有者・現所有者 住所"""
    # 半角変換 + プロポーショナル配置
    conv_str = to_half_width(address_str)
    return _get_proportional_text_fields(conv_str, "owner_address", line_spacing=8)

def get_user_name_data(name_str):
    """使用者 氏名"""
    return _get_multiline_text_fields(name_str, "user_name", line_spacing=8)

def get_user_address_data(address_str):
    """使用者 住所"""
    # 半角変換 + プロポーショナル配置
    conv_str = to_half_width(address_str)
    return _get_proportional_text_fields(conv_str, "user_address", line_spacing=8)

def get_section_data(name_str, address_str, name_key, address_key):
    """汎用セクションデータ生成 (旧所有者、代理人、受検者)"""
    name_fields = _get_multiline_text_fields(name_str, name_key, line_spacing=8)
    address_fields = _get_proportional_text_fields(to_half_width(address_str), address_key, line_spacing=8)
    return name_fields + address_fields

def get_single_char_data(char, config_key):
    """単一文字フィールド生成 (フラグ等)"""
    pdf_fields = []
    cfg = FIELD_CONFIGS[config_key]
    sx, sy = _transform_coords(cfg["x"], cfg["y"])
    pdf_fields.append({
        "text": char,
        "x": sx,
        "y": sy,
        "font_size": cfg["font_size"],
        "rotate": 270
    })
    return pdf_fields

def get_chassis_data(chassis_num_str):
    """
    車台番号のデータを生成。ローマ字の場合は下欄にマークを入れる。
    """
    pdf_fields = []
    text_cfg = FIELD_CONFIGS["chassis_num"]
    mark_cfg = FIELD_CONFIGS["chassis_mark"]
    
    # 23桁まで
    for i, char in enumerate(chassis_num_str):
        if i >= 23: break
        
        # 1. 文字の書き込み
        sx, sy = _get_coords_for_box_sequence(i, text_cfg["start_x"], text_cfg["start_y"], text_cfg["pitch"])
        pdf_fields.append({
            "type": "text",
            "text": char,
            "x": sx,
            "y": sy,
            "font_size": text_cfg["font_size"],
            "rotate": 270
        })
        
        # 2. ローマ字なら下欄をマーク (塗りつぶし矩形)
        if is_roman_letter(char):
            # マークボックスの基準座標 (User X, User Y)
            # User Xは左端の座標
            user_x_left = mark_cfg["start_x"] - (i * mark_cfg["pitch"])
            user_y_bottom = mark_cfg["start_y"]
            
            # Storage変換
            # Storage X = UserY + Offset
            # Storage Y = UserX + Offset
            sx_origin, sy_origin = _transform_coords(user_x_left, user_y_bottom)
            
            # 矩形のサイズ計算
            # PDF Storage座標系では：
            # - User Width (Horizontal) -> Storage Y (Height)
            # - User Height (Vertical) -> Storage X (Width)
            # かつ、Storage YはUser Xが減る方向(Right)にいくと減る(Down?)
            # 上記 _transform_coords では sy = user_x + offset.
            # user_xが基準(Left)。Right端は user_x - 17.
            # sy_right = (user_x - 17) + offset = sy_origin - 17.
            # したがって、Storage上のY範囲は [sy_origin - 17, sy_origin].
            # Rect(x, y, w, h) の y は min_y なので sy_origin - 17 を指定する。
            
            rect_w = mark_cfg["height"] # User Height(2.5) -> Storage Width
            rect_h = mark_cfg["width"]  # User Width(17) -> Storage Height
            
            rect_x = sx_origin
            rect_y = sy_origin - rect_h
            
            pdf_fields.append({
                "type": "rect",
                "x": rect_x,
                "y": rect_y,
                "width": rect_w,
                "height": rect_h,
                "fill": 1
            })
            
    return pdf_fields

def get_vehicle_registration_data(area_name, class_num, kana, serial_num):
    """
    自動車登録番号の各要素を受け取り、PDF書き込み用のデータリストを生成して返す
    
    Args:
        area_name (str): 地域名 (例: '尾張小牧')
        class_num (str): 分類番号 (例: '330')
        kana (str): かな (例: 'さ')
        serial_num (str): 一連指定番号 (例: '1234')
        
    Returns:
        list: pdf_utils.embed_text_to_pdf に渡すための辞書リスト
    """
    pdf_fields = []

    # 1. 地域名 (Area Name)
    cfg = FIELD_CONFIGS["area_name"]
    for i, char in enumerate(area_name):
        sx, sy = _get_coords_for_box_sequence(i, cfg["start_x"], cfg["start_y"], cfg["pitch"])
        pdf_fields.append({
            "text": char, "x": sx, "y": sy, 
            "font_size": cfg["font_size"], "rotate": 270
        })

    # 2. 分類番号 (Class Number)
    cfg = FIELD_CONFIGS["class_num"]
    for i, char in enumerate(class_num):
        sx, sy = _get_coords_for_box_sequence(i, cfg["start_x"], cfg["start_y"], cfg["pitch"])
        pdf_fields.append({
            "text": char, "x": sx, "y": sy, 
            "font_size": cfg["font_size"], "rotate": 270
        })

    # 3. かな (Kana)
    cfg = FIELD_CONFIGS["kana"]
    # 1文字固定
    sx, sy = _transform_coords(cfg["x"], cfg["y"])
    pdf_fields.append({
        "text": kana, "x": sx, "y": sy, 
        "font_size": cfg["font_size"], "rotate": 270
    })

    # 4. 一連指定番号 (Serial Number)
    cfg = FIELD_CONFIGS["serial_num"]
    for i, char in enumerate(serial_num):
        sx, sy = _get_coords_for_box_sequence(i, cfg["start_x"], cfg["start_y"], cfg["pitch"])
        pdf_fields.append({
            "text": char, "x": sx, "y": sy, 
            "font_size": cfg["font_size"], "rotate": 270
        })
        
    return pdf_fields
