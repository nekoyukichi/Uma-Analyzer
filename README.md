# Uma Analyzer

競馬データを分析してレース傾向を可視化するフルスタック Web アプリケーションです。  
フロントエンドは Next.js (TypeScript, Tailwind CSS, shadcn/ui)、バックエンドは FastAPI を使用します。

## 技術スタック

- **フロントエンド**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **バックエンド**: FastAPI, Uvicorn

## ディレクトリ構成（概要）

- **frontend**: Next.js フロントエンド
- **backend**: FastAPI バックエンド API

---

## セットアップ

プロジェクトルート:

```bash
cd "/Users/sakakibarakaito/Documents/開発/Uma-Analyzer"
```

### 1. フロントエンド (Next.js)

依存関係のインストール:

```bash
cd frontend
npm install
```

開発サーバー起動:

```bash
npm run dev
```

ブラウザで `http://localhost:3000` を開きます。

### 2. バックエンド (FastAPI)

仮想環境の作成と有効化 (任意推奨):

```bash
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

依存関係のインストール:

```bash
pip install -r requirements.txt
```

Uvicorn で API サーバーを起動:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

ブラウザで `http://localhost:8000/docs` にアクセスすると、自動生成された API ドキュメント (Swagger UI) を確認できます。

---

## API エンドポイント（初期状態）

- **GET `/`**: `"Uma Analyzer API"` というメッセージを返すルートエンドポイント
- **GET `/health`**: `{ "status": "ok" }` を返すヘルスチェックエンドポイント

---

## 開発メモ

- `.gitignore` は Node.js / Next.js / Python / macOS / 一般的な IDE の不要ファイルを除外するように設定済みです。
- shadcn/ui 用の `components.json` とボタンコンポーネントを用意しているので、今後コンポーネントを追加しやすい構成になっています。


