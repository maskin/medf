# MeDF 開発進捗状況

## プロジェクト概要

**MeDF (Meaning-anchored Document Format)** は、URL中心の参照モデルから脱却し、**ドキュメントそのものを意味単位で安定的に引用・再利用可能**にするドキュメントフォーマットです。

**開発期間**: 2026年2月4日開始
**現在のバージョン**: v0.2 (Public Document Specification)

---

## 実装完了項目

### 1. コア仕様

#### v0.1 基本仕様
- ✅ 単一JSON形式での実装
- ✅ メタデータ構造定義
- ✅ SHA-256ハッシュによる内容保証
- ✅ Markdownベースのコンテンツ記述
- ✅ インデックス構造（タイトル、要約、セクション、タグ、キーワード）
- ✅ 参照元情報の記録

#### v0.2 公的文書仕様
- ✅ ID@timestamp形式の識別子（例: JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z）
- ✅ ドキュメントタイプ（public_notice, guideline, press_release, report, white_paper, official_statement）
- ✅ 責任主体オブジェクト（name, code, department）
- ✅ fenced blockベースのMarkdown拡張
- ✅ JWS署名フィールドの定義
- ✅ 拡張フィールドによる柔軟性

### 2. スキーマ定義

- ✅ `schema/medf-v0.1.schema.json` - v0.1バージョンのJSON Schema
- ✅ `schema/medf-v0.2-public.schema.json` - v0.2公的文書向けJSON Schema

### 3. CLIツール

#### 機能
- ✅ Markdown → MeDF 変換 (`convert` コマンド)
- ✅ MeDF バリデーション (`validate` コマンド)
- ✅ MeDF → HTML 変換 (`to-html` コマンド)
- ✅ ハッシュ計算 (`hash` コマンド)
- ✅ ハッシュ検証 (`verify` コマンド)

#### オプション
- ✅ v0.1/v0.2 の切り替え
- ✅ ドキュメントタイプ指定
- ✅ 権威機関情報の指定
- ✅ 参照URIの追加
- ✅ スナップショット時刻の指定

### 4. サンプルファイル

- ✅ `examples/tourism-policy-2024-03.medf` - v0.1形式のサンプル
- ✅ `examples/JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z.medf` - v0.2形式のサンプル

### 5. ドキュメント

- ✅ README.md - 全体説明と使い方
- ✅ requirements.txt - 依存パッケージ

---

## 実装のポイント

### データ構造

v0.2の基本構造：
```json
{
  "medf_version": "0.2",
  "document_type": "guideline",
  "id": "JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z",
  "snapshot": "2026-02-04T10:00:00Z",
  "hash": {
    "algorithm": "sha-256",
    "value": "..."
  },
  "authority": {
    "name": "国土交通省",
    "code": "JP-MLIT",
    "department": "観光庁"
  },
  "content": "# Markdown content...",
  "index": {...},
  "references": [...],
  "extensions": {}
}
```

### ハッシュ計算対象

ハッシュ計算には以下のフィールドが含まれます：
- `id`
- `snapshot`
- `authority`
- `content`
- `index` (存在する場合)
- `references` (存在する場合)

**除外項目**:
- `medf_version` (バージョン情報)
- `hash`フィールド自体
- `signature`フィールド
- `extensions`フィールド

### Markdown拡張

セクションブロック：
```markdown
```medf-section
id: executive-summary
role: executive_summary
```

# セクションタイトル

コンテンツ...
```
```

---

## 次のステップ (開発計画詳細は ROADMAP.md を参照)

### 優先度高
1. **実在PDFのMeDF化デモ**
   - 実際の公的文書PDFをMeDFに変換
   - 変換プロセスの検証

2. **JWS署名機能の実装**
   - 電子署名の生成
   - 署名の検証機能

3. **引用表記の標準化**
   - 論文形式での引用例
   - 脚注形式の引用例

### 優先度中
4. **バリデータの強化**
   - セクション構造の検証
   - Markdown拡張のパース

5. **CLIツールの機能追加**
   - 一括変換機能
   - 差分表示機能

6. **ツールの改善**
   - Pythonパッケージ化
   - インストーラの作成

### 優先度低
7. **拡張機能**
   - 他形式からの変換（PDF→MeDF）
   - バイナリ添付機能
   - マルチ言語サポート

---

## 技術スタック

- **言語**: Python 3.7+
- **ライブラリ**:
  - `markdown`: Markdown→HTML変換
  - `jsonschema`: JSON Schema検証
- **フォーマット**: JSON, Markdown

---

## ファイル構成

```
mdf/
├── cli/                    # CLIツール
│   ├── __init__.py
│   └── medf.py
├── schema/                 # JSON Schema
│   ├── medf-v0.1.schema.json
│   └── medf-v0.2-public.schema.json
├── examples/               # サンプルファイル
│   ├── tourism-policy-2024-03.medf
│   └── JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z.medf
├── DOCS/                   # ドキュメント
│   ├── PROGRESS.md         # 進捗状況
│   ├── ROADMAP.md          # 開発計画
│   └── SPEC.md             # 技術仕様
├── README.md
└── requirements.txt
```

---

## 更新履歴

### 2026-02-04
- ✅ v0.2 公的文書仕様の実装完了
- ✅ ID@timestamp形式の導入
- ✅ ドキュメントタイプの追加
- ✅ CLIツールのv0.2対応
- ✅ JSON Schemaの更新
- ✅ サンプルファイルの作成
- ✅ ドキュメントの整理
