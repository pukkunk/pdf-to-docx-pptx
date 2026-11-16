# pdf_to_docx.py

from copy import deepcopy
from io import BytesIO

from docx import Document
from docx.enum.section import WD_SECTION
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from pdf_converter_common import (
    execute_converter,
    render_pdf_pages,
)


def set_picture_behind_text(
    paragraph,
    image_stream,
    width_pt,
    height_pt
):
    """
    Word画像をページ左上基準の絶対位置に配置し、
    文字の背面に設定する。
    """

    run = paragraph.add_run()

    picture = run.add_picture(
        image_stream,
        width=Pt(width_pt),
        height=Pt(height_pt)
    )

    inline = picture._inline

    anchor = OxmlElement("wp:anchor")

    anchor.set("distT", "0")
    anchor.set("distB", "0")
    anchor.set("distL", "0")
    anchor.set("distR", "0")
    anchor.set("simplePos", "0")
    anchor.set("relativeHeight", "0")
    anchor.set("behindDoc", "1")
    anchor.set("locked", "0")
    anchor.set("layoutInCell", "1")
    anchor.set("allowOverlap", "1")

    # 単純位置
    simple_pos = OxmlElement("wp:simplePos")
    simple_pos.set("x", "0")
    simple_pos.set("y", "0")
    anchor.append(simple_pos)

    # 水平方向
    position_h = OxmlElement("wp:positionH")
    position_h.set("relativeFrom", "page")

    pos_offset_h = OxmlElement("wp:posOffset")
    pos_offset_h.text = "0"

    position_h.append(pos_offset_h)
    anchor.append(position_h)

    # 垂直方向
    position_v = OxmlElement("wp:positionV")
    position_v.set("relativeFrom", "page")

    pos_offset_v = OxmlElement("wp:posOffset")
    pos_offset_v.text = "0"

    position_v.append(pos_offset_v)
    anchor.append(position_v)

    # サイズ
    anchor.append(deepcopy(inline.extent))

    # 効果範囲
    effect_extent = OxmlElement("wp:effectExtent")
    effect_extent.set("l", "0")
    effect_extent.set("t", "0")
    effect_extent.set("r", "0")
    effect_extent.set("b", "0")
    anchor.append(effect_extent)

    # テキスト回り込みなし
    anchor.append(OxmlElement("wp:wrapNone"))

    # 図形情報
    anchor.append(deepcopy(inline.docPr))

    # cNvGraphicFramePrを新規作成
    c_nv = OxmlElement("wp:cNvGraphicFramePr")
    anchor.append(c_nv)

    # 画像本体
    anchor.append(deepcopy(inline.graphic))

    # inline画像をanchor画像に置き換える
    inline.getparent().replace(inline, anchor)

def clear_header(header):
    """ヘッダーの既存内容をクリア"""

    for paragraph in header.paragraphs:
        paragraph.clear()


def convert_to_docx(
    pdf,
    output_path,
    width_pt,
    height_pt,
    dpi
):
    """PDFをWordに変換する"""

    doc = Document()

    for page_number, image in enumerate(
        render_pdf_pages(pdf, dpi),
        start=1
    ):

        if page_number == 1:
            section = doc.sections[0]
        else:
            section = doc.add_section(
                WD_SECTION.NEW_PAGE
            )

        # ページサイズをPDFと同じにする
        section.page_width = Pt(width_pt)
        section.page_height = Pt(height_pt)

        # 余白を0に設定
        section.top_margin = Pt(0)
        section.bottom_margin = Pt(0)
        section.left_margin = Pt(0)
        section.right_margin = Pt(0)

        section.header_distance = Pt(0)
        section.footer_distance = Pt(0)

        # セクションごとに独立したヘッダーを設定
        section.header.is_linked_to_previous = False

        header = section.header
        clear_header(header)

        paragraph = header.paragraphs[0]

        # 背景画像を設定
        stream = BytesIO()
        image.save(stream, format="PNG")
        stream.seek(0)

        set_picture_behind_text(
            paragraph,
            stream,
            width_pt,
            height_pt
        )

        print(f"Word: {page_number}ページ目")

    doc.save(str(output_path))


def main():
    return execute_converter(
        script_path=__file__,
        description="PDF to Word Converter",
        output_ext=".docx",
        converter=convert_to_docx
    )


if __name__ == "__main__":
    raise SystemExit(main())
