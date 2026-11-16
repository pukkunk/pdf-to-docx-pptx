# pdf_to_pptx.py

from pptx import Presentation
from pptx.util import Pt

from pdf_converter_common import (
    execute_converter,
    render_pdf_pages,
)


def convert_to_pptx(
    pdf,
    output_path,
    width_pt,
    height_pt,
    dpi
):
    """PDFをPowerPointに変換する"""

    prs = Presentation()

    # PDFと同じサイズに設定
    prs.slide_width = Pt(width_pt)
    prs.slide_height = Pt(height_pt)

    # 空白レイアウト
    blank_layout = prs.slide_layouts[6]

    for page_number, image in enumerate(
        render_pdf_pages(pdf, dpi),
        start=1
    ):
        slide = prs.slides.add_slide(blank_layout)

        # PDFページ画像をスライド全面に配置
        slide.shapes.add_picture(
            image_to_stream(image),
            left=0,
            top=0,
            width=Pt(width_pt),
            height=Pt(height_pt)
        )

        print(f"PowerPoint: {page_number}ページ目")

    prs.save(str(output_path))


def image_to_stream(image):
    """PIL画像をメモリ上のPNGストリームに変換"""
    from io import BytesIO

    stream = BytesIO()
    image.save(stream, format="PNG")
    stream.seek(0)

    return stream


def main():
    return execute_converter(
        script_path=__file__,
        description="PDF to PowerPoint Converter",
        output_ext=".pptx",
        converter=convert_to_pptx
    )


if __name__ == "__main__":
    raise SystemExit(main())
