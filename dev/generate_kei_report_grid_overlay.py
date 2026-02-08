# -*- coding: utf-8 -*-
"""
軽自動車税環境性能割（報告書）用 座標確認グリッドPDF生成（画像オーバーレイ版）

テンプレート画像の上にグリッドを重ねて表示します。
"""

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import ImageReader

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# PDFサイズ（軽自動車報告書: A4横向き相当）
PAGE_WIDTH = 841.2
PAGE_HEIGHT = 595.2

def generate_grid_overlay_pdf(
    image_path="templates/kei_report_page4_final.png",
    output_path="output/kei_report_grid_overlay.pdf"
):
    """テンプレート画像にグリッドを重ねたPDFを生成"""
    
    c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # 背景画像を描画
    try:
        img = ImageReader(image_path)
        c.drawImage(img, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
        print(f"✅ 画像を読み込みました: {image_path}")
    except Exception as e:
        print(f"⚠️ 画像読み込みエラー: {e}")
        # 画像がなくても続行（白背景）
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
    
    # 10ptグリッド（薄い赤）
    c.setStrokeColorRGB(1, 0.7, 0.7, 0.3)
    c.setLineWidth(0.2)
    for x in range(0, int(PAGE_WIDTH) + 1, 10):
        c.line(x, 0, x, PAGE_HEIGHT)
    for y in range(0, int(PAGE_HEIGHT) + 1, 10):
        c.line(0, y, PAGE_WIDTH, y)
    
    # 50ptグリッド（赤）
    c.setStrokeColorRGB(1, 0.3, 0.3, 0.5)
    c.setLineWidth(0.5)
    for x in range(0, int(PAGE_WIDTH) + 1, 50):
        c.line(x, 0, x, PAGE_HEIGHT)
    for y in range(0, int(PAGE_HEIGHT) + 1, 50):
        c.line(0, y, PAGE_WIDTH, y)
    
    # 100ptグリッド（濃い赤 + ラベル）
    c.setStrokeColorRGB(1, 0, 0, 0.8)
    c.setLineWidth(1)
    c.setFont('HeiseiMin-W3', 7)
    
    for x in range(0, int(PAGE_WIDTH) + 1, 100):
        c.line(x, 0, x, PAGE_HEIGHT)
        # X座標ラベル（下端）- 白背景付き
        c.setFillColorRGB(1, 1, 1)
        c.rect(x + 1, 2, 28, 10, stroke=0, fill=1)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(x + 2, 4, f"X={x}")
        # X座標ラベル（上端）
        c.setFillColorRGB(1, 1, 1)
        c.rect(x + 1, PAGE_HEIGHT - 14, 28, 10, stroke=0, fill=1)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(x + 2, PAGE_HEIGHT - 12, f"X={x}")
    
    for y in range(0, int(PAGE_HEIGHT) + 1, 100):
        c.line(0, y, PAGE_WIDTH, y)
        # Y座標ラベル（左端）- 白背景付き
        c.setFillColorRGB(1, 1, 1)
        c.rect(2, y + 1, 28, 10, stroke=0, fill=1)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(4, y + 2, f"Y={y}")
        # Y座標ラベル（右端）
        c.setFillColorRGB(1, 1, 1)
        c.rect(PAGE_WIDTH - 32, y + 1, 30, 10, stroke=0, fill=1)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(PAGE_WIDTH - 30, y + 2, f"Y={y}")
    
    # 原点マーク（左下）
    c.setFillColorRGB(0, 0, 1)
    c.circle(0, 0, 5, stroke=0, fill=1)
    
    c.save()
    print(f"✅ グリッドオーバーレイPDFを生成しました: {output_path}")
    print("")
    print("📋 座標の読み取り方:")
    print("   - X座標: 左端が0、右に行くほど大きい（最大 約841）")
    print("   - Y座標: 下端が0、上に行くほど大きい（最大 約595）")
    print("")
    print("📍 「主たる定置場」欄のX座標とY座標を読み取って教えてください！")

if __name__ == "__main__":
    generate_grid_overlay_pdf()
