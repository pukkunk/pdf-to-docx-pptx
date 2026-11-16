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
- Manage Python environments and dependencies with uv.

## Conversion scripts

| Output format | Script | Documentation |
|---|---|---|
| PowerPoint | `pdf_to_pptx.py` | [English](README_PPTX.md) / [日本語](README_PPTX.ja.md) |
| Word | `pdf_to_docx.py` | [English](README_DOCX.md) / [日本語](README_DOCX.ja.md) |

Choose the script for the output format you need. The command-line options and conversion details are described in the corresponding document.

## Requirements

- Windows 10 / 11
- Python 3.8 or later
- [uv](https://docs.astral.sh/uv/)

The conversion itself does not require Microsoft PowerPoint or Microsoft Word to be installed. An Office application or compatible software is required only to open and edit the resulting files.

## Project files

```text
pdf-to-docx-pptx/
├── LICENSE
├── pdf_converter_common.py
├── pdf_to_docx.bat
├── pdf_to_docx.ini
├── pdf_to_docx.py
├── pdf_to_pptx.bat
├── pdf_to_pptx.ini
├── pdf_to_pptx.py
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── README.md
├── README.ja.md
├── README_DOCX.md
├── README_DOCX.ja.md
├── README_PPTX.md
└── README_PPTX.ja.md
```

| File | Description |
|---|---|
| `LICENSE` | License information |
| `pdf_converter_common.py` | Common PDF loading, validation, and page-processing functions |
| `pdf_to_docx.py` | Converts PDF files to Word documents |
| `pdf_to_pptx.py` | Converts PDF files to PowerPoint presentations |
| `pdf_to_docx.bat` | Windows batch file for DOCX conversion |
| `pdf_to_pptx.bat` | Windows batch file for PPTX conversion |
| `pdf_to_docx.ini` | Overwrite settings for the DOCX converter |
| `pdf_to_pptx.ini` | Overwrite settings for the PPTX converter |
| `pyproject.toml` | Project metadata and dependency definitions |
| `uv.lock` | Locked dependency versions |
| `requirements.txt` | Python package dependencies for pip |
| `README.md` / `README.ja.md` | Project overview in English and Japanese |
| `README_DOCX.md` / `README_DOCX.ja.md` | DOCX conversion instructions |
| `README_PPTX.md` / `README_PPTX.ja.md` | PPTX conversion instructions |

## Installation

### 1. Install uv

If uv is not installed, follow the official installation instructions:

https://docs.astral.sh/uv/getting-started/installation/

### 2. Clone the repository

```cmd
git clone https://github.com/pukkunk/pdf-to-docx-pptx.git
cd pdf-to-docx-pptx
```

### 3. Set up the Python environment

Run the following command in the project directory:

```cmd
uv sync
```

This creates a virtual environment and installs the required packages based on `pyproject.toml` and `uv.lock`.

## Quick start

Run the appropriate script and specify the input PDF.

### Convert to PowerPoint (PPTX)

```cmd
uv run pdf_to_pptx.py input.pdf
```

### Convert to Word (DOCX)

```cmd
uv run pdf_to_docx.py input.pdf
```

### Run using Windows batch files

You can also use the included batch files on Windows.

```cmd
pdf_to_pptx.bat input.pdf
```

```cmd
pdf_to_docx.bat input.pdf
```

The batch files search for the uv executable. If it cannot be found, they attempt to install uv using the official installer.

### Install using pip (alternative)

If you prefer not to use uv, install the dependencies into your Python environment using:

```cmd
python -m pip install -r requirements.txt
```

Then run the scripts directly:

```cmd
python pdf_to_pptx.py input.pdf
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
