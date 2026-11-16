# PDF to DOCX / PPTX Converter

Python scripts for converting PDF files to PowerPoint (`.pptx`) and Word (`.docx`).

The conversion preserves the appearance and page dimensions of the original PDF by rendering each PDF page as an image and placing that image on a corresponding Office page.

[日本語版 README](README.ja.md)

## Features

- Convert PDF files to PowerPoint or Word.
- Preserve the original PDF page appearance by using page images.
- Use the original PDF page dimensions for the PowerPoint slide size or Word page size.
- Support multi-page PDF files (one PDF page per slide or document page).
- Set the image resolution (DPI).
- Open password-protected PDF files by specifying a password.
- Specify the output file path.
- Control whether an existing output file can be overwritten through an INI configuration file.
- Share common PDF processing code between the DOCX and PPTX converters.

## Conversion scripts

| Output format | Script | Documentation |
|---|---|---|
| PowerPoint | `pdf_to_pptx.py` | [English](README_PPTX.md) / [日本語](README_PPTX.ja.md) |
| Word | `pdf_to_docx.py` | [English](README_DOCX.md) / [日本語](README_DOCX.ja.md) |

Choose the script for the output format you need. The command-line options and conversion details are described in the corresponding document.

## Requirements

- Python 3.8 or later
- Packages listed in [`requirements.txt`](requirements.txt)

The conversion itself does not require Microsoft PowerPoint or Microsoft Word to be installed. An Office application or compatible software is required only to open and edit the resulting files.

## Project files

```text
pdf-converter/
├── pdf_converter_common.py
├── pdf_to_docx.ini
├── pdf_to_docx.py
├── pdf_to_pptx.ini
├── pdf_to_pptx.py
├── README.md
├── README.ja.md
├── README_DOCX.md
├── README_DOCX.ja.md
├── README_PPTX.md
├── README_PPTX.ja.md
└── requirements.txt
```

| File | Description |
|---|---|
| `pdf_converter_common.py` | Common PDF loading, validation, and page-processing functions |
| `pdf_to_docx.py` | Converts PDF files to Word documents |
| `pdf_to_pptx.py` | Converts PDF files to PowerPoint presentations |
| `pdf_to_docx.ini` | Overwrite settings for the DOCX converter |
| `pdf_to_pptx.ini` | Overwrite settings for the PPTX converter |
| `requirements.txt` | Python package dependencies |
| `README.md` / `README.ja.md` | Project overview in English and Japanese |
| `README_DOCX.md` / `README_DOCX.ja.md` | DOCX conversion instructions |
| `README_PPTX.md` / `README_PPTX.ja.md` | PPTX conversion instructions |

## Installation

Run the following command in the project directory:

```text
python -m pip install -r requirements.txt
```

## Quick start

Run the appropriate script and specify the input PDF:

```text
python pdf_to_pptx.py input.pdf
```

```text
python pdf_to_docx.py input.pdf
```

By default, the output file is created in the same directory as the input PDF, using the same base name and the corresponding extension (`.pptx` or `.docx`).

For output options, DPI, password-protected PDFs, and overwrite behavior, see the format-specific documentation.

## Important: image-based conversion

These scripts do not convert PDF text, lines, or figures into individually editable PowerPoint or Word objects. Each PDF page is rendered as an image.

- In PowerPoint, the page image is placed across the entire slide.
- In Word, the page image is placed on the corresponding document page.

The original page appearance is retained, but text and graphics contained in the PDF image cannot be edited individually. You can add text boxes, shapes, or other Office objects over the image as needed.

## Page-size handling

The page dimensions of the PDF are used for the output slide or document page. The converters check that all pages in a PDF have the same dimensions. If pages have different dimensions, conversion is stopped with an error rather than producing a document with inconsistent page sizing.

## Configuration and overwrite protection

Each converter uses its own INI file located alongside the script:

- `pdf_to_pptx.ini`
- `pdf_to_docx.ini`

If the corresponding INI file does not exist, the script creates it with the default setting `overwrite=0`.

- `overwrite=0`: do not overwrite an existing output file. The conversion ends with an error if the output file already exists.
- `overwrite=1`: allow an existing output file to be overwritten.

The two converters have separate INI files, so their overwrite settings can be managed independently.

## License

See the repository's `LICENSE` file for license terms.
