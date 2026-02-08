# -*- coding: utf-8 -*-
"""
軽自動車税環境性能割（報告書）用 座標確認グリッドPDF生成

このスクリプトは、帳票に重ねて座標を特定するためのグリッドPDFを生成します。
50ptグリッドと10ptグリッドを描画し、座標値を表示します。

使い方:
1. このスクリプトを実行
2. 生成された output/kei_report_grid.pdf を開く
3. 帳票PDFと重ねて座標を読み取る
"""

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# PDFサイズ（軽自動車報告書: A4横向き相当）
PAGE_WIDTH = 841.2
PAGE_HEIGHT = 595.2

def generate_grid_pdf(output_path="output/kei_report_grid.pdf"):
    """座標確認用のグリッドPDFを生成"""
    
    c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # 背景を白に
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
    
    # 10ptグリッド（薄いグレー）
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(0.3)
    for x in range(0, int(PAGE_WIDTH) + 1, 10):
        c.line(x, 0, x, PAGE_HEIGHT)
    for y in range(0, int(PAGE_HEIGHT) + 1, 10):
        c.line(0, y, PAGE_WIDTH, y)
    
    # 50ptグリッド（グレー）
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.setLineWidth(0.5)
    for x in range(0, int(PAGE_WIDTH) + 1, 50):
        c.line(x, 0, x, PAGE_HEIGHT)
    for y in range(0, int(PAGE_HEIGHT) + 1, 50):
        c.line(0, y, PAGE_WIDTH, y)
    
    # 100ptグリッド（濃いグレー + ラベル）
    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.setLineWidth(1)
    c.setFont('HeiseiMin-W3', 8)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    
    for x in range(0, int(PAGE_WIDTH) + 1, 100):
        c.line(x, 0, x, PAGE_HEIGHT)
        # X座標ラベル（下端）
        c.drawString(x + 2, 5, f"X={x}")
        # X座標ラベル（上端）
        c.drawString(x + 2, PAGE_HEIGHT - 12, f"X={x}")
    
    for y in range(0, int(PAGE_HEIGHT) + 1, 100):
        c.line(0, y, PAGE_WIDTH, y)
        # Y座標ラベル（左端）
        c.drawString(5, y + 2, f"Y={y}")
        # Y座標ラベル（右端）
        c.drawString(PAGE_WIDTH - 40, y + 2, f"Y={y}")
    
    # 原点マーク（左下）
    c.setFillColorRGB(1, 0, 0)
    c.circle(0, 0, 5, stroke=0, fill=1)
    c.setFont('HeiseiMin-W3', 10)
    c.drawString(10, 15, "原点(0,0)")
    
    # ページサイズ表示
    c.setFillColorRGB(0, 0, 0)
    c.setFont('HeiseiMin-W3', 12)
    c.drawString(PAGE_WIDTH / 2 - 100, PAGE_HEIGHT - 30, 
                 f"軽自動車報告書 座標グリッド ({PAGE_WIDTH} x {PAGE_HEIGHT} pt)")
    
    # 座標読み取りガイド
    c.setFont('HeiseiMin-W3', 10)
    c.drawString(50, 40, "【使い方】帳票PDFと重ねて、追加したいフィールドの位置のX座標とY座標を読み取ってください")
    
    c.save()
    print(f"✅ グリッドPDFを生成しました: {output_path}")
    print(f"   サイズ: {PAGE_WIDTH} x {PAGE_HEIGHT} pt")
    print("")
    print("📋 次のステップ:")
    print("   1. output/kei_report_grid.pdf を開く")
    print("   2. 帳票PDFと重ねて確認")
    print("   3. 「主たる定置場」欄のX座標とY座標を読み取る")
    print("   4. 読み取った座標を教えてください")

if __name__ == "__main__":
    generate_grid_pdf()
