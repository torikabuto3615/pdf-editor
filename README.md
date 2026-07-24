# PDFツールキット

Flask + [pypdf](https://pypdf.readthedocs.io/) で作った、ブラウザから使えるPDF編集ツールです。
実習用に作成したアプリを、機能追加とデザイン改善を経てブラッシュアップしました。

## 主な機能

| 機能 | 説明 |
|---|---|
| PDF結合 | 複数のPDFを選んだ順に1つのファイルへまとめます |
| PDF分割 | 1ページごとに分割し、ZIPでまとめてダウンロードします |
| PDF削除 | 指定した1ページだけを取り除いた新しいPDFを作成します |
| 並び替え・回転 | ページをドラッグ&ドロップで並び替え、ボタンで回転できます |

いずれの画面でも、ファイルを選択した時点で **ファイル名とページ数がプレビュー表示**されます
（[PDF.js](https://mozilla.github.io/pdf.js/)によりブラウザ上でPDFを読み込んで表示しているため、サーバーには一切送信されません）。

## 使用技術

- **バックエンド**: Python 3 / Flask / pypdf
- **フロントエンド**: HTML / CSS / JavaScript（PDF.jsをCDN経由で使用、フレームワーク不使用）
- **本番サーバー**: gunicorn（Render上で使用）

## ディレクトリ構成

```
.
├── app.py                  # Flaskアプリ本体(ルーティング・PDF処理)
├── requirements.txt        # 依存ライブラリ一覧
├── Procfile                # Render起動コマンド定義
├── templates/
│   ├── base.html           # 共通レイアウト(全ページはこれを継承)
│   ├── index.html          # トップページ
│   ├── merge.html          # PDF結合
│   ├── split.html          # PDF分割
│   ├── delete.html         # PDFページ削除
│   └── reorder.html        # 並び替え・回転
└── static/
    ├── css/style.css        # 全ページ共通のスタイル
    └── js/preview.js        # ファイルプレビュー・ドロップゾーン用の共通JS
```

## ローカルでの実行方法

### 1. リポジトリを取得

```bash
git clone <このリポジトリのURL>
cd <リポジトリ名>
```

### 2. 仮想環境を作成して有効化

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. 依存ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 4. アプリを起動

```bash
python app.py
```

ブラウザで `http://127.0.0.1:5000` を開くと使用できます。

---

## GitHubへのアップロード手順

まだGitHubにリポジトリを作っていない場合は、GitHub上で「New repository」から空のリポジトリを作成してください（READMEなどは追加しない）。

```bash
cd <プロジェクトのフォルダ>

git init
git add .
git commit -m "PDFツールキット初回コミット"

git branch -M main
git remote add origin <GitHubリポジトリのURL>
git push -u origin main
```

> `.gitignore` で `venv/` や `__pycache__/` は除外済みのため、余計なファイルはアップロードされません。

---

## Renderへのデプロイ手順

1. [Render](https://render.com/) にログイン(GitHubアカウントで登録可能)
2. ダッシュボードで **New +** → **Web Service** を選択
3. 先ほどGitHubにアップロードしたリポジトリを選択して連携
4. 以下の内容を設定
   | 項目 | 値 |
   |---|---|
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn app:app` |
   | Instance Type | Free（学習用途であれば無料枠でOK） |
5. **Create Web Service** をクリックしてデプロイ開始
6. 数分待つとURL(例: `https://your-app-name.onrender.com`)が発行され、公開されます

### デプロイ時の注意点

- **アップロードしたファイルの保存場所について**：このアプリは処理したPDFを一時フォルダ（`tempfile`）に保存しています。Renderの無料プランはファイルシステムが再起動のたびにリセットされる「一時的な」構成のため、生成したファイルは長期保存されません。ダウンロードしたらその場で使い切る想定の設計になっています。
- **無料プランのスリープ**：Renderの無料プランは、一定時間アクセスがないとアプリがスリープします。次にアクセスした際、起動までに数十秒かかることがあります。
- **ファイルサイズ**：大きなPDFを扱う場合、Flaskの`MAX_CONTENT_LENGTH`設定やRender側のリクエストサイズ制限に注意してください（本アプリでは現在未設定=無制限のため、必要に応じて`app.py`に追加することをおすすめします）。

---

## 今後改善できそうな点

- パスワード保護・暗号化機能の追加
- 透かし(ウォーターマーク)機能の追加
- アップロードファイルサイズの上限設定とエラーメッセージの表示
- 複数ページ削除への対応(現在は1ページのみ)
