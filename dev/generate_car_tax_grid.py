# -*- coding: utf-8 -*-
"""
自動車税申告書（発・異）用 座標確認グリッドPDF生成

テンプレートPDFにグリッドを重ねて表示します。
"""

import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def generate_grid_overlay_on_pdf(
    input_pdf_path: str,
    output_path: str,
    grid_color=(1, 0, 0)  # 赤
):
    """既存PDFにグリッドを重ねたPDFを生成"""
    
    # 元PDFを読み込み
    reader = PdfReader(input_pdf_path)
    page = reader.pages[0]
    
    # ページサイズ取得
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    
    print(f"📄 PDF読み込み: {input_pdf_path}")
    print(f"   サイズ: {width:.1f} x {height:.1f} pt")
    
    # グリッドオーバーレイ作成
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    
    # 10ptグリッド（薄い色）
    c.setStrokeColorRGB(grid_color[0], grid_color[1], grid_color[2], 0.2)
    c.setLineWidth(0.2)
    for x in range(0, int(width) + 1, 10):
        c.line(x, 0, x, height)
    for y in range(0, int(height) + 1, 10):
        c.line(0, y, width, y)
    
    # 50ptグリッド（中程度）
    c.setStrokeColorRGB(grid_color[0], grid_color[1], grid_color[2], 0.4)
    c.setLineWidth(0.4)
    for x in range(0, int(width) + 1, 50):
        c.line(x, 0, x, height)
    for y in range(0, int(height) + 1, 50):
        c.line(0, y, width, y)
    
    # 100ptグリッド（濃い + ラベル）
    c.setStrokeColorRGB(grid_color[0], grid_color[1], grid_color[2], 0.8)
    c.setLineWidth(1)
    c.setFont('HeiseiMin-W3', 7)
    
    for x in range(0, int(width) + 1, 100):
        c.line(x, 0, x, height)
        # X座標ラベル（白背景付き）
        c.setFillColorRGB(1, 1, 1)
        c.rect(x + 1, 2, 30, 10, stroke=0, fill=1)
        c.rect(x + 1, height - 14, 30, 10, stroke=0, fill=1)
        c.setFillColorRGB(grid_color[0], grid_color[1], grid_color[2])
        c.drawString(x + 2, 4, f"X={x}")
        c.drawString(x + 2, height - 12, f"X={x}")
    
    for y in range(0, int(height) + 1, 100):
        c.line(0, y, width, y)
        # Y座標ラベル（白背景付き）
        c.setFillColorRGB(1, 1, 1)
        c.rect(2, y + 1, 30, 10, stroke=0, fill=1)
        c.rect(width - 34, y + 1, 32, 10, stroke=0, fill=1)
        c.setFillColorRGB(grid_color[0], grid_color[1], grid_color[2])
        c.drawString(4, y + 2, f"Y={y}")
        c.drawString(width - 32, y + 2, f"Y={y}")
    
    # 原点マーク
    c.setFillColorRGB(0, 0, 1)
    c.circle(0, 0, 5, stroke=0, fill=1)
    
    c.save()
    packet.seek(0)
    
    # オーバーレイPDFを読み込み
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]
    
    # 元ページにオーバーレイをマージ
    page.merge_page(overlay_page)
    
    # 出力
    writer = PdfWriter()
    writer.add_page(page)
    
    with open(output_path, "wb") as f:
        writer.write(f)
    
    print(f"✅ グリッドオーバーレイPDF生成: {output_path}")


if __name__ == "__main__":
    # 発（転入用）
    generate_grid_overlay_on_pdf(
        "templates/20260208_自動車税(環境性能割種別割)申告害(報告害)発.pdf",
        "output/car_tax_hatsu_grid.pdf",
        grid_color=(1, 0, 0)  # 赤
    )
    
    # 異（異動用）
    generate_grid_overlay_on_pdf(
        "templates/20260208_自動車税(環境性能割種別割)申告書(報告書)異.pdf",
        "output/car_tax_i_grid.pdf",
        grid_color=(0, 0, 1)  # 青
    )
    
    print("")
    print("📋 座標の読み取り方:")
    print("   - X座標: 左端が0、右に行くほど大きい")
    print("   - Y座標: 下端が0、上に行くほど大きい")
    print("")
    print("📍 各フィールドのX座標とY座標を読み取って教えてください！")
