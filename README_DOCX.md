# PDF to Word Converter

日本語版 → [README_DOCX.ja.md](README_DOCX.ja.md)

## Overview

A Python script for converting PDF files into Word (DOCX) documents.

Each PDF page is rendered as an image and positioned as the background of the corresponding Word page.

The original PDF page dimensions are applied to the Word page size.

The original layout and Japanese text appearance are preserved. Text and shapes can be added on top of the page images.

## Features

- One PDF page per Word page
- Multi-page PDF support
- Automatic PDF page size detection
- Original page dimensions
- PDF page images placed as page backgrounds
- Configurable image resolution (DPI)
- Custom output filename
- INI-based overwrite control
- Validation of consistent page sizes

## File Structure

- `pdf_to_docx.py`
- `pdf_converter_common.py`
- `pdf_to_docx.bat` (Windows launcher)
- `pdf_to_docx.ini` (created automatically on first execution)

## Requirements

- Python 3.11 or later
- uv (recommended) or pip
- pypdfium2
- python-docx
- Pillow

## Installation

Run the following command in the project root directory.

### Using uv (recommended)

```cmd
uv sync
```

This installs the dependencies defined in `pyproject.toml`.

### Using pip

```cmd
python -m pip install -r requirements.txt
```

The `requirements.txt` file provides the dependency list for pip users.

## Usage

### Basic conversion

#### Windows

```cmd
pdf_to_docx.bat sample.pdf
```

#### Linux / macOS

```bash
uv run python pdf_to_docx.py sample.pdf
```

The output file `sample.docx` is created in the same directory as the input PDF.

### Specify output filename

#### Windows

```cmd
pdf_to_docx.bat sample.pdf -o output.docx
```

#### Linux / macOS

```bash
uv run python pdf_to_docx.py sample.pdf -o output.docx
```

### Specify image resolution

The default resolution is 300 DPI.

#### Windows

```cmd
pdf_to_docx.bat sample.pdf --dpi 400
```

#### Linux / macOS

```bash
uv run python pdf_to_docx.py sample.pdf --dpi 400
```

Higher DPI produces sharper images but increases the output file size.

### Running with pip

If dependencies were installed with pip, run the Python script directly:

```cmd
python pdf_to_docx.py sample.pdf
```

The same command-line options can be used.

## INI Configuration

The INI file is named `pdf_to_docx.ini` and is located in the same directory as the script.

If the file does not exist, it is created automatically on first execution.

Default settings:

```ini
[DEFAULT]
overwrite = 0
```

### Overwrite setting

| Value | Behavior |
|---|---|
| 0 | Prevent overwriting existing output files |
| 1 | Allow overwriting existing output files |

The default is `overwrite = 0`.

## PDF Page Size

The page dimensions of the input PDF are detected and applied to the Word page size.

All pages must have the same dimensions.

If a page has different dimensions from the first page, conversion is terminated with an error.

## Using the Document in Word

Each PDF page is placed as the background of the corresponding Word page.

Text and shapes can be added on top of the image.

The original PDF text is not converted into individually editable Word text.

## Notes

- PDF text, lines, and graphics are preserved as part of the page image.
- Output file size depends on the selected DPI.
- PDFs with different page dimensions are not supported.
- Password-protected PDFs may need to be unlocked separately.
- Display and editing results may vary depending on the Word-compatible application being used.

## License

MIT License

See [LICENSE](LICENSE) for details.
