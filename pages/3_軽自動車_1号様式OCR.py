# pages/3_軽自動車_1号様式OCR.py
# 軽自動車 第1号様式 OCR申請書 作成ページ

import streamlit as st
import os
import sys

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kei_1gou_fields import (
    get_business_code_data, get_application_type_data, get_vehicle_number_data,
    get_expiry_date_data, get_notification_type_1_data, get_notification_type_2_data,
    get_notification_date_data, get_office_code_data, get_chassis_data,
    get_user_name_data, get_user_address_data, get_owner_name_data, get_owner_address_data
)
from pdf_utils import create_blank_pdf_with_text


def main():
    st.set_page_config(page_title="軽1号様式OCR申請書", layout="wide")
    
    st.title("軽自動車 第1号様式 OCR申請書作成")
    st.markdown("必要な情報を入力して、「PDF作成」ボタンを押してください。")
    st.caption("※ 座標は調整中です。プレビューで位置を確認してから印刷してください。")

    # --- 1. 業務種別・申請区分 ---
    st.header("1. 業務種別・申請区分")
    col1, col2 = st.columns(2)
    with col1:
        business_code = st.text_input("業務種別コード (4桁)", value="0012")
    with col2:
        application_type = st.text_input("申請区分 (1桁)", value="4")
    
    col3, col4 = st.columns(2)
    with col3:
        notification_type_1 = st.text_input("届出区分1 (1桁)", value="7")
    with col4:
        notification_type_2 = st.text_input("届出区分2 (1桁)", value="7")
    
    col5, col6 = st.columns(2)
    with col5:
        notification_date = st.text_input("届出年月日 (例: 4.07.04)", value="4.07.04")
    with col6:
        office_code = st.text_input("主務所コード (5桁)", value="47774")

    # --- 2. 車両番号 ---
    st.header("2. 車両番号")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        plate_code = st.text_input("プレート記号 (例: -B)", value="-B")
    with col_a2:
        class_num = st.text_input("分類番号 (例: 580)", value="580")
    with col_a3:
        kana = st.text_input("かな (例: こ)", value="こ")
    with col_a4:
        serial_num = st.text_input("一連番号 (例: 6528)", value="6528")

    # --- 3. 車台番号・有効期間 ---
    st.header("3. 車台番号・有効期間")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        chassis_num = st.text_input("車台番号 (最大17桁)", value="19008 0008")
    with col_b2:
        expiry_date = st.text_input("有効期間 (8桁: YYYYMMDD)", value="20140416")

    # --- 4. 使用者情報 ---
    st.header("4. 使用者情報")
    user_name = st.text_input("使用者氏名", value="株式会社アットカーズ")
    user_address = st.text_input("使用者住所", value="滋賀県守山市赤野井町761-2")

    # --- 5. 所有者情報 ---
    st.header("5. 所有者情報")
    owner_name = st.text_input("所有者氏名", value="株式会社アットカーズ")
    owner_address = st.text_input("所有者住所", value="滋賀県守山市赤野井町761-2")

    # --- PDF生成 ---
    st.markdown("---")
    if st.button("PDF作成", type="primary"):
        output_pdf = "output/KEI_1GO_OCR.pdf"
        
        try:
            # データ生成
            all_fields = []
            
            # 業務種別・申請区分
            all_fields += get_business_code_data(business_code)
            all_fields += get_application_type_data(application_type)
            all_fields += get_notification_type_1_data(notification_type_1)
            all_fields += get_notification_type_2_data(notification_type_2)
            all_fields += get_notification_date_data(notification_date)
            all_fields += get_office_code_data(office_code)
            
            # 車両番号
            all_fields += get_vehicle_number_data(plate_code, class_num, kana, serial_num)
            
            # 車台番号
            all_fields += get_chassis_data(chassis_num)
            
            # 有効期間
            all_fields += get_expiry_date_data(expiry_date)
            
            # 使用者情報
            all_fields += get_user_name_data(user_name)
            all_fields += get_user_address_data(user_address)
            
            # 所有者情報
            all_fields += get_owner_name_data(owner_name)
            all_fields += get_owner_address_data(owner_address)
            
            # PDF生成 (軽1号様式: ランドスケープ 838 x 595 pt)
            create_blank_pdf_with_text(output_pdf, all_fields, pagesize=(838, 595))
            
            st.success("PDFの作成に成功しました！")
            
            # ダウンロードボタン
            with open(output_pdf, "rb") as f:
                st.download_button(
                    label="PDFをダウンロード",
                    data=f,
                    file_name="KEI_1GO_OCR.pdf",
                    mime="application/pdf"
                )
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            import traceback
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
