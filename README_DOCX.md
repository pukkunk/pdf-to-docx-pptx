# PDF to Word Converter

日本語版 → [README_DOCX.ja.md](README_DOCX.ja.md)

## Overview

A Python script for converting PDF files into Word (DOCX) documents.

Each PDF page is rendered as an image and positioned behind the text on a corresponding Word page.

The original PDF page dimensions are applied to the Word page size.

The original layout and Japanese text appearance are preserved. Text and shapes can be added on top of the page images.

## Features

- One PDF page per Word page
- Multi-page PDF support
- Automatic PDF page size detection
- Original page dimensions
- Page images positioned behind text
- Separate page images for each page
- Configurable image resolution (DPI)
- Custom output filename
- INI-based overwrite control
- Validation of consistent page sizes

## File Structure

- `pdf_to_docx.py`
- `pdf_converter_common.py`
- `pdf_to_docx.ini` (created automatically on first execution)

## Requirements

- Python 3.8 or later
- pypdfium2
- python-docx
- Pillow

## Installation

Install the project dependencies from the project root directory.

### Using pip

```cmd
python -m pip install -r requirements.txt
```

## Usage

### Basic conversion

```cmd
python pdf_to_docx.py sample.pdf
```

The output file `sample.docx` is created in the same directory as the input PDF.

### Specify output filename

```cmd
python pdf_to_docx.py sample.pdf -o output.docx
```

### Specify image resolution

The default resolution is 300 DPI.

```cmd
python pdf_to_docx.py sample.pdf --dpi 400
```

Higher DPI produces sharper images but increases the output file size.

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

## Word Background Images

Each PDF page image is placed in the Word header area and positioned relative to the page.

The image is placed behind the text.

This allows users to add text and shapes on top of the original PDF page image.

Each page can have its own image, including multi-page documents.

## Notes

- PDF text is preserved as part of the page image.
- The original PDF text is not converted into editable Word text.
- The background image uses the Word header area. Take care when editing headers.
- Image position may vary depending on the Word version and printing environment.
- Output file size depends on the selected DPI.
- PDFs with different page dimensions are not supported.
- Password-protected PDFs may need to be unlocked separately.
- PDFs exceeding Word page-size limits may not be supported.

## License

MIT License

See [LICENSE](LICENSE) for details.

