# PDF to Word Converter

English version → [README_DOCX.md](README_DOCX.md)

## 概要

PDFファイルをWord（DOCX）に変換するPythonスクリプトです。

PDFの各ページを画像化し、対応するWordページの背景に配置します。

PDFの原稿サイズを取得し、Wordのページサイズに反映します。

PDFのレイアウトや日本語文字の表示を維持したまま、画像の上に文字や図形を追加できます。

## 主な機能

- PDFの1ページをWordの1ページに変換
- 複数ページ対応
- PDFの原稿サイズを自動取得
- 元のPDFと同じページサイズで出力
- PDFページ画像をページの背景に配置
- DPI指定による画像解像度の変更
- 出力ファイル名の指定
- INIファイルによる上書き制御
- 全ページの原稿サイズが同一であることを検証

## ファイル構成

- `pdf_to_docx.py`
- `pdf_converter_common.py`
- `pdf_to_docx.bat`（Windows用実行ファイル）
- `pdf_to_docx.ini`（初回実行時に自動作成）

## 動作環境

- Python 3.11以上
- uv（推奨）または pip

## 必要なライブラリ

- pypdfium2
- python-docx
- Pillow

## インストール

プロジェクトのルートディレクトリで実行します。

### uvによるインストール（推奨）

```cmd
uv sync
```

`pyproject.toml` に定義された依存ライブラリがインストールされます。

### pipによるインストール

```cmd
python -m pip install -r requirements.txt
```

`requirements.txt` はpipを使用する場合の依存ライブラリ一覧です。

## 使用方法

### 基本変換

#### Windows

```cmd
pdf_to_docx.bat sample.pdf
```

#### Linux / macOS

```bash
uv run python pdf_to_docx.py sample.pdf
```

入力PDFと同じフォルダに `sample.docx` を作成します。

### 出力ファイルの指定

#### Windows

```cmd
pdf_to_docx.bat sample.pdf -o output.docx
```

#### Linux / macOS

```bash
uv run python pdf_to_docx.py sample.pdf -o output.docx
```

### 画像解像度の指定

デフォルトは300 DPIです。

#### Windows

```cmd
pdf_to_docx.bat sample.pdf --dpi 400
```

#### Linux / macOS

```bash
uv run python pdf_to_docx.py sample.pdf --dpi 400
```

DPIを大きくすると画像が鮮明になりますが、出力ファイルのサイズも大きくなります。

### pip環境での実行

pipで依存ライブラリをインストールした場合は、Pythonスクリプトを直接実行します。

```cmd
python pdf_to_docx.py sample.pdf
```

オプションも同様に指定できます。

## INIファイル

スクリプトと同じフォルダに `pdf_to_docx.ini` を配置します。

初回実行時に存在しない場合は自動作成します。

初期設定：

```ini
[DEFAULT]
overwrite = 0
```

### overwriteの設定

| 設定値 | 動作 |
|---|---|
| 0 | 出力ファイルが存在する場合はエラー。上書き禁止 |
| 1 | 出力ファイルが存在しても上書き許可 |

デフォルトは `overwrite = 0` です。

## PDFのページサイズ

PDFのページサイズを取得し、Wordのページサイズに反映します。

すべてのページが同じ原稿サイズであることを条件とします。

1ページ目と異なるサイズのページが存在する場合は、エラー終了します。

## Word上での利用

PDFページ画像は、対応するWordページの背景として配置されます。

画像の上にテキストや図形を追加して、原稿に記入できます。

PDFの文字自体はWordの編集可能なテキストにはなりません。

## 注意事項

- PDFの文字・罫線・図形は画像として保持されます。
- 出力ファイルサイズは指定したDPIによって変化します。
- PDFのページサイズが異なるファイルには対応していません。
- パスワード保護されたPDFは、別途解除が必要な場合があります。
- Wordで開いた際の表示や編集結果は、使用するWord互換ソフトによって異なる場合があります。

## ライセンス

MIT License

詳細は [LICENSE](LICENSE) を参照してください。
