# MeDF (Meta / Modular e-Document Format) Specification v1.0

## 1. 概要（Overview）

### 1.1 目的（Purpose）

MeDFは、**AI時代に最適化された軽量・可変・機械可読なドキュメントフォーマット**です。PDFの「紙前提・固定レイアウト・重量化」という制約から脱却し、以下を同時に実現します：

* **情報の全体像把握（インデックス性）** - 構造化されたメタデータとインデックスにより、AIとヒューマンの両方が迅速に全体像を理解できる
* **スナップショットとしての公式性** - 特定時点の状態を確実に記録・共有できる
* **分散管理された原本との整合性** - 外部ソースへの参照を保持し、常に最新状態を追跡可能

### 1.2 一言定義

> **「思考とプロジェクトの"状態"を凍結・共有できる、AIネイティブなインデックス型ドキュメント」**

### 1.3 解決する本質的課題

1. **全体像が誰にも見えていない** → 構造化メタデータとインデックスで解決
2. **正式情報と作業情報が混ざる** → レイヤー分離とステータス管理で解決
3. **AI時代の「記録単位」が存在しない** → MeDFが新しい標準単位に

## 2. コア概念（Core Concepts）

### 2.1 状態スナップショット（State Snapshot）

MeDFドキュメントは特定時点における「状態の凍結」を表します。

* **時間軸の明確化** - 作成日時、有効期限、バージョン情報
* **不変性** - 一度作成されたスナップショットは変更されない
* **追跡可能性** - 前バージョンとの差分、変更履歴の記録

### 2.2 インデックス構造（Index Structure）

ドキュメントの内容を多次元で索引化：

* **階層的目次** - セクション、サブセクション、項目
* **意味的タグ** - キーワード、カテゴリ、関連性
* **メタデータ** - 著者、ステータス、重要度、関連リソース

### 2.3 モジュラー性（Modularity）

* **分散参照** - 外部ドキュメント、データソース、APIへのリンク
* **部分的更新** - モジュール単位での差し替え・更新
* **再利用性** - 共通部品の参照と継承

## 3. フォーマット仕様（Format Specification）

### 3.1 基本構造

MeDFドキュメントはJSON形式で記述され、以下の構造を持ちます：

```json
{
  "medf": {
    "version": "1.0",
    "schema": "https://medf.org/schema/v1.0"
  },
  "metadata": { ... },
  "index": { ... },
  "content": { ... },
  "references": { ... }
}
```

### 3.2 メタデータセクション（Metadata Section）

```json
"metadata": {
  "id": "unique-document-id",
  "title": "ドキュメントタイトル",
  "type": "report | specification | snapshot | analysis",
  "status": "draft | review | official | archived",
  "created": "2026-02-03T23:00:00Z",
  "modified": "2026-02-03T23:00:00Z",
  "validUntil": "2027-02-03T23:00:00Z",
  "version": "1.0.0",
  "previousVersion": "document-id-of-previous-version",
  "authors": [
    {
      "name": "著者名",
      "role": "creator | contributor | reviewer",
      "contact": "email@example.com"
    }
  ],
  "tags": ["AI", "specification", "format"],
  "language": "ja",
  "security": {
    "classification": "public | internal | confidential",
    "accessControl": ["group1", "group2"]
  }
}
```

### 3.3 インデックスセクション（Index Section）

```json
"index": {
  "toc": [
    {
      "id": "section-1",
      "title": "セクション1",
      "level": 1,
      "summary": "このセクションの概要",
      "children": [
        {
          "id": "section-1-1",
          "title": "サブセクション1.1",
          "level": 2
        }
      ]
    }
  ],
  "keywords": [
    {
      "term": "MeDF",
      "frequency": 15,
      "contexts": ["section-1", "section-3"],
      "definition": "Meta/Modular e-Document Format"
    }
  ],
  "entities": [
    {
      "name": "PDF",
      "type": "technology",
      "mentions": ["section-1", "section-2"]
    }
  ],
  "relationships": [
    {
      "source": "section-1",
      "target": "section-3",
      "type": "references | depends-on | contradicts"
    }
  ]
}
```

### 3.4 コンテンツセクション（Content Section）

```json
"content": {
  "sections": [
    {
      "id": "section-1",
      "title": "イントロダクション",
      "type": "text | code | data | image | table",
      "body": "実際のコンテンツ内容...",
      "metadata": {
        "importance": "high | medium | low",
        "confidence": 0.95,
        "lastVerified": "2026-02-03T23:00:00Z"
      },
      "annotations": [
        {
          "type": "note | warning | question",
          "text": "注釈内容",
          "author": "著者名",
          "timestamp": "2026-02-03T23:00:00Z"
        }
      ]
    }
  ]
}
```

### 3.5 参照セクション（References Section）

```json
"references": {
  "external": [
    {
      "id": "ref-1",
      "type": "document | api | dataset | repository",
      "title": "参照先タイトル",
      "url": "https://example.com/resource",
      "version": "1.0",
      "accessed": "2026-02-03T23:00:00Z",
      "checksum": "sha256:abc123...",
      "status": "active | deprecated | unavailable"
    }
  ],
  "internal": [
    {
      "id": "int-ref-1",
      "sourceSection": "section-1",
      "targetSection": "section-3",
      "relationship": "supports | contradicts | extends"
    }
  ]
}
```

## 4. ユースケース（Use Cases）

### 4.1 プロジェクト状態レポート

特定時点でのプロジェクト全体の状態を記録：

* 進捗状況のスナップショット
* 課題と決定事項の記録
* 関連ドキュメント・リソースへのインデックス

### 4.2 AI対話の記録

AIとの対話内容を構造化して保存：

* 質問と回答のペア
* コンテキストと推論過程
* 生成されたコード・データへの参照

### 4.3 分散ナレッジベースのスナップショット

複数のソースから情報を統合：

* Wiki、Notion、GitHubなどからの情報収集
* 時点を固定したスナップショット作成
* 元ソースへのトレーサビリティ保持

### 4.4 仕様書・設計書の管理

技術ドキュメントのバージョン管理：

* 正式版と作業版の明確な分離
* 変更履歴と承認プロセスの記録
* 実装との紐付け

## 5. AI活用のための設計（AI-Optimized Design）

### 5.1 機械可読性

* **構造化データ** - JSON形式により、AIが容易にパース・理解可能
* **明示的メタデータ** - 型情報、ステータス、関係性を明記
* **セマンティック情報** - キーワード、エンティティ、関係性の索引

### 5.2 コンテキスト提供

* **階層的構造** - セクション間の関係を明示
* **サマリー情報** - 各セクションの要約をインデックスに含める
* **参照の追跡** - 外部リソースとの関連を記録

### 5.3 検索・分析の最適化

* **多次元インデックス** - 内容、著者、日付、タグなど多角的な検索
* **ベクトル埋め込み対応** - セクション単位でのembedding生成を想定
* **差分抽出** - バージョン間の変更を効率的に特定

## 6. 実装ガイドライン（Implementation Guidelines）

### 6.1 ファイル命名規則

```
{document-name}.{version}.medf.json
例: project-status.v1.0.medf.json
```

### 6.2 バージョニング

* セマンティックバージョニング（Major.Minor.Patch）を推奨
* メジャーバージョンアップ：構造の大幅変更
* マイナーバージョンアップ：セクションの追加・削除
* パッチバージョンアップ：内容の修正・更新

### 6.3 検証

* JSON Schema による構造検証
* メタデータの必須フィールドチェック
* 参照の整合性検証（循環参照、デッドリンクの検出）

### 6.4 変換・出力

MeDFからの変換：
* **Markdown** - 人間が読みやすい形式
* **HTML** - Web表示用
* **PDF** - 印刷・配布用（従来フォーマットとの互換性）

## 7. セキュリティ考慮事項（Security Considerations）

### 7.1 アクセス制御

* メタデータレベルでのアクセス権限定義
* セクション単位での機密性分類
* 外部参照先の信頼性検証

### 7.2 完全性保証

* チェックサム・ハッシュ値による改ざん検出
* デジタル署名のサポート
* バージョン履歴の追跡

### 7.3 プライバシー

* 個人情報の適切なマスキング
* 機密情報のフィルタリング機構
* 公開範囲の明示的な制御

## 8. 拡張性（Extensibility）

### 8.1 カスタムフィールド

標準フィールド以外に、用途別の拡張フィールドを定義可能：

```json
"metadata": {
  ...
  "custom": {
    "projectCode": "PROJ-2026-001",
    "department": "Engineering",
    "budget": 1000000
  }
}
```

### 8.2 プラグイン機構

* カスタムバリデーター
* 独自の変換処理
* 専用ビューア・エディタ

## 9. 移行パス（Migration Path）

### 9.1 既存フォーマットからの変換

* **PDF → MeDF** - テキスト抽出、構造解析、メタデータ推定
* **Markdown → MeDF** - セクション分割、インデックス生成
* **Word/Excel → MeDF** - 構造化データ抽出、参照の保持

### 9.2 段階的導入

1. **Phase 1**: 新規ドキュメントからMeDF採用
2. **Phase 2**: 重要ドキュメントの変換
3. **Phase 3**: レガシードキュメントのアーカイブ・変換

## 10. まとめ（Summary）

MeDFは、AI時代における新しいドキュメント標準として、以下を実現します：

* ✅ **全体像の可視化** - 構造化メタデータとインデックス
* ✅ **状態の凍結** - スナップショットによる公式記録
* ✅ **分散管理** - 外部ソースへの参照と追跡
* ✅ **機械可読性** - AIによる自動処理・分析
* ✅ **柔軟性** - モジュラー構造と拡張性

MeDFは、情報の記録・共有・活用における新しいパラダイムを提供し、人間とAIの協働を促進します。
