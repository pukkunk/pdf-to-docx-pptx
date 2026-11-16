

# PDF to PowerPoint Converter

English version → [README_PPTX.md](README_PPTX.md)

## 概要

PDFファイルをPowerPoint（PPTX）に変換するPythonスクリプトです。

PDFの各ページを画像化し、PowerPointの各スライドの全面に配置します。

PDFの原稿サイズを取得し、PowerPointのスライドサイズに反映します。

PDFのレイアウトや日本語文字の表示を維持したまま、PowerPoint上で文字や図形を追加できます。

## 主な機能

- PDFの1ページをPowerPointの1スライドに変換
- 複数ページ対応
- PDFの原稿サイズを自動取得
- 元のPDFと同じスライドサイズで出力
- PDFページ画像をスライド全面に配置
- DPI指定による画像解像度の変更
- 出力ファイル名の指定
- INIファイルによる上書き制御
- 全ページの原稿サイズが同一であることを検証

## ファイル構成

- `pdf_to_pptx.py`
- `pdf_converter_common.py`
- `pdf_to_pptx.ini`（初回実行時に自動作成）

## 動作環境

- Python 3.8以上

## 必要なライブラリ

- pypdfium2
- python-pptx
- Pillow

## インストール

プロジェクトのルートディレクトリで実行します。

### pipによるインストール

```cmd
python -m pip install -r requirements.txt
```

## 使用方法

### 基本変換

```cmd
python pdf_to_pptx.py sample.pdf
```

入力PDFと同じフォルダに `sample.pptx` を作成します。

### 出力ファイルの指定

```cmd
python pdf_to_pptx.py sample.pdf -o output.pptx
```

### 画像解像度の指定

デフォルトは300 DPIです。

```cmd
python pdf_to_pptx.py sample.pdf --dpi 400
```

DPIを大きくすると画像が鮮明になりますが、出力ファイルのサイズも大きくなります。

## INIファイル

スクリプトと同じフォルダに `pdf_to_pptx.ini` を配置します。

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

PDFのページサイズを取得し、PowerPointのスライドサイズに反映します。

すべてのページが同じ原稿サイズであることを条件とします。

1ページ目と異なるサイズのページが存在する場合は、エラー終了します。

## PowerPoint上での利用

PDFページ画像はスライド全面に配置されます。

画像の上にテキストボックスや図形を配置することで、PDFの原稿に対して記入できます。

PDFの文字自体はPowerPointの編集可能なテキストにはなりません。

## 注意事項

- PDFの文字・罫線・図形は画像として保持されます。
- 出力ファイルサイズは指定したDPIによって変化します。
- PDFのページサイズが異なるファイルには対応していません。
- パスワード保護されたPDFは、別途解除が必要な場合があります。
- PowerPointのスライドサイズ制限を超えるPDFには対応できない場合があります。

## ライセンス

MIT License

詳細は [LICENSE](LICENSE) を参照してください。

