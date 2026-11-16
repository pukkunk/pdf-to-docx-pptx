# coding: utf-8
# Copyright (c) 2026 pukkunk
# pdf_to_pptx.py

import platform

try:
    from pptx import Presentation
    from pptx.util import Pt
except ImportError as e:
    print(f"ERROR: {e}")
    print("Install the required library using:")
    print("    uv add python-pptx")
    raise SystemExit(1)

from pdf_converter_common import (
    execute_converter,
    render_pdf_pages,
)


__version_short__ = (
    f"0.0.2, python={platform.python_version()} "
    f"{platform.architecture()[0]}"
)
__version__ = f"{__version_short__}\n"
__copyright__ = "pukkunk"
__author__ = "pukkunk"


def main() -> int:
    return execute_converter(
        script_path=__file__,
        description="PDF to PowerPoint Converter.\n",
        output_ext=".pptx",
        converter=convert_to_pptx,
        version=__version__,
        copyright=__copyright__,
        author=__author__
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


if __name__ == "__main__":
    raise SystemExit(main())
