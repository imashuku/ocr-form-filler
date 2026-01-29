# -*- coding: utf-8 -*-
"""
OCR申請書作成アプリ - メインエントリポイント

Streamlit Multi-page App
- 普通乗用車（第1号様式）
- 軽自動車（環境性能割報告書）
"""

import streamlit as st

st.set_page_config(
    page_title="OCR申請書作成",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 OCR申請書作成アプリ")

st.markdown("""
## 書類を選択してください

👈 左のサイドバーからフォームを選んでください。

---

### 対応している書類

| 書類 | 説明 |
|------|------|
| **普通乗用車 OCR申請書** | 第1号様式（移転登録等） |
| **軽自動車 報告書** | 軽自動車税環境性能割（報告書） |

---

### 今後の予定

- 📷 **車検証スキャン** - スマホカメラで車検証を読み取り、自動入力
- 📷 **印鑑証明スキャン** - 住所・氏名を自動入力
""")

# session_state の初期化（将来のOCRデータ用）
if "form_data" not in st.session_state:
    st.session_state.form_data = None
    
if "ocr_result" not in st.session_state:
    st.session_state.ocr_result = None
