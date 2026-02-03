# MeDF 使用ガイド

このガイドでは、MeDFフォーマットの実践的な使用方法を説明します。

## 目次

1. [MeDFドキュメントの作成](#medfドキュメントの作成)
2. [メタデータの設定](#メタデータの設定)
3. [インデックスの構築](#インデックスの構築)
4. [コンテンツの記述](#コンテンツの記述)
5. [参照の管理](#参照の管理)
6. [ベストプラクティス](#ベストプラクティス)

## MeDFドキュメントの作成

### 1. 基本テンプレート

新しいMeDFドキュメントを作成する際は、以下の基本テンプレートから始めます：

```json
{
  "medf": {
    "version": "1.0",
    "schema": "https://medf.org/schema/v1.0"
  },
  "metadata": {
    "id": "",
    "title": "",
    "type": "",
    "status": "draft",
    "created": "",
    "authors": [],
    "language": "ja"
  },
  "index": {
    "toc": []
  },
  "content": {
    "sections": []
  }
}
```

### 2. IDの生成

ドキュメントIDは一意である必要があります。推奨される命名規則：

```
{プロジェクト名}-{ドキュメントタイプ}-{日付}
例: medf-spec-2026-02-03
```

または、UUIDを使用：

```
550e8400-e29b-41d4-a716-446655440000
```

## メタデータの設定

### ドキュメントタイプ

適切なタイプを選択してください：

* `report` - レポート、報告書
* `specification` - 仕様書、規格書
* `snapshot` - 状態のスナップショット
* `analysis` - 分析結果、調査報告
* `other` - その他

### ステータス管理

ドキュメントのライフサイクルを表現：

* `draft` - 草稿、作成中
* `review` - レビュー中
* `official` - 正式版、承認済み
* `archived` - アーカイブ済み

### 著者情報

```json
"authors": [
  {
    "name": "山田太郎",
    "role": "creator",
    "contact": "yamada@example.com"
  },
  {
    "name": "佐藤花子",
    "role": "contributor"
  },
  {
    "name": "鈴木一郎",
    "role": "reviewer"
  }
]
```

役割の種類：
* `creator` - 主著者、作成者
* `contributor` - 共同執筆者、貢献者
* `reviewer` - レビュアー、査読者

### セキュリティ分類

```json
"security": {
  "classification": "internal",
  "accessControl": ["engineering-team", "management"]
}
```

分類レベル：
* `public` - 公開情報
* `internal` - 社内限定
* `confidential` - 機密情報
* `secret` - 極秘情報

## インデックスの構築

### 目次（TOC）の作成

階層構造を持つ目次を定義します：

```json
"toc": [
  {
    "id": "section-1",
    "title": "イントロダクション",
    "level": 1,
    "summary": "プロジェクトの背景と目的",
    "children": [
      {
        "id": "section-1-1",
        "title": "背景",
        "level": 2,
        "summary": "なぜこのプロジェクトが必要か"
      },
      {
        "id": "section-1-2",
        "title": "目的",
        "level": 2,
        "summary": "達成すべき目標"
      }
    ]
  },
  {
    "id": "section-2",
    "title": "実装詳細",
    "level": 1
  }
]
```

**ポイント**：
* `level`は見出しレベル（1が最上位）
* `summary`は省略可能だが、AI処理に役立つため推奨
* `children`で階層構造を表現

### キーワードの索引

重要な用語を索引化します：

```json
"keywords": [
  {
    "term": "機械学習",
    "frequency": 15,
    "contexts": ["section-2", "section-4", "section-7"],
    "definition": "データから学習するアルゴリズム"
  },
  {
    "term": "API",
    "frequency": 23,
    "contexts": ["section-3", "section-5"],
    "definition": "Application Programming Interface"
  }
]
```

**ポイント**：
* `frequency`は出現回数（省略可能）
* `contexts`は出現セクションのID
* `definition`は用語の定義（特に略語や専門用語で重要）

### エンティティの抽出

固有名詞を索引化します：

```json
"entities": [
  {
    "name": "TensorFlow",
    "type": "technology",
    "mentions": ["section-2", "section-6"]
  },
  {
    "name": "OpenAI",
    "type": "organization",
    "mentions": ["section-1"]
  },
  {
    "name": "John Doe",
    "type": "person",
    "mentions": ["section-4"]
  }
]
```

エンティティタイプ：
* `person` - 人名
* `organization` - 組織名
* `technology` - 技術名、製品名
* `location` - 地名
* `concept` - 概念、抽象的な概念
* `other` - その他

### 関係性の定義

セクション間の関係を明示します：

```json
"relationships": [
  {
    "source": "section-3",
    "target": "section-2",
    "type": "depends-on"
  },
  {
    "source": "section-5",
    "target": "section-4",
    "type": "extends"
  }
]
```

関係性のタイプ：
* `references` - 参照している
* `depends-on` - 依存している
* `contradicts` - 矛盾している
* `extends` - 拡張している
* `supports` - 支持している、根拠となっている

## コンテンツの記述

### テキストコンテンツ

```json
{
  "id": "intro",
  "title": "はじめに",
  "type": "text",
  "body": "このドキュメントでは...",
  "metadata": {
    "importance": "high",
    "confidence": 1.0,
    "lastVerified": "2026-02-03T23:00:00Z"
  }
}
```

### 構造化データ

```json
{
  "id": "metrics",
  "title": "パフォーマンス指標",
  "type": "data",
  "body": {
    "responseTime": {
      "average": 120,
      "max": 450,
      "unit": "ms"
    },
    "throughput": {
      "value": 1000,
      "unit": "requests/sec"
    }
  },
  "metadata": {
    "importance": "high",
    "confidence": 0.95,
    "lastVerified": "2026-02-03T22:00:00Z"
  }
}
```

### コードブロック

```json
{
  "id": "code-example",
  "title": "実装例",
  "type": "code",
  "body": "function validateMeDF(doc) {\n  // バリデーション処理\n  return schema.validate(doc);\n}",
  "metadata": {
    "language": "javascript",
    "importance": "medium"
  }
}
```

### アノテーション

セクションに注釈を追加できます：

```json
"annotations": [
  {
    "type": "note",
    "text": "このセクションは次回更新予定",
    "author": "山田太郎",
    "timestamp": "2026-02-03T15:00:00Z"
  },
  {
    "type": "warning",
    "text": "この機能は非推奨になる予定",
    "timestamp": "2026-02-03T16:00:00Z"
  },
  {
    "type": "todo",
    "text": "パフォーマンステストの結果を追加",
    "author": "佐藤花子"
  }
]
```

アノテーションタイプ：
* `note` - メモ、補足情報
* `warning` - 警告、注意事項
* `question` - 質問、要確認事項
* `todo` - TODO、未完了タスク
* `info` - 情報、ヒント

## 参照の管理

### 外部参照

```json
"external": [
  {
    "id": "ref-api-doc",
    "type": "document",
    "title": "REST API ドキュメント",
    "url": "https://api.example.com/docs",
    "version": "2.0",
    "accessed": "2026-02-03T20:00:00Z",
    "checksum": "sha256:abc123def456...",
    "status": "active"
  },
  {
    "id": "ref-github",
    "type": "repository",
    "title": "プロジェクトリポジトリ",
    "url": "https://github.com/example/project",
    "accessed": "2026-02-03T20:00:00Z",
    "status": "active"
  }
]
```

参照タイプ：
* `document` - ドキュメント、論文
* `api` - API、Webサービス
* `dataset` - データセット
* `repository` - リポジトリ（Git等）
* `website` - Webサイト
* `other` - その他

### 内部参照

同一ドキュメント内のセクション間参照：

```json
"internal": [
  {
    "id": "int-ref-1",
    "sourceSection": "section-5",
    "targetSection": "section-2",
    "relationship": "depends-on"
  }
]
```

## ベストプラクティス

### 1. 適切な粒度でセクション分割

* 1セクションは1つの主要トピックに集中
* 長すぎるセクション（3000語以上）は分割を検討
* AI処理を考慮し、セクションサイズを適度に保つ

### 2. メタデータを充実させる

* `summary`を各TOCエントリに追加
* `importance`と`confidence`を適切に設定
* タグとキーワードを活用して検索性を向上

### 3. バージョン管理を適切に行う

* メジャー変更：構造の大幅変更、互換性のない変更
* マイナー変更：セクションの追加・削除
* パッチ変更：誤字修正、軽微な更新

### 4. 外部参照の保守

* 定期的に外部リンクの有効性を確認
* `accessed`フィールドを更新
* リンク切れは`status: "unavailable"`に変更

### 5. AI処理を意識した記述

* セクションには明確な`title`と`summary`を設定
* キーワードとエンティティを適切に索引化
* 関係性を明示的に定義

### 6. セキュリティに配慮

* 機密情報は適切に分類
* アクセス制御を設定
* 公開範囲を明確に

### 7. 一貫性の維持

* 用語の使い方を統一
* IDの命名規則を統一
* 日時はISO 8601形式で記録

## 検証とテスト

### JSON Schemaによる検証

```bash
# ajvなどのツールを使用
ajv validate -s schema.json -d your-document.medf.json
```

### 手動チェックリスト

- [ ] すべての必須フィールドが存在する
- [ ] IDが一意である
- [ ] セクションIDとTOCのIDが一致する
- [ ] 内部参照が有効である
- [ ] 外部参照が有効である
- [ ] 日時がISO 8601形式である
- [ ] バージョン番号がセマンティックバージョニングに従っている

## まとめ

MeDFは柔軟で強力なフォーマットです。このガイドに従って、AIと人間の両方が理解しやすい、高品質なドキュメントを作成してください。

不明点や改善提案があれば、プロジェクトにフィードバックをお願いします！
