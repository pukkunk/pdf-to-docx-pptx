# pdf_converter_common.py

import argparse
import configparser
import sys
from pathlib import Path

import pypdfium2 as pdfium


DEFAULT_DPI = 300
PAGE_SIZE_TOLERANCE = 0.01


def create_argument_parser(description):
    """共通コマンドライン引数"""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "input",
        help="入力PDFファイル"
    )

    parser.add_argument(
        "-o", "--output",
        help="出力ファイル（省略時は入力PDFと同じフォルダ）"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"画像解像度（デフォルト: {DEFAULT_DPI} DPI）"
    )

    return parser


def load_config(script_path):
    """
    スクリプトと同じフォルダにINIを配置する。
    初回起動時は overwrite=0 で作成する。
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

        print(f"INIファイルを作成しました: {ini_path}")

    config.read(ini_path, encoding="utf-8")

    value = config.get(
        "DEFAULT",
        "overwrite",
        fallback="0"
    ).strip()

    if value not in ("0", "1"):
        raise ValueError(
            f"INIファイルのoverwrite設定が不正です: {value}"
        )

    return value == "1"


def prepare_paths(input_arg, output_arg, output_ext):
    """入力・出力パスの検証"""

    input_path = Path(input_arg).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(
            f"入力ファイルが存在しません: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"入力ファイルが通常のファイルではありません: {input_path}"
        )

    if input_path.suffix.lower() != ".pdf":
        raise ValueError("入力ファイルはPDFを指定してください。")

    if output_arg:
        output_path = Path(output_arg).expanduser().resolve()

        if output_path.suffix.lower() != output_ext:
            raise ValueError(
                f"出力ファイルの拡張子は {output_ext} にしてください。"
            )
    else:
        output_path = input_path.with_suffix(output_ext)

    if output_path == input_path:
        raise ValueError("入力ファイルと出力ファイルが同じです。")

    if not output_path.parent.exists():
        raise FileNotFoundError(
            f"出力先フォルダが存在しません: {output_path.parent}"
        )

    return input_path, output_path


def check_output_permission(output_path, overwrite):
    """出力ファイルの上書き可否確認"""

    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"出力ファイルが既に存在します。上書きは禁止されています。\n"
            f"ファイル: {output_path}\n"
            f"上書きする場合はINIのoverwrite=1にしてください。"
        )


def inspect_pdf(pdf_path):
    """
    PDFの全ページを検査する。
    全ページが同じサイズであることを確認する。

    戻り値:
        pdfium.PdfDocument
        ページ幅（pt）
        ページ高さ（pt）
    """

    pdf = pdfium.PdfDocument(str(pdf_path))

    if len(pdf) == 0:
        pdf.close()
        raise ValueError("PDFにページがありません。")

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
                "PDFのページサイズが統一されていません。\n"
                f"1ページ目: {width:.3f} x {height:.3f} pt\n"
                f"{index + 1}ページ目: "
                f"{current_width:.3f} x {current_height:.3f} pt\n"
                "全ページが同じ原稿サイズのPDFのみ対応します。"
            )

    return pdf, width, height


def render_pdf_pages(pdf, dpi):
    """PDF全ページを画像化するジェネレータ"""

    if dpi <= 0:
        raise ValueError("DPIは1以上を指定してください。")

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
    converter
):
    """共通メイン処理"""

    parser = create_argument_parser(description)
    args = parser.parse_args()

    try:
        if args.dpi <= 0:
            raise ValueError("--dpiは1以上を指定してください。")

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
            print(f"入力PDF : {input_path}")
            print(f"出力先  : {output_path}")
            print(f"ページ数: {len(pdf)}")
            print(
                f"原稿サイズ: {width_pt:.3f} x "
                f"{height_pt:.3f} pt"
            )
            print(f"解像度: {args.dpi} DPI")

            converter(
                pdf,
                output_path,
                width_pt,
                height_pt,
                args.dpi
            )

        finally:
            pdf.close()

        print(f"変換完了: {output_path}")

    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    return 0
