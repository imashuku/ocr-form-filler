import io
from typing import List, Dict, Union
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter

# 日本語フォントの登録 (HeiseiMin-W3 は標準的な日本語フォントの一つです)
# これにより、PDF生成時に日本語が文字化けせずに表示されます
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def create_overlay_pdf(fields: List[Dict[str, Union[str, int, float]]], pagesize=letter) -> io.BytesIO:
    """
    指定された座標にテキストを配置した、透明なPDFページを作成します。
    
    Args:
        fields: 以下のキーを持つ辞書のリスト:
            - text: 挿入するテキスト。
            - x: X座標 (ポイント単位, 左下原点)。
            - y: Y座標 (ポイント単位, 左下原点)。
            - font_size: (オプション) フォントサイズ (デフォルト: 12)。
            - font_name: (オプション) フォント名 (デフォルト: "HeiseiMin-W3")。
        pagesize: ページのサイズ (デフォルト: letter)。 A4 や landscape(A4) などを指定可能。

    Returns:
        io.BytesIO: 生成されたPDFデータを含む BytesIO オブジェクト。
    """
    packet = io.BytesIO()
    # Reportlabで新しいPDFを作成
    can = canvas.Canvas(packet, pagesize=pagesize)
    
    for field in fields:
        field_type = field.get('type', 'text')
        
        can.saveState()
        
        if field_type == 'text':
            text = field.get('text', '')
            x = field.get('x', 0)
            y = field.get('y', 0)
            font_size = field.get('font_size', 12)
            font_name = field.get('font_name', 'HeiseiMin-W3')
            rotation = field.get('rotate', 0)

            can.translate(x, y)
            if rotation:
                can.rotate(rotation)
            
            can.setFont(font_name, font_size)
            can.drawString(0, 0, str(text))
            
        elif field_type == 'rect':
            x = field.get('x', 0)
            y = field.get('y', 0)
            w = field.get('width', 0)
            h = field.get('height', 0)
            stroke = field.get('stroke', 0)
            fill = field.get('fill', 1)
            
            # 矩形を描画 (fill=1 で塗りつぶし)
            can.rect(x, y, w, h, stroke=stroke, fill=fill)

        can.restoreState()
        
    can.save()
    packet.seek(0)
    return packet

def embed_text_to_pdf(
    source_pdf_path: str,
    output_pdf_path: str,
    fields: List[Dict[str, Union[str, int, float]]],
    page_indices: List[int] = None,
    pagesize=letter
):
    """
    既存のPDFにテキストを重ねて、新しいPDFとして保存します。

    Args:
        source_pdf_path: 入力元のPDFファイルのパス。
        output_pdf_path: 保存先のPDFファイルのパス。
        fields:埋め込むテキスト情報のリスト (create_overlay_pdf 参照)。
        page_indices: (オプション) テキストを埋め込むページのインデックス(0始まり)のリスト。
                      Noneの場合はすべてのページに埋め込みます。
        pagesize: オーバーレイPDFのサイズ (デフォルト: letter)。
                  A4横向きの場合は landscape(A4) を指定します。
    """
    try:
        # オーバーレイ用のPDFを作成
        overlay_pdf_stream = create_overlay_pdf(fields, pagesize=pagesize)
        overlay_pdf = PdfReader(overlay_pdf_stream)
        overlay_page = overlay_pdf.pages[0]

        # 元のPDFを読み込む
        source_pdf = PdfReader(source_pdf_path)
        writer = PdfWriter()

        for i, page in enumerate(source_pdf.pages):
            # page_indicesが指定されている場合、そのページのみ処理する
            if page_indices is None or i in page_indices:
                # ページの結合（元のページの上にオーバーレイを重ねる）
                page.merge_page(overlay_page)
            
            writer.add_page(page)

        # ファイルに書き出し
        with open(output_pdf_path, "wb") as f:
            writer.write(f)

        print(f"成功: PDFファイルを保存しました -> {output_pdf_path}")
        return True

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

def create_blank_pdf_with_text(
    output_pdf_path: str,
    fields: List[Dict[str, Union[str, int, float]]],
    pagesize=(595, 836)
):
    """
    白紙のPDF上にテキストのみを配置して保存します。
    （既存PDFへのオーバーレイではなく、テキストのみの印刷用）

    Args:
        output_pdf_path: 保存先のPDFファイルのパス。
        fields: 埋め込むテキスト情報のリスト (create_overlay_pdf 参照)。
        pagesize: ページのサイズ (デフォルト: (595, 836) - ユーザー指定サイズ)。
    """
    try:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=pagesize)
        
        # 白背景を描画
        can.setFillColorRGB(1, 1, 1)  # 白
        can.rect(0, 0, pagesize[0], pagesize[1], stroke=0, fill=1)
        can.setFillColorRGB(0, 0, 0)  # 黒に戻す
        
        for field in fields:
            field_type = field.get('type', 'text')
            
            can.saveState()
            
            if field_type == 'text':
                text = field.get('text', '')
                x = field.get('x', 0)
                y = field.get('y', 0)
                font_size = field.get('font_size', 12)
                font_name = field.get('font_name', 'HeiseiMin-W3')
                rotation = field.get('rotate', 0)

                can.translate(x, y)
                if rotation:
                    can.rotate(rotation)
                
                can.setFont(font_name, font_size)
                can.drawString(0, 0, str(text))
                
            elif field_type == 'rect':
                x = field.get('x', 0)
                y = field.get('y', 0)
                w = field.get('width', 0)
                h = field.get('height', 0)
                stroke = field.get('stroke', 0)
                fill = field.get('fill', 1)
                can.rect(x, y, w, h, stroke=stroke, fill=fill)

            can.restoreState()
            
        can.save()
        packet.seek(0)
        
        # ファイルに書き出し
        with open(output_pdf_path, "wb") as f:
            f.write(packet.getvalue())
        
        print(f"成功: 白紙PDFファイルを保存しました -> {output_pdf_path}")
        return True

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False
