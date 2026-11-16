# pdf_converter_common.py

import argparse
import configparser
import sys
from pathlib import Path

DEFAULT_DPI = 300
PAGE_SIZE_TOLERANCE = 0.01


def create_argument_parser(description):
    """Common command-line arguments."""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "input",
        help="Input PDF file"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file (default: same folder as input PDF)"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"Image resolution (default: {DEFAULT_DPI} DPI)"
    )

    return parser


def load_config(script_path):
    """
    Place the INI file in the same folder as the script.
    Create it with overwrite=0 if it does not exist.
    """
    script_path = Path(script_path)

    ini_path = script_path.with_name(
        script_path.stem + ".ini"
    )

    config = configparser.ConfigParser()

    if not ini_path.exists():
        config["DEFAULT"] = {
            "overwrite": "0"
        }

        with ini_path.open("w", encoding="utf-8") as f:
            config.write(f)

        print(f"Created INI file: {ini_path}")

    config.read(ini_path, encoding="utf-8")

    value = config.get(
        "DEFAULT",
        "overwrite",
        fallback="0"
    ).strip()

    if value not in ("0", "1"):
        raise ValueError(
            f"Invalid overwrite setting in INI file: {value}"
        )

    return value == "1"


def prepare_paths(input_arg, output_arg, output_ext):
    """Validate input and output paths."""

    input_path = Path(input_arg).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Input path is not a regular file: {input_path}"
        )

    if input_path.suffix.lower() != ".pdf":
        raise ValueError("Input file must be a PDF.")

    if output_arg:
        output_path = Path(output_arg).expanduser().resolve()

        if output_path.suffix.lower() != output_ext:
            raise ValueError(
                f"Output file extension must be {output_ext}."
            )
    else:
        output_path = input_path.with_suffix(output_ext)

    if output_path == input_path:
        raise ValueError("Input and output files must be different.")

    if not output_path.parent.exists():
        raise FileNotFoundError(
            f"Output directory does not exist: {output_path.parent}"
        )

    return input_path, output_path


def check_output_permission(output_path, overwrite):
    """Check whether the output file can be overwritten."""

    if output_path.exists() and not overwrite:
        raise FileExistsError(
            "Output file already exists. Overwriting is disabled.\n"
            f"File: {output_path}\n"
            "Set overwrite=1 in the INI file to allow overwriting."
        )


def inspect_pdf(pdf_path):
    """
    Inspect all PDF pages.
    Verify that all pages have the same dimensions.

    Returns:
        pdfium.PdfDocument
        Page width (pt)
        Page height (pt)
    """

    try:
        import pypdfium2 as pdfium
    except ImportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print(
            "Install the required library using:",
            file=sys.stderr
        )
        print(
            "    uv add pypdfium2",
            file=sys.stderr
        )
        raise SystemExit(1)

    pdf = pdfium.PdfDocument(str(pdf_path))

    if len(pdf) == 0:
        pdf.close()
        raise ValueError("The PDF contains no pages.")

    first_page = pdf[0]

    try:
        width, height = first_page.get_size()
    finally:
        first_page.close()

    for index in range(1, len(pdf)):
        page = pdf[index]

        try:
            current_width, current_height = page.get_size()
        finally:
            page.close()

        if (
            abs(width - current_width) > PAGE_SIZE_TOLERANCE
            or abs(height - current_height) > PAGE_SIZE_TOLERANCE
        ):
            pdf.close()

            raise ValueError(
                "PDF page dimensions are inconsistent.\n"
                f"Page 1: {width:.3f} x {height:.3f} pt\n"
                f"Page {index + 1}: "
                f"{current_width:.3f} x {current_height:.3f} pt\n"
                "Only PDFs with identical page dimensions are supported."
            )

    return pdf, width, height


def render_pdf_pages(pdf, dpi):
    """Generate images from all PDF pages."""

    if dpi <= 0:
        raise ValueError("DPI must be greater than or equal to 1.")

    scale = dpi / 72.0

    for index in range(len(pdf)):
        page = pdf[index]

        try:
            bitmap = page.render(scale=scale)

            try:
                yield bitmap.to_pil().convert("RGB")
            finally:
                bitmap.close()

        finally:
            page.close()


def execute_converter(
    script_path,
    description,
    output_ext,
    converter,
    version,
    copyright,
    author
):
    """Common conversion process."""

    parser = create_argument_parser(description)

    args = parser.parse_args()

    try:
        if args.dpi <= 0:
            raise ValueError("--dpi must be greater than or equal to 1.")

        overwrite = load_config(script_path)

        input_path, output_path = prepare_paths(
            args.input,
            args.output,
            output_ext
        )

        check_output_permission(
            output_path,
            overwrite
        )

        pdf, width_pt, height_pt = inspect_pdf(input_path)

        try:
            print(f"Input PDF : {input_path}")
            print(f"Output    : {output_path}")
            print(f"Pages     : {len(pdf)}")
            print(
                f"Page size : {width_pt:.3f} x "
                f"{height_pt:.3f} pt"
            )
            print(f"Resolution: {args.dpi} DPI")

            converter(
                pdf,
                output_path,
                width_pt,
                height_pt,
                args.dpi
            )

        finally:
            pdf.close()

        print(f"Conversion completed: {output_path}")

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0
