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

## 変換スクリプト

| 出力形式 | スクリプト | 説明 |
|---|---|---|
| PowerPoint | `pdf_to_pptx.py` | [日本語](README_PPTX.ja.md) / [English](README_PPTX.md) |
| Word | `pdf_to_docx.py` | [日本語](README_DOCX.ja.md) / [English](README_DOCX.md) |

必要な出力形式に応じてスクリプトを選択してください。コマンドラインオプションや変換方式の詳細は、それぞれの説明書を参照してください。

## 動作環境・必要なもの

- Python 3.8以降
- [`requirements.txt`](requirements.txt) に記載したPythonパッケージ

変換処理そのものにMicrosoft PowerPointやMicrosoft Wordは必要ありません。変換後のファイルを開いて編集する場合に、Officeまたは互換ソフトが必要です。

## ファイル構成

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

| ファイル名 | 説明 |
|---|---|
| `pdf_converter_common.py` | PDFの読み込み、検証、ページ処理などの共通関数 |
| `pdf_to_docx.py` | PDFをWordファイルに変換するスクリプト |
| `pdf_to_pptx.py` | PDFをPowerPointファイルに変換するスクリプト |
| `pdf_to_docx.ini` | DOCX変換用の上書き設定 |
| `pdf_to_pptx.ini` | PPTX変換用の上書き設定 |
| `requirements.txt` | Pythonパッケージの依存関係 |
| `README.md` / `README.ja.md` | プロジェクト全体の説明（英語・日本語） |
| `README_DOCX.md` / `README_DOCX.ja.md` | DOCX変換の説明（英語・日本語） |
| `README_PPTX.md` / `README_PPTX.ja.md` | PPTX変換の説明（英語・日本語） |

## インストール

プロジェクトのフォルダーで、次のコマンドを実行してください。

```text
python -m pip install -r requirements.txt
```

## 基本的な使い方

入力PDFを指定して、出力形式に対応するスクリプトを実行します。

```text
python pdf_to_pptx.py input.pdf
```

```text
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
