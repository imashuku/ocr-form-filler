# OCR申請書作成アプリ

車両登録用OCR帳票（第1号様式）のテキスト入力・PDF生成を行うStreamlitアプリケーションです。

## 機能

- 車両情報（地域名、分類番号、かな、一連指定番号）の入力
- 車台番号（ローマ字自動マーク付き）
- 所有者・使用者情報
- 旧所有者・代理人・受検者情報
- 各種フラグ（同上マーク等）
- 白紙PDFへのテキスト出力

## 使い方

1. 各フィールドに情報を入力
2. 「PDF作成」ボタンをクリック
3. 生成されたPDFをダウンロード

## ローカル実行

```bash
pip install -r requirements.txt
streamlit run ocr_app.py
```

## ライセンス

Private - Step Out Marketing LLC
