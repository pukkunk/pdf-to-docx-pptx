# PDF to DOCX / PPTX Converter

PDFファイルをPowerPoint（`.pptx`）またはWord（`.docx`）に変換するPythonスクリプトです。

PDFの各ページを画像として出力し、PowerPointではスライド全面に、Wordでは対応するページに配置することで、元のPDFの見た目と用紙サイズを維持します。

[English README](README.md)

## 主な機能

- PDFをPowerPointまたはWordに変換
- PDFの各ページを画像化して配置し、元の見た目を維持
- PDFのページサイズをPowerPointのスライドサイズまたはWordの用紙サイズに反映
- 複数ページのPDFに対応（PDF 1ページにつきスライドまたはWord 1ページ）
- 画像解像度（DPI）の指定
- パスワード付きPDFに対応
- 出力ファイルの保存先を指定可能
- INI設定ファイルで既存ファイルの上書き可否を制御
- DOCX版とPPTX版で共通のPDF処理コードを使用
- uvによるPython環境と依存パッケージの管理

## 変換スクリプト

| 出力形式 | スクリプト | 説明 |
|---|---|---|
| PowerPoint | `pdf_to_pptx.py` | [日本語](README_PPTX.ja.md) / [English](README_PPTX.md) |
| Word | `pdf_to_docx.py` | [日本語](README_DOCX.ja.md) / [English](README_DOCX.md) |

必要な出力形式に応じてスクリプトを選択してください。コマンドラインオプションや変換方式の詳細は、それぞれの説明書を参照してください。

## 動作環境・必要なもの

- Windows 10 / 11
- Python 3.11以降
- [uv](https://docs.astral.sh/uv/)

変換処理そのものにMicrosoft PowerPointやMicrosoft Wordは必要ありません。変換後のファイルを開いて編集する場合に、Officeまたは互換ソフトが必要です。

## ファイル構成

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

| ファイル名 | 説明 |
|---|---|
| `pdf_converter_common.py` | PDFの読み込み、検証、ページ処理などの共通関数 |
| `pdf_to_docx.py` | PDFをWordファイルに変換するスクリプト |
| `pdf_to_pptx.py` | PDFをPowerPointファイルに変換するスクリプト |
| `pdf_to_docx.bat` | DOCX変換を実行するWindowsバッチファイル |
| `pdf_to_pptx.bat` | PPTX変換を実行するWindowsバッチファイル |
| `pdf_to_docx.ini` | DOCX変換用の上書き設定 |
| `pdf_to_pptx.ini` | PPTX変換用の上書き設定 |
| `pyproject.toml` | プロジェクト情報と依存パッケージの定義 |
| `uv.lock` | 依存パッケージのバージョン固定情報 |
| `requirements.txt` | pip用の依存パッケージ一覧 |
| `README.md` / `README.ja.md` | プロジェクト全体の説明（英語・日本語） |
| `README_DOCX.md` / `README_DOCX.ja.md` | DOCX変換の説明（英語・日本語） |
| `README_PPTX.md` / `README_PPTX.ja.md` | PPTX変換の説明（英語・日本語） |
| `LICENSE` | ライセンス |

## インストール

### 1. uvのインストール

uvがインストールされていない場合は、公式サイトの手順に従ってインストールしてください。

https://docs.astral.sh/uv/getting-started/installation/

### 2. リポジトリの取得

```cmd
git clone https://github.com/pukkunk/pdf-to-docx-pptx.git
cd pdf-to-docx-pptx
```

### 3. Python環境の構築

プロジェクトのフォルダーで、次のコマンドを実行してください。

```cmd
uv sync
```

`pyproject.toml` と `uv.lock` に基づいて仮想環境が作成され、必要な依存パッケージがインストールされます。

## 基本的な使い方

入力PDFを指定して、出力形式に対応するスクリプトを実行します。

### PowerPoint（PPTX）への変換

```cmd
uv run pdf_to_pptx.py input.pdf
```

### Word（DOCX）への変換

```cmd
uv run pdf_to_docx.py input.pdf
```

### バッチファイルから実行

Windowsでは、付属のバッチファイルを利用できます。

```cmd
pdf_to_pptx.bat input.pdf
```

```cmd
pdf_to_docx.bat input.pdf
```

バッチファイルはuvのインストール先を検索し、見つからない場合は公式インストーラーによるインストールを試みます。

### 従来のpipによるインストール

uvを使用しない場合は、Python環境に対して以下のコマンドで依存パッケージをインストールできます。

```cmd
python -m pip install -r requirements.txt
```

インストール後は、次のように実行できます。

```cmd
python pdf_to_pptx.py input.pdf
python pdf_to_docx.py input.pdf
```

既定では、入力PDFと同じフォルダーに、入力ファイルと同じベース名で`.pptx`または`.docx`を出力します。

出力先、DPI、パスワード付きPDF、既存ファイルの上書き動作などの詳細は、各形式の説明書を参照してください。

## 重要：画像による変換方式

このスクリプトは、PDF内の文字・線・図形を、PowerPointやWordで個別に編集できるオブジェクトへ変換するものではありません。PDFの各ページ全体を画像に変換して配置します。

- PowerPoint：PDFページの画像をスライド全面に配置します。
- Word：PDFページの画像を対応する文書ページに配置します。

元のPDFの見た目は維持されますが、画像に含まれる文字や図形を個別に編集することはできません。必要に応じて、画像の上にテキストボックスや図形などを追加してください。

## ページサイズの扱い

PDFのページ寸法を、出力するスライドまたは文書ページのサイズに反映します。PDF内の全ページが同じ寸法であることを確認し、ページサイズが異なる場合は、サイズの不揃いなファイルが作成されないよう変換をエラー終了します。

## 設定ファイルと上書き制御

各スクリプトは、スクリプトと同じフォルダーにある専用のINIファイルを使用します。

- `pdf_to_pptx.ini`
- `pdf_to_docx.ini`

対応するINIファイルが存在しない場合、既定値`overwrite=0`で自動作成します。

- `overwrite=0`：既存の出力ファイルを上書きしません。出力先に同名ファイルが存在する場合はエラーになります。
- `overwrite=1`：既存の出力ファイルを上書きします。

DOCX版とPPTX版は別々のINIファイルを使用するため、上書き設定を個別に管理できます。

## ライセンス

ライセンス条件については、リポジトリ内の`LICENSE`ファイルを参照してください。
