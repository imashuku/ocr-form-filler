# -*- coding: utf-8 -*-
"""
普通乗用車 自動車税申告書（発・異）作成
"""

import streamlit as st
import os
from car_tax_fields import (
    ALL_FIELDS, PAGE_SIZE, get_car_tax_field_list
)
from pdf_utils import create_blank_pdf_with_text, embed_text_to_pdf

st.title("🚗 普通乗用車 自動車税申告書（発・異）作成")

# ============================================================
# 初期値・テストデータ定義
# ============================================================

# デフォルト値（初回起動時やリセット時に使用）
DEFAULT_VALUES = {
    "inspection_office": "滋賀", "class_number": "300", "kana": "さ", "serial_number": "1234",
    "old_inspection_office": "", "old_class_number": "", "old_kana": "", "old_serial_number": "",
    "reference_number": "", "declaration_type": "",
    "reg_year": "6", "reg_month": "4", "reg_day": "1", "reg_year_era": "令和",
    "first_reg_year": "6", "first_reg_month": "3", "first_reg_era_select": "令和",
    # 納税義務者
    "taxpayer_zip1": "520", "taxpayer_zip2": "0000",
    "taxpayer_address": "滋賀県大津市...",
    "taxpayer_name": "山田 太郎",
    "taxpayer_phone": "090-1234-5678",
    # 車両情報
    "usage_code": "01", "category_code": "1", "business_private_code": "2",
    "body_type": "箱型", "maker_name": "トヨタ", "model": "ABC-12345",
    "chassis_number": "ABC-1234567",
    "classification_number": "0001", "capacity": "5",
    "vehicle_weight": "1500", "gross_weight": "1775", "max_loading": "",
    "engine_model": "ABC",
    "length": "480", "width": "180", "height": "145",
    "displacement": "2.00", "fuel_code": "1", "rotor_count": "",
    # その他
    "owner_address_input": "", "owner_name_input": "", "owner_same_check": False,
    "user_address_input": "", "user_name_input": "", "user_same_check": False,
    "other_address": "", "other_name": "",
    "other_phone_area": "", "other_phone_local": "", "other_phone_number": "",
    "old_owner_address": "", "old_owner_name": "",
    "old_user_address": "", "old_user_name": "",
    "old_parking_place": "", "prev_usage_code": "", "ownership_code": ""
}

# テストデータ（一括入力用）
TEST_DATA = {
    "inspection_office": "滋賀", "class_number": "300", "kana": "さ", "serial_number": "1234",
    "old_inspection_office": "京都", "old_class_number": "300", "old_kana": "い", "old_serial_number": "9876",
    "reference_number": "123456", "declaration_type": "1",
    "reg_year": "6", "reg_month": "4", "reg_day": "1", "reg_year_era": "令和",
    "first_reg_year": "3", "first_reg_month": "4", "first_reg_era_select": "令和",
    # 納税義務者
    "taxpayer_zip1": "520", "taxpayer_zip2": "0000",
    "taxpayer_address": "滋賀県大津市京町四丁目1番1号",
    "taxpayer_name": "滋賀 太郎",
    "taxpayer_phone": "077-528-3211",
    # 所有者・使用者（テスト時は同上チェックを外して値を入れる想定）
    "owner_address_input": "滋賀県大津市...", "owner_name_input": "滋賀 次郎", "owner_same_check": False,
    "user_address_input": "滋賀県大津市...", "user_name_input": "滋賀 三郎", "user_same_check": False,
    # その他
    "other_address": "大阪府大阪市...", "other_name": "大阪 花子",
    "other_phone_area": "06", "other_phone_local": "1234", "other_phone_number": "5678",
    # 車両情報
    "reg_num_kanji": "滋賀", "reg_num_class": "500", "reg_num_kana": "あ", "current_reg_num_serial": "1234",
    "usage_code": "01", 
    "category_code": "1", 
    "business_private_code": "2", 
    "body_type": "箱型",
    "maker_name": "トヨタ",
    "model": "ABC-123",
    "chassis_number": "ABC-1234567",
    "capacity": "5",
    "max_loading": "",
    "vehicle_weight": "1500",
    "gross_weight": "1775",
    "classification_number": "001",
    "engine_model": "ABC",
    "length": "469", "width": "169", "height": "199",
    "displacement": "1.99",
    "fuel_code": "1", "rotor_count": ""
}

# session_stateの初期化関数
def initialize_session_state():
    for key, output_val in DEFAULT_VALUES.items():
        if key not in st.session_state:
            st.session_state[key] = output_val

# 初期化実行（ウィジェット生成前に行う）
initialize_session_state()

# 一括入力ボタン処理
if st.button("📝 テストデータを自動入力（テンプレート読み込み）"):
    for key, val in TEST_DATA.items():
        st.session_state[key] = val
    # フラグセット（必要なら）
    st.session_state["test_data_loaded"] = True
    st.rerun()

st.markdown("必要な情報を入力して、「PDF作成」ボタンを押してください。")

# 申告区分の選択
report_type = st.radio(
    "申告書の種類を選択してください",
    ("発（転入）", "異（異動）"),
    horizontal=True
)

st.markdown("---")

# データ格納用（後でフィールド辞書に変換するために使用）
data = {}

# ============================================================
# 基本情報
# ============================================================
st.header("1. 種類・整理番号・登録番号・日付")
st.info("※整理番号・申告区分は、OCR読み取り用の数値入力欄です。")

col_h1, _ = st.columns([1, 1])
with col_h1:
    # 申告区分のデフォルト値を種類に応じて設定（空の場合）
    default_decl_type = "1" if report_type == "発（転入）" else "2"
    data["declaration_type"] = st.text_input("申告区分", value=st.session_state.get("declaration_type", default_decl_type), key="declaration_type", help="OCR用区分コード (発=1, 異=2)")

st.subheader("現在の登録番号")
col1, col2, col3, col4 = st.columns(4)
with col1:
    data["reg_num_kanji"] = st.text_input("運輸支局等", key="inspection_office")
with col2:
    data["reg_num_class"] = st.text_input("分類番号", key="class_number")
with col3:
    data["reg_num_kana"] = st.text_input("かな", key="kana")
with col4:
    data["reg_num_serial"] = st.text_input("一連番号", key="serial_number")

st.subheader("旧登録番号")
col_old1, col_old2, col_old3, col_old4 = st.columns(4)
with col_old1:
    data["old_reg_num_kanji"] = st.text_input("旧運輸支局等", key="old_inspection_office")
with col_old2:
    data["old_reg_num_class"] = st.text_input("旧分類番号", key="old_class_number")
with col_old3:
    data["old_reg_num_kana"] = st.text_input("旧かな", key="old_kana")
with col_old4:
    data["old_reg_num_serial"] = st.text_input("旧一連番号", key="old_serial_number")

st.subheader("日付情報")
col_date1, col_date2 = st.columns(2)

with col_date1:
    st.markdown("**登録年月日**")
    d1, d2, d3, d4 = st.columns([1, 1, 1, 1])
    with d1:
        # 入力用キーと出力用データキーを分ける
        reg_era_val = st.selectbox("年号", ["", "令和", "平成", "昭和"], key="reg_year_era_select")
        # 年号変換マップ
        era_map = {"昭和": "3", "平成": "4", "令和": "5"}
        data["reg_year_era"] = era_map.get(reg_era_val, "")
    with d2:
        data["reg_year"] = st.text_input("年", key="reg_year")
    with d3:
        data["reg_month"] = st.text_input("月", key="reg_month")
    with d4:
        data["reg_day"] = st.text_input("日", key="reg_day")

with col_date2:
    st.markdown("**初度登録年月**")
    fd1, fd2, fd3 = st.columns([1, 1, 1])
    with fd1:
        era_map = {"昭和": "3", "平成": "4", "令和": "5"}
        # selectboxの選択肢はキー（昭和、平成...)
        era_key_val = st.selectbox("初度年号", list(era_map.keys()), key="first_reg_era_select")
        data["first_reg_era_code"] = era_map[era_key_val]
    with fd2:
        data["first_reg_year"] = st.text_input("初度年", key="first_reg_year")
    with fd3:
        data["first_reg_month"] = st.text_input("初度月", key="first_reg_month")


# ============================================================
# 納税義務者
# ============================================================
st.header("2. 納税義務者・所有者")

st.subheader("納税義務者")
col_tax1, col_tax2 = st.columns([1, 2])
with col_tax1:
    c1, c2 = st.columns([1, 1])
    with c1:
        data["taxpayer_zip1"] = st.text_input("郵便番号(3桁)", key="taxpayer_zip1")
    with c2:
        data["taxpayer_zip2"] = st.text_input("郵便番号(4桁)", key="taxpayer_zip2")
with col_tax2:
    data["taxpayer_address"] = st.text_input("住所", key="taxpayer_address")

c_name, c_phone = st.columns([2, 1])
with c_name:
    data["taxpayer_name"] = st.text_input("氏名", key="taxpayer_name")
with c_phone:
    data["taxpayer_phone"] = st.text_input("電話番号", key="taxpayer_phone")


st.subheader("所有者・使用者（納税義務者と異なる場合）")

# 納税義務者情報をその他申告に関わる者にコピー
if st.button("納税義務者の情報を「その他申告に関わる者」にコピー"):
    if "taxpayer_address" in st.session_state:
        st.session_state["other_address"] = st.session_state["taxpayer_address"]
    if "taxpayer_name" in st.session_state:
        st.session_state["other_name"] = st.session_state["taxpayer_name"]
    # 電話番号も分割して入れる簡易ロジック
    if "taxpayer_phone" in st.session_state:
        phone = st.session_state["taxpayer_phone"]
        parts = phone.split("-")
        if len(parts) == 3:
            st.session_state["other_phone_area"] = parts[0]
            st.session_state["other_phone_local"] = parts[1]
            st.session_state["other_phone_number"] = parts[2]
            
    st.success("「その他申告に関わる者」欄にコピーしました")
    st.rerun()

col_own1, col_own2 = st.columns(2)
with col_own1:
    st.subheader("所有者")
    # keyを指定してsession_stateと連動させる
    data["owner_address"] = st.text_input("所有者住所", key="owner_address_input")
    data["owner_name"] = st.text_input("所有者氏名", key="owner_name_input")
    data["owner_same_check"] = st.checkbox("所有者は納税義務者に同じ", key="owner_same_check")

with col_own2:
    st.subheader("使用者")
    data["user_address"] = st.text_input("使用者住所", key="user_address_input")
    data["user_name"] = st.text_input("使用者氏名", key="user_name_input")
    data["user_same_check"] = st.checkbox("使用者は納税義務者に同じ", key="user_same_check")

st.subheader("その他申告に関わる者（右側の欄）")
col_other1, col_other2 = st.columns([2, 1])
with col_other1:
    data["other_address"] = st.text_input("住所（その他）", key="other_address")
    data["other_name"] = st.text_input("氏名（その他）", key="other_name")

with col_other2:
    data["other_phone_area"] = st.text_input("市外局番", key="other_phone_area")
    data["other_phone_local"] = st.text_input("局番", key="other_phone_local")
    data["other_phone_number"] = st.text_input("番号", key="other_phone_number")


# ============================================================
# 車両情報
# ============================================================
st.header("3. 車両情報")

# 行1: 用途、種別、営・自区分、形状、車名、型式
col_v1, col_v2, col_v3 = st.columns(3)
with col_v1:
    data["usage_code"] = st.text_input("用途(コード)", key="usage_code")
with col_v2:
    data["category_code"] = st.text_input("種別(1:普通...)", key="category_code")
with col_v3:
    data["business_private_code"] = st.text_input("営・自区分(1:自家用...)", key="business_private_code")

col_v4, col_v5, col_v6 = st.columns([1, 1, 1])
with col_v4:
    data["body_type"] = st.text_input("車体の形状", key="body_type")
with col_v5:
    data["maker_name"] = st.text_input("車名", key="maker_name")
with col_v6:
    data["model"] = st.text_input("型式", key="model")

# 行2: 車台番号、定員、積載量、重量、総重量、類別
col_v7, col_v8, col_v9 = st.columns(3)
with col_v7:
    data["chassis_number"] = st.text_input("車台番号", key="chassis_number")
with col_v8:
    data["classification_number"] = st.text_input("類別区分番号", key="classification_number")
with col_v9:
    data["capacity"] = st.text_input("乗車定員", key="capacity")

col_v10, col_v11, col_v12 = st.columns(3)
with col_v10:
    data["vehicle_weight"] = st.text_input("車両重量", key="vehicle_weight")
with col_v11:
    data["gross_weight"] = st.text_input("車両総重量", key="gross_weight")
with col_v12:
    data["max_loading"] = st.text_input("最大積載量", key="max_loading")

# 行3: 原動機、寸法、排気量、燃料
st.caption("詳細スペック")
col_v13, col_v14, col_v15, col_v16 = st.columns(4)
with col_v13:
    data["engine_model"] = st.text_input("原動機の型式", key="engine_model")
with col_v14:
    data["length"] = st.text_input("長さ(cm)", key="length")
with col_v15:
    data["width"] = st.text_input("幅(cm)", key="width")
with col_v16:
    data["height"] = st.text_input("高さ(cm)", key="height")

col_v17, col_v18, col_v19 = st.columns(3)
with col_v17:
    data["displacement"] = st.text_input("総排気量(L)", key="displacement")
with col_v18:
    data["fuel_code"] = st.text_input("燃料(1:ガソリン...)", key="fuel_code")
with col_v19:
    data["rotor_count"] = st.text_input("ローター数", key="rotor_count")

# ============================================================
# 旧所有者・旧使用者・その他
# ============================================================
st.header("4. 旧所有者・旧使用者・その他")

col_o1, col_o2 = st.columns(2)
with col_o1:
    st.subheader("旧所有者")
    data["old_owner_address"] = st.text_input("住所", key="old_owner_address")
    data["old_owner_name"] = st.text_input("氏名", key="old_owner_name")
with col_o2:
    st.subheader("旧使用者")
    data["old_user_address"] = st.text_input("住所", key="old_user_address")
    data["old_user_name"] = st.text_input("氏名", key="old_user_name")

st.subheader("その他情報")
col_o3, col_o4, col_o5 = st.columns(3)
with col_o3:
    data["old_parking_place"] = st.text_input("主たる定置場（旧）", key="old_parking_place")
with col_o4:
    data["prev_usage_code"] = st.text_input("取得前の用途(コード)", key="prev_usage_code")
with col_o5:
    data["ownership_code"] = st.text_input("所有形態(コード)", key="ownership_code")

# ============================================================
# PDF生成
# ============================================================
st.markdown("---")
if st.button("📄 PDF作成", type="primary"):
    # 出力ファイル名
    if report_type == "発（転入）":
        output_filename = "car_tax_hatsu.pdf"
        template_path = "templates/20260208_自動車税(環境性能割種別割)申告害(報告害)発.pdf"
    else:
        output_filename = "car_tax_i.pdf"
        template_path = "templates/20260208_自動車税(環境性能割種別割)申告書(報告書)異.pdf"
        
    output_pdf = f"output/{output_filename}"
    
    try:
        # フィールドリスト生成
        fields = get_car_tax_field_list(data)
        
        # PDF生成
        if os.path.exists(template_path):
            # テンプレートPDFがある場合は重ね合わせ
            embed_text_to_pdf(template_path, output_pdf, fields, pagesize=PAGE_SIZE)
            st.success(f"✅ テンプレートを使用して {report_type}用PDFを作成しました！")
        else:
            # テンプレートがない場合は白紙
            create_blank_pdf_with_text(output_pdf, fields, pagesize=PAGE_SIZE)
            st.warning(f"⚠️ テンプレートが見つからないため白紙で作成しました: {template_path}")
            st.success(f"✅ {report_type}用PDF作成（白紙）")
        
        # ダウンロードボタン
        with open(output_pdf, "rb") as f:
            st.download_button(
                label="📥 PDFをダウンロード",
                data=f,
                file_name=output_filename,
                mime="application/pdf"
            )
            
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
        import traceback
        st.code(traceback.format_exc())
