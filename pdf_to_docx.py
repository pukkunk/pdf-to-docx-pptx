# coding: utf-8
# Copyright (c) 2026 pukkunk
# pdf_to_docx.py

from copy import deepcopy
from io import BytesIO
import platform

try:
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.shared import Pt
    from docx.oxml import OxmlElement
except ImportError as e:
    print(f"ERROR: {e}")
    print("Install the required library using:")
    print("    uv add python-docx")
    raise SystemExit(1)

from pdf_converter_common import (
    execute_converter,
    render_pdf_pages,
)


__version_short__ = (
    f"0.0.1, python={platform.python_version()} "
    f"{platform.architecture()[0]}"
)
__version__ = f"{__version_short__}\n"
__copyright__ = "pukkunk"
__author__ = "pukkunk"


def main() -> int:
    return execute_converter(
        script_path=__file__,
        description="PDF to Word Converter\n",
        output_ext=".docx",
        converter=convert_to_docx,
        version=__version__,
        copyright=__copyright__,
        author=__author__
    )


def set_picture_behind_text(
    paragraph,
    image_stream,
    width_pt,
    height_pt
):
    """
    Place a Word image at an absolute position relative to the
    top-left corner of the page, behind the text.
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

    # Simple position
    simple_pos = OxmlElement("wp:simplePos")
    simple_pos.set("x", "0")
    simple_pos.set("y", "0")
    anchor.append(simple_pos)

    # Horizontal position
    position_h = OxmlElement("wp:positionH")
    position_h.set("relativeFrom", "page")

    pos_offset_h = OxmlElement("wp:posOffset")
    pos_offset_h.text = "0"

    position_h.append(pos_offset_h)
    anchor.append(position_h)

    # Vertical position
    position_v = OxmlElement("wp:positionV")
    position_v.set("relativeFrom", "page")

    pos_offset_v = OxmlElement("wp:posOffset")
    pos_offset_v.text = "0"

    position_v.append(pos_offset_v)
    anchor.append(position_v)

    # Size
    anchor.append(deepcopy(inline.extent))

    # Effect extent
    effect_extent = OxmlElement("wp:effectExtent")
    effect_extent.set("l", "0")
    effect_extent.set("t", "0")
    effect_extent.set("r", "0")
    effect_extent.set("b", "0")
    anchor.append(effect_extent)

    # No text wrapping
    anchor.append(OxmlElement("wp:wrapNone"))

    # Drawing properties
    anchor.append(deepcopy(inline.docPr))

    # Create a new cNvGraphicFramePr element
    c_nv = OxmlElement("wp:cNvGraphicFramePr")
    anchor.append(c_nv)

    # Image content
    anchor.append(deepcopy(inline.graphic))

    # Replace the inline image with the anchored image
    inline.getparent().replace(inline, anchor)


def clear_header(header):
    """Clear existing header content."""

    for paragraph in header.paragraphs:
        paragraph.clear()


def convert_to_docx(
    pdf,
    output_path,
    width_pt,
    height_pt,
    dpi
):
    """Convert PDF to Word."""

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

        # Set the page size to match the PDF
        section.page_width = Pt(width_pt)
        section.page_height = Pt(height_pt)

        # Set all margins to zero
        section.top_margin = Pt(0)
        section.bottom_margin = Pt(0)
        section.left_margin = Pt(0)
        section.right_margin = Pt(0)

        section.header_distance = Pt(0)
        section.footer_distance = Pt(0)

        # Use an independent header for each section
        section.header.is_linked_to_previous = False

        header = section.header
        clear_header(header)

        paragraph = header.paragraphs[0]

        # Set the background image
        stream = BytesIO()
        image.save(stream, format="PNG")
        stream.seek(0)

        set_picture_behind_text(
            paragraph,
            stream,
            width_pt,
            height_pt
        )

        print(f"Word: Page {page_number}")

    doc.save(str(output_path))


if __name__ == "__main__":
    raise SystemExit(main())
