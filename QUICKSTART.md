# MeDF Quick Start

5分でMeDFドキュメントを作成できる簡単ガイドです。

## ステップ 1: テンプレートを用意

以下のテンプレートをコピーして、新しいファイル `my-document.v1.0.medf.json` を作成します：

```json
{
  "medf": {
    "version": "1.0",
    "schema": "https://medf.org/schema/v1.0"
  },
  "metadata": {
    "id": "my-document-2026-02-03",
    "title": "私のドキュメント",
    "type": "report",
    "status": "draft",
    "created": "2026-02-03T23:00:00Z",
    "authors": [
      {
        "name": "あなたの名前",
        "role": "creator"
      }
    ],
    "tags": ["example"],
    "language": "ja"
  },
  "index": {
    "toc": [
      {
        "id": "introduction",
        "title": "はじめに",
        "level": 1,
        "summary": "ドキュメントの概要"
      }
    ]
  },
  "content": {
    "sections": [
      {
        "id": "introduction",
        "title": "はじめに",
        "type": "text",
        "body": "ここに内容を書きます。",
        "metadata": {
          "importance": "high"
        }
      }
    ]
  }
}
```

## ステップ 2: 内容をカスタマイズ

### メタデータを更新

```json
"metadata": {
  "id": "project-report-2026-02",        ← 一意のIDに変更
  "title": "2月度プロジェクトレポート",   ← タイトルを変更
  "type": "report",                      ← report/specification/snapshot/analysis から選択
  "status": "draft",                     ← draft/review/official/archived から選択
  "created": "2026-02-03T23:00:00Z",    ← 作成日時（ISO 8601形式）
  "authors": [
    {
      "name": "山田太郎",                 ← 著者名
      "role": "creator"                   ← creator/contributor/reviewer
    }
  ],
  "tags": ["project", "monthly-report"], ← タグを追加
  "language": "ja"                       ← 言語コード
}
```

### セクションを追加

```json
"content": {
  "sections": [
    {
      "id": "introduction",
      "title": "はじめに",
      "type": "text",
      "body": "ドキュメントの概要..."
    },
    {
      "id": "main-content",
      "title": "主な内容",
      "type": "text",
      "body": "詳細な説明..."
    },
    {
      "id": "conclusion",
      "title": "まとめ",
      "type": "text",
      "body": "結論..."
    }
  ]
}
```

### 目次（TOC）を更新

セクションを追加したら、TOCも更新：

```json
"toc": [
  {
    "id": "introduction",
    "title": "はじめに",
    "level": 1,
    "summary": "ドキュメントの概要"
  },
  {
    "id": "main-content",
    "title": "主な内容",
    "level": 1,
    "summary": "詳細な説明"
  },
  {
    "id": "conclusion",
    "title": "まとめ",
    "level": 1,
    "summary": "結論"
  }
]
```

## ステップ 3: 検証

ドキュメントが正しい形式か確認：

```bash
python3 validate.py my-document.v1.0.medf.json
```

✓が表示されたら成功です！

## よくある使い方

### 1. 構造化データを含める

```json
{
  "id": "metrics",
  "title": "指標",
  "type": "data",
  "body": {
    "revenue": 1000000,
    "growth": "20%",
    "customers": 500
  }
}
```

### 2. コードを含める

```json
{
  "id": "code-sample",
  "title": "コード例",
  "type": "code",
  "body": "function hello() {\n  console.log('Hello MeDF!');\n}"
}
```

### 3. 注釈を追加

```json
{
  "id": "section-1",
  "title": "セクション1",
  "type": "text",
  "body": "内容...",
  "annotations": [
    {
      "type": "note",
      "text": "後で更新予定",
      "author": "山田"
    }
  ]
}
```

### 4. 外部参照を追加

```json
"references": {
  "external": [
    {
      "id": "ref-1",
      "type": "website",
      "title": "参考サイト",
      "url": "https://example.com",
      "accessed": "2026-02-03T23:00:00Z",
      "status": "active"
    }
  ]
}
```

## 次のステップ

- 📖 [USAGE_GUIDE.md](USAGE_GUIDE.md) - 詳細な使い方
- 📚 [USE_CASES.md](USE_CASES.md) - ユースケース集
- 📋 [examples/](examples/) - 実際の例を見る
- 📜 [SPECIFICATION.md](SPECIFICATION.md) - 完全な仕様

## ヘルプ

質問や問題がある場合は、GitHubのIssuesで質問してください！
