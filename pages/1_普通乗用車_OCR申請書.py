# -*- coding: utf-8 -*-
"""
普通乗用車 OCR申請書（第1号様式）作成
"""

import streamlit as st
import os
from ocr_fields import (
    get_vehicle_registration_data, get_chassis_data, get_owner_code_data, 
    get_model_data, get_class_data, get_owner_name_data, get_owner_address_data,
    get_user_name_data, get_user_address_data, get_section_data, get_single_char_data
)
from pdf_utils import create_blank_pdf_with_text

st.title("🚗 OCR申請書（第1号様式）作成")
st.markdown("必要な情報を入力して、「PDF作成」ボタンを押してください。")

# --- 1. 車両情報 ---
st.header("1. 車両情報")
col1, col2, col3, col4 = st.columns(4)
with col1:
    area_name = st.text_input("地域名 (例: 尾張小牧)", value="尾張小牧")
with col2:
    class_num = st.text_input("分類番号 (例: 330)", value="330")
with col3:
    kana = st.text_input("かな (例: さ)", value="さ")
with col4:
    serial_num = st.text_input("一連指定番号 (例: 1234)", value="1234")

col_chassis, col_code = st.columns(2)
with col_chassis:
    chassis_num = st.text_input("車台番号 (例: ZVW55-1234567)", value="ZVW55-1234567")
    st.caption("ローマ字が入ると自動で下欄にマークが付きます")
with col_code:
    owner_code = st.text_input("所有者コード (5桁)", value="12345")

col_model, col_class_code = st.columns(2)
with col_model:
    model_num = st.text_input("型式指定番号 (5桁)", value="12345")
with col_class_code:
    class_code = st.text_input("類別区分番号 (4桁)", value="0001")

# --- 2. 新所有者・現所有者 ---
st.header("2. 新所有者・現所有者")
owner_name = st.text_area("氏名 (改行で2行になります)", value="株式会社アットカーズ\n代表取締役　上田和治")
owner_address = st.text_input("住所", value="滋賀県守山市赤野井町761-2")

# 所有権解除フラグ
is_ownership_release = st.checkbox("所有権解除 (コード: 1)", value=True)

# --- 3. 使用者 ---
st.header("3. 使用者")

# フラグ設定
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    is_user_name_same = st.checkbox("氏名 同上 (コード: 1)", value=True)
with col_u2:
    is_user_address_same = st.checkbox("住所 同上 (コード: 1)", value=True)
with col_u3:
    is_principal_place_same = st.checkbox("使用の本拠 同上 (コード: 1)", value=True)

user_name = st.text_area("氏名 (同上の場合は空欄でも可)", value="株式会社アットカーズ\n代表取締役　上田和治")
user_address = st.text_input("住所 (同上の場合は空欄でも可)", value="滋賀県守山市赤野井町761-2")

# --- 4. その他 (旧所有者・代理人・受検者) ---
with st.expander("4. その他 (旧所有者・代理人・受検者)", expanded=False):
    st.subheader("旧所有者")
    old_owner_name = st.text_area("旧所有者 氏名", value="株式会社旧オーナー代表取締役 旧田太郎")
    old_owner_address = st.text_input("旧所有者 住所", value="旧県旧市旧町1-1")
    
    st.subheader("申請代理人")
    agent_name = st.text_area("代理人 氏名", value="日本自動車販売協会連合会滋賀県支部長")
    agent_address = st.text_input("代理人 住所", value="滋賀県守山市木浜町2298-4")
    
    st.subheader("受検者")
    examinee_name = st.text_area("受検者 氏名", value="受検 太郎")
    examinee_address = st.text_input("受検者 住所", value="受検県受検市受検町3-3")

# --- PDF生成 ---
st.markdown("---")
if st.button("📄 PDF作成", type="primary"):
    output_pdf = "output/OCR_TextOnly.pdf"
    
    try:
        # データ生成
        reg_fields = get_vehicle_registration_data(area_name, class_num, kana, serial_num)
        chassis_fields = get_chassis_data(chassis_num)
        owner_code_fields = get_owner_code_data(owner_code)
        model_fields = get_model_data(model_num)
        class_fields = get_class_data(class_code)
        
        owner_name_fields = get_owner_name_data(owner_name)
        owner_address_fields = get_owner_address_data(owner_address)
        
        user_name_fields = get_user_name_data(user_name)
        user_address_fields = get_user_address_data(user_address)
        
        old_owner_fields = get_section_data(old_owner_name, old_owner_address, "old_owner_name", "old_owner_address")
        agent_fields = get_section_data(agent_name, agent_address, "agent_name", "agent_address")
        examinee_fields = get_section_data(examinee_name, examinee_address, "examinee_name", "examinee_address")

        # フラグ処理
        flags = []
        if is_ownership_release:
            flags += get_single_char_data("1", "owner_ownership_release_flag")
        if is_user_name_same:
            flags += get_single_char_data("1", "user_name_same_flag")
        if is_user_address_same:
            flags += get_single_char_data("1", "user_address_same_flag")
        if is_principal_place_same:
            flags += get_single_char_data("1", "principal_place_same_flag")
        
        # 全結合
        all_fields = (reg_fields + chassis_fields + owner_code_fields + model_fields + class_fields + 
                     owner_name_fields + owner_address_fields + user_name_fields + user_address_fields +
                     old_owner_fields + agent_fields + examinee_fields + flags)
        
        # 生成 (白紙モード - テキストのみ)
        create_blank_pdf_with_text(output_pdf, all_fields, pagesize=(595, 836))
        
        st.success("✅ PDFの作成に成功しました！")
        
        # ダウンロードボタン
        with open(output_pdf, "rb") as f:
            st.download_button(
                label="📥 PDFをダウンロード",
                data=f,
                file_name="OCR_Formatted.pdf",
                mime="application/pdf"
            )
            
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
        import traceback
        st.code(traceback.format_exc())
