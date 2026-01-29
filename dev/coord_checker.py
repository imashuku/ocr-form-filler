#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
座標確認ツール（Streamlit版）
画像上にグリッドを表示し、クリック位置の座標を確認できます。
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def draw_grid_on_image(image, grid_spacing=50, show_coords=True):
    """
    画像にグリッド線と座標を描画する
    
    Args:
        image: PIL Image
        grid_spacing: グリッド間隔（ピクセル）
        show_coords: 座標ラベルを表示するか
    
    Returns:
        グリッド付きのPIL Image
    """
    # 画像をコピー
    img = image.copy()
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # グリッド線の色
    line_color = (255, 0, 0, 128)  # 赤（半透明）
    text_color = (255, 0, 0)
    
    # フォントサイズ（小さめ）
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except:
        font = ImageFont.load_default()
    
    # 縦線（X座標）
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)
        if show_coords and x % (grid_spacing * 2) == 0:
            draw.text((x + 2, 5), str(x), fill=text_color, font=font)
    
    # 横線（Y座標）
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)
        if show_coords and y % (grid_spacing * 2) == 0:
            draw.text((5, y + 2), str(y), fill=text_color, font=font)
    
    return img

def main():
    st.set_page_config(page_title="座標確認ツール", layout="wide")
    
    st.title("🎯 座標確認ツール")
    st.markdown("画像上のグリッドを参考に、各フィールドの座標を確認します。")
    
    # サイドバー設定
    st.sidebar.header("設定")
    
    # 画像選択
    # スクリプトの場所から相対パスで探す
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    image_dir = os.path.join(parent_dir, "templates")
    
    if os.path.exists(image_dir):
        images = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if images:
            selected_image = st.sidebar.selectbox("画像を選択", images)
            image_path = os.path.join(image_dir, selected_image)
        else:
            st.error("templates/ フォルダに画像がありません")
            return
    else:
        st.error("templates/ フォルダが見つかりません")
        return
    
    # グリッド設定
    grid_spacing = st.sidebar.slider("グリッド間隔 (px)", 25, 100, 50, 5)
    show_coords = st.sidebar.checkbox("座標ラベル表示", value=True)
    
    # 画像読み込み
    try:
        image = Image.open(image_path)
        st.sidebar.write(f"**画像サイズ**: {image.size[0]} x {image.size[1]} px")
    except Exception as e:
        st.error(f"画像を読み込めません: {e}")
        return
    
    # グリッド付き画像を生成
    grid_image = draw_grid_on_image(image, grid_spacing, show_coords)
    
    # 画像表示
    st.image(grid_image, use_container_width=True)
    
    # 座標入力エリア
    st.markdown("---")
    st.subheader("📍 座標メモ")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        field_name = st.text_input("フィールド名", "")
    with col2:
        x_coord = st.number_input("X座標", min_value=0, max_value=5000, value=0)
    with col3:
        y_coord = st.number_input("Y座標", min_value=0, max_value=5000, value=0)
    with col4:
        st.write("")  # スペース
        if st.button("追加"):
            if field_name:
                if "coord_notes" not in st.session_state:
                    st.session_state.coord_notes = []
                st.session_state.coord_notes.append({
                    "name": field_name,
                    "x": x_coord,
                    "y": y_coord
                })
    
    # 座標メモ表示
    if "coord_notes" in st.session_state and st.session_state.coord_notes:
        st.markdown("### 記録した座標")
        for i, note in enumerate(st.session_state.coord_notes):
            st.write(f"{i+1}. **{note['name']}**: X={note['x']}, Y={note['y']}")

if __name__ == "__main__":
    main()
