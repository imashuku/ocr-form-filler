#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF傾き補正スクリプト
指定したページの傾きを検出して補正し、新しいPDFとして保存します。
"""

import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import sys
import os

def detect_skew_angle(image):
    """
    画像の傾き角度を検出する
    """
    # グレースケール変換
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # エッジ検出
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # ハフ変換で直線検出
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is None:
        return 0
    
    # 各直線の角度を計算
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        # 水平に近い線のみを対象（±45度以内）
        if abs(angle) < 45:
            angles.append(angle)
    
    if not angles:
        return 0
    
    # 中央値を返す（外れ値の影響を減らす）
    return np.median(angles)

def deskew_image(image, angle):
    """
    画像を指定した角度で回転補正する
    """
    # PIL画像をnumpy配列に変換
    img_array = np.array(image)
    
    # 画像の中心を計算
    h, w = img_array.shape[:2]
    center = (w // 2, h // 2)
    
    # 回転行列を作成
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # アフィン変換を適用（背景は白で埋める）
    rotated = cv2.warpAffine(img_array, rotation_matrix, (w, h), 
                              borderMode=cv2.BORDER_CONSTANT, 
                              borderValue=(255, 255, 255))
    
    return Image.fromarray(rotated)

def deskew_pdf_page(input_pdf, page_number, output_path, dpi=300):
    """
    PDFの指定ページを傾き補正して保存する
    
    Args:
        input_pdf: 入力PDFのパス
        page_number: ページ番号（1始まり）
        output_path: 出力画像/PDFのパス
        dpi: 解像度
    """
    print(f"PDFを読み込み中: {input_pdf}")
    
    # PDFをページごとに画像に変換
    pages = convert_from_path(input_pdf, dpi=dpi)
    
    if page_number < 1 or page_number > len(pages):
        print(f"エラー: ページ番号 {page_number} は範囲外です（1-{len(pages)}）")
        return False
    
    # 指定ページを取得（0始まりインデックス）
    page_image = pages[page_number - 1]
    
    print(f"ページ {page_number} の傾きを検出中...")
    angle = detect_skew_angle(page_image)
    print(f"検出された傾き角度: {angle:.2f}度")
    
    if abs(angle) < 0.1:
        print("傾きはほぼありません。補正不要です。")
        page_image.save(output_path)
    else:
        print(f"傾きを補正中（{-angle:.2f}度回転）...")
        corrected = deskew_image(page_image, angle)
        corrected.save(output_path)
    
    print(f"保存完了: {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用法: python deskew_pdf.py <入力PDF> <ページ番号> [出力ファイル]")
        print("例: python deskew_pdf.py input.pdf 4 output.png")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    page_number = int(sys.argv[2])
    output_path = sys.argv[3] if len(sys.argv) > 3 else f"page_{page_number}_corrected.png"
    
    deskew_pdf_page(input_pdf, page_number, output_path)
