# -*- coding: utf-8 -*-
"""
軽自動車税環境性能割（報告書）作成アプリ

Streamlitアプリで入力フォームを提供し、PDFを生成します。
"""

import streamlit as st
import os
from kei_report_fields import (
    ALL_FIELDS, PAGE_SIZE, get_field_list_for_pdf,
    FIELD_A_OLD_VEHICLE, FIELD_B_VEHICLE_INFO, 
    FIELD_C_TAXPAYER, FIELD_D_FORMER, FIELD_E_APPLICANT
)
from pdf_utils import create_blank_pdf_with_text

def main():
    st.set_page_config(page_title="軽自動車税報告書", layout="wide")
    
    st.title("🚗 軽自動車税環境性能割（報告書）作成")
    st.markdown("必要な情報を入力して、「PDF作成」ボタンを押してください。")

    # データ格納用
    data = {}

    # ============================================================
    # Aエリア: 旧車両番号
    # ============================================================
    st.header("A. 旧車両番号・初度検査年月")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data["A1_office"] = st.text_input("運輸支局等", value="一宮", max_chars=4)
    with col2:
        data["A2_class_number"] = st.text_input("分類番号", value="580", max_chars=3)
    with col3:
        data["A3_kana"] = st.text_input("かな", value="と", max_chars=1)
    with col4:
        data["A4_serial"] = st.text_input("一連番号", value="6528", max_chars=4)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        data["A5_era"] = st.selectbox("年号", options=["5 (令和)", "4 (平成)"], index=0)[0]
    with col6:
        data["A6_year"] = st.text_input("年", value="01", max_chars=2)
    with col7:
        data["A7_month"] = st.text_input("月", value="07", max_chars=2)
    with col8:
        data["A8_usage"] = st.text_input("用途コード", value="01", max_chars=2)
        st.caption("乗用=01")

    # ============================================================
    # Bエリア: 車両情報
    # ============================================================
    st.header("B. 車両情報")
    
    col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
    with col_b1:
        data["B1_category"] = st.selectbox("種別", options=["4 (軽)", "3 (小型)"], index=0)[0]
    with col_b2:
        data["B2_private"] = st.selectbox("営・自区分", options=["2 (家庭用)", "1 (営業用)"], index=0)[0]
    with col_b3:
        data["B3_body_type"] = st.text_input("車体の形状", value="ステーションワゴン")
    with col_b4:
        data["B4_maker"] = st.text_input("車名", value="スズキ")
    with col_b5:
        data["B5_model"] = st.text_input("型式", value="ABA-DA17W")
    
    col_b6, col_b7, col_b8, col_b9, col_b10 = st.columns(5)
    with col_b6:
        data["B6_capacity"] = st.text_input("乗車定員", value="4")
    with col_b7:
        data["B7_weight"] = st.text_input("車両重量(kg)", value="950")
    with col_b8:
        data["B8_total_weight"] = st.text_input("車両総重量(kg)", value="1170")
    with col_b9:
        data["B9_chassis"] = st.text_input("車台番号", value="201416")
    with col_b10:
        data["B10_category_code"] = st.text_input("類別区分番号", value="0008")
    
    col_b11, col_b12, col_b13, col_b14, col_b15, col_b16 = st.columns(6)
    with col_b11:
        data["B11_engine"] = st.text_input("原動機型式", value="R06A")
    with col_b12:
        data["B12_length"] = st.text_input("長さ(cm)", value="339")
    with col_b13:
        data["B13_width"] = st.text_input("幅(cm)", value="147")
    with col_b14:
        data["B14_height"] = st.text_input("高さ(cm)", value="191")
    with col_b15:
        data["B15_displacement"] = st.text_input("総排気量(L)", value="0.65")
    with col_b16:
        data["B16_fuel"] = st.selectbox("燃料", options=["1 (ガソリン)", "2 (軽油)", "3 (その他)"], index=0)[0]

    # ============================================================
    # Cエリア: 納税義務者
    # ============================================================
    st.header("C. 納税義務者")
    
    col_c1, col_c2 = st.columns([1, 3])
    with col_c1:
        zip_code = st.text_input("郵便番号", value="524-0061", max_chars=8)
        if "-" in zip_code:
            parts = zip_code.split("-")
            data["C1_zip_upper"] = parts[0]
            data["C2_zip_lower"] = parts[1] if len(parts) > 1 else ""
        else:
            data["C1_zip_upper"] = zip_code[:3]
            data["C2_zip_lower"] = zip_code[3:]
    with col_c2:
        data["C3_address"] = st.text_input("住所", value="滋賀県守山市赤野井町761-2")
    
    col_c3, col_c4 = st.columns(2)
    with col_c3:
        data["C4_name"] = st.text_input("氏名または名称", value="株式会社アットカーズ")
    with col_c4:
        phone = st.text_input("電話番号（ハイフンなし）", value="0775859397")
        data["C5_phone"] = phone.replace("-", "")
    
    col_c5, col_c6 = st.columns(2)
    with col_c5:
        data["C6_owner_check"] = st.checkbox("所有者: 納税義務者に同じ", value=True)
    with col_c6:
        data["C7_user_check"] = st.checkbox("使用者: 納税義務者に同じ", value=True)

    # ============================================================
    # Dエリア: 旧所有者・旧使用者
    # ============================================================
    with st.expander("D. 旧所有者・旧使用者", expanded=False):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            data["D1_former_owner_address"] = st.text_input("旧所有者 住所", value="愛知県一宮市木曽川町外割田")
            data["D2_former_owner_name"] = st.text_input("旧所有者 氏名", value="小笠原 崇")
        with col_d2:
            data["D3_former_user_address"] = st.text_input("旧使用者 住所", value="愛知県一宮市木曽川町外割田")
            data["D4_former_user_name"] = st.text_input("旧使用者 氏名", value="小笠原 崇")

    # ============================================================
    # Eエリア: 申告に関わる者
    # ============================================================
    with st.expander("E. 申告に関わる者", expanded=False):
        data["E1_ownership"] = st.selectbox("所有形態", options=["1 (自己所有)", "2 (リース)"], index=0)[0]
        data["E2_address"] = st.text_input("住所 (申告者)", value="滋賀県守山市赤野井町761-2")
        data["E3_name"] = st.text_input("氏名名称 (申告者)", value="株式会社アットカーズ")
        
        col_e4, col_e5, col_e6 = st.columns(3)
        with col_e4:
            data["E4_phone_area"] = st.text_input("市外局番", value="077")
        with col_e5:
            data["E5_phone_local"] = st.text_input("局番", value="585")
        with col_e6:
            data["E6_phone_number"] = st.text_input("番号", value="9397")

    # ============================================================
    # PDF生成
    # ============================================================
    st.markdown("---")
    if st.button("📄 PDF作成", type="primary"):
        output_pdf = "output/kei_report_output.pdf"
        
        try:
            # フィールドリスト生成
            fields = get_field_list_for_pdf(data)
            
            # PDF生成
            create_blank_pdf_with_text(output_pdf, fields, pagesize=PAGE_SIZE)
            
            st.success("✅ PDFの作成に成功しました！")
            
            # ダウンロードボタン
            with open(output_pdf, "rb") as f:
                st.download_button(
                    label="📥 PDFをダウンロード",
                    data=f,
                    file_name="kei_report.pdf",
                    mime="application/pdf"
                )
                
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {e}")
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
