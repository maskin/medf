# MeDF 技術仕様書 v0.2

**Meaning-anchored Document Format**

---

## 1. 概要

### 1.1 目的

MeDFは、URL中心の参照モデルから脱却し、**ドキュメントそのものを意味単位で安定的に引用・再利用可能**にするドキュメントフォーマットである。

### 1.2 位置づけ

- **URL**: 「輸送路」
- **MeDF**: 「意味と状態の固定層」

### 1.3 コア要件

1. **意味中心**: 「何であり、いつの状態か」を指す
2. **元本性**: ハッシュによる状態固定、改変不可
3. **引用性**: URLに依存しない安定した引用
4. **可動性**: 紙レイアウト非依存、ブロック指向
5. **機械可読**: AIによる検証・比較・分析が可能

---

## 2. 公的文書における要件

### 2.1 最重要要件

- **元本性（Originality）**: 文書の原本性を保証
- **非改ざん性（Integrity）**: 改変の検出が可能
- **時点固定性（Snapshot性）**: 特定の時点での状態を記録
- **長期参照性**: 10年〜100年スパンでの安定参照
- **人間可読性と機械可読性の両立**

### 2.2 位置づけ

MeDFは「編集可能なワークドキュメント」ではなく、**公式状態を確定させるための意味的スナップショット**として機能する。

---

## 3. 基本構造

### 3.1 3層構造

MeDF公的文書は以下の3層構造を取る：

1. **メタデータ層（Metadata）**: 文書の識別・分類
2. **意味本文層（Meaning Body）**: 実際の内容
3. **署名・検証層（Verification）**: 署名と検証情報

これらは**単一ファイル**として配布・保存される。

### 3.2 単一JSON形式

メタデータはJSONで定義する。YAML等は禁止（曖昧性排除）。

```json
{
  "medf_version": "0.2",
  "document_type": "public_notice",
  "id": "JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z",
  "snapshot": "2026-02-04T10:00:00Z"
}
```

---

## 4. フィールド定義

### 4.1 必須フィールド

| フィールド | 型 | 説明 |
|-----------|------|------|
| `medf_version` | string | MeDFフォーマットバージョン（例: "0.2"） |
| `document_type` | string | ドキュメントタイプ |
| `id` | string | ドキュメントID（ID@timestamp形式） |
| `snapshot` | string | スナップショット時刻（ISO 8601） |
| `hash` | object | ハッシュオブジェクト |
| `authority` | object | 責任主体オブジェクト |
| `content` | string | メインコンテンツ（Markdown） |

### 4.2 ドキュメントタイプ

- `public_notice`: 公告
- `guideline`: ガイドライン
- `press_release`: プレスリリース
- `report`: 報告書
- `white_paper`: 白書
- `official_statement`: 公式声明
- `academic_paper`: 論文（拡張）
- `blog_post`: ブログ記事（拡張）

### 4.3 ID@timestamp形式

**形式**: `[ID]@[ISO8601-TIMESTAMP]`

**例**: `JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z`

- **ID**: 意味的同一性を示す識別子
- **@timestamp**: 状態固定点

### 4.4 発行主体（Issuer, v0.2）

```json
{
  "issuer": "JP-MLIT"
}
```

- `issuer`: 発行主体コード（例: JP-MLIT, JP-CA）
- 形式: `[国コード2文字]-[組織コード]`

### 4.5 発行時刻（Issued At, v0.2）

```json
{
  "issued_at": "2026-02-04T10:00:00Z"
}
```

- `issued_at`: 発行時刻（ISO 8601形式）
- `snapshot`と異なる場合、文書の発行日時を記録

### 4.6 言語（Language, v0.2）

```json
{
  "language": "ja"
}
```

- `language`: 言語コード（ISO 639-1）
- 形式: `ja`, `en`, `zh` または `ja-JP`, `en-US` のような地域コード付き

### 4.7 責任主体（Authority）

```json
{
  "name": "国土交通省",
  "code": "JP-MLIT",
  "department": "観光庁"
}
```

- `name`（必須）: 組織名または個人名
- `code`: 組織コード
- `department`: 部署名

### 4.5 ハッシュ（Hash）

```json
{
  "algorithm": "sha-256",
  "value": "9f3a1b2c..."
}
```

- **アルゴリズム**: sha-256, sha-384, sha-512
- **ハッシュ対象**: id, snapshot, authority, content, index, references

**ハッシュ計算対象外**:
- `medf_version`
- `hash`フィールド自体
- `signature`フィールド
- `extensions`フィールド

### 4.6 インデックス（Index）

```json
{
  "title": "ドキュメントタイトル",
  "summary": {
    "short": "1行要約",
    "medium": "2-3行要約",
    "full": "詳細な要約"
  },
  "sections": [
    {
      "id": "sec-1",
      "title": "セクションタイトル",
      "level": 1,
      "role": "executive_summary",
      "summary": "セクションの要約"
    }
  ],
  "tags": ["タグ1", "タグ2"],
  "keywords": ["キーワード1", "キーワード2"]
}
```

#### セクションの役割（role）

- `executive_summary`: 概要
- `introduction`: 序論
- `background`: 背景
- `policy`: 方針
- `principles`: 原則
- `methodology`: 方法論
- `results`: 結果
- `discussion`: 考察
- `conclusion`: 結論
- `decisions`: 決定事項

### 4.7 参照情報（References）

```json
{
  "references": [
    {
      "uri": "https://example.com/doc",
      "type": "source",
      "title": "参照先タイトル",
      "retrieved": "2026-02-04T10:00:00Z",
      "medf_id": "JP-XXX-2026-DOC@2026-02-04T10:00:00Z"
    }
  ]
}
```

#### 参照タイプ

- `source`: 元文書
- `related`: 関連文書
- `citation`: 引用
- `supplement`: 補足資料

### 4.8 署名（Signature, オプション）

```json
{
  "signature": {
    "algorithm": "ES256",
    "value": "eyJhbGciOiJFUzI1NiJ9...",
    "signer": "did:example:12345",
    "timestamp": "2026-02-04T10:00:00Z"
  }
}
```

#### JWSアルゴリズム

- **ECDSA**: ES256, ES384, ES512
- **RSA**: RS256, RS384, RS512

### 4.9 拡張フィールド（Extensions）

```json
{
  "extensions": {
    "custom": {
      "department": "国際観光課",
      "contact": "tourism@example.go.jp",
      "document_number": "令和8年第1号"
    }
  }
}
```

拡張フィールドはハッシュ計算対象外。

---

## 5. Markdown拡張

### 5.1 セクションブロック

```markdown
```medf-section
id: executive-summary
role: executive_summary
```

# セクションタイトル

コンテンツ...
```
```

### 5.2 参照ブロック

```markdown
:::reference{uri="https://example.com/doc"}
参照先の説明...
:::
```

### 5.3 注釈ブロック

```markdown
:::note{type=background}
注釈内容...
:::
```

#### 注釈タイプ

- `background`: 背景
- `supplement`: 補足
- `warning`: 注意
- `info`: 情報

---

## 6. 引用モデル

### 6.1 自然言語中での引用

```
MeDF: JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z によれば...
```

### 6.2 脚注形式

```
[1] MeDF: JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z
    snapshot: 2026-02-04T10:00:00Z
    authority: 国土交通省
    hash: 9f3a...
```

### 6.3 元本指定引用

URLではなく、識別子そのものが引用単位となる：

- 再配布されても意味は変わらない
- 鏡サイト・ローカル保存でも成立
- AI・人間双方が同一対象を参照

---

## 7. PDFとの関係性

### 7.1 役割分担

| フォーマット | 役割 |
|-------------|------|
| PDF | 表示・印刷最適化 |
| MeDF | 意味・公式性・参照最適化 |

### 7.2 位置づけ

PDFはMeDFから**派生生成物**として生成される。元本は常にMeDF。

---

## 8. PDF→MeDF変換

### 8.1 捨てるもの

- ページ番号
- 段組・余白
- フォント指定

### 8.2 保持・強化するもの

- 発行主体（issuer）
- 発行時点（issued_at）
- 意味構造（背景／方針／決定）

---

## 9. 論文フォーマット

### 9.1 MeDF論文の基本構造

- **メタデータ**: 著者・所属・査読情報・確定時点
- **本文**: 意味セクション単位
- **引用**: 意味ID@timestamp

### 9.2 セクション構造

```medf-section
id: introduction
role: intro
```

```medf-section
id: method
role: methodology
```

```medf-section
id: result
role: results
```

```medf-section
id: discussion
role: discussion
```

### 9.3 ページレス引用

| 従来（PDF） | MeDF |
|-----------|------|
| ページ番号 | 意味ブロックID |
| 段組 | セクション構造 |
| 図表番号 | 図表ID@timestamp |

### 9.4 効果

- 引用がレイアウト非依存になる
- AIが論理構造を直接参照可能
- 長期的知識アーカイブに適合

---

## 10. 非圧縮の思想

人間が直接読めることを優先する。圧縮は流通レイヤーで対応し、**元本は常に非圧縮**。

これは「MeDFは保存形式であり、転送最適化形式ではない」という思想を明確にする。

---

## 11. ファイル形式

### 11.1 拡張子

- `.medf`

### 11.2 MIMEタイプ

- `application/medf+json`

### 11.3 マジックナンバー

- `{"medf_version":"` で開始

---

## 11. 思想概念の防御

MeDFの思想的中核を守るために、想定される代表的な反論に応答する。

### 11.1 「HTMLで十分ではないか？」

HTMLは表示・配信のための優れたフォーマットであるが、以下の点でMeDFとは目的が異なる。

- HTMLは常に「現在の状態」を指す
- URLは意味ではなく場所を示す
- 内容更新と公式性が分離されにくい

MeDFは、**『ある意味内容が、ある時点で公式に確定した』**という状態を固定するためのフォーマットであり、HTMLとは補完関係にある。

### 11.2 「Gitで管理すればよいのでは？」

Gitは履歴管理・差分管理に優れるが、以下の点で公的文書用途には不足がある。

- Gitのコミットは社会的公式性を持たない
- ハッシュは人間にとって意味的参照にならない
- ブランチ文化は制度文書と相性が悪い

MeDFは、**Gitの外側で『公式確定点』を示すアンカー**として機能する。

### 11.3 「AIが要約・理解すれば十分では？」

AIは可変的な解釈主体であり、要約結果そのものは公式ではない。

MeDFは、
- AIが参照すべき元本
- AIの解釈対象

を固定するための前提層である。

### 11.4 「結局PDFの焼き直しでは？」

PDFは視覚的同一性を保証するが、意味構造・参照安定性は副次的である。

MeDFは、
- 視覚ではなく意味を固定
- レイアウトを派生物と定義

する点で、役割が根本的に異なる。

### 11.5 MeDFが"やらないこと"

MeDFは以下を意図的に行わない。

- 編集支援
- リアルタイム共同作業
- 表示最適化
- ワークフロー管理

これらを排除することで、**意味確定フォーマットとしての純度を保つ**。

---

## 12. 総括

MeDFは、

> 意味を、時点と責任主体とともに固定する

という一点に集中する。

それ以外は、意図的に外部に委ねる。

この設計こそが、MeDFを一過性の技術ではなく、**長期的に機能する社会的インフラ**にする。

---

## 13. バージョン管理

### 13.1 バージョン番号

- メジャー: 互換性のない変更
- マイナー: 後方互換性のある追加
- パッチ: バグ修正

### 13.2 互換性

異なるバージョン間の互換性は、明示的な変換ツールを通じて保証する。

---

## 付録A: 完全な例

```json
{
  "medf_version": "0.2",
  "document_type": "guideline",
  "id": "JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z",
  "snapshot": "2026-02-04T10:00:00Z",
  "hash": {
    "algorithm": "sha-256",
    "value": "b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9"
  },
  "authority": {
    "name": "国土交通省",
    "code": "JP-MLIT",
    "department": "観光庁"
  },
  "content": "```medf-section\nid: executive-summary\nrole: executive_summary\n```\n\n# 持続可能な観光推進ガイドライン\n\n...",
  "index": {
    "title": "持続可能な観光推進ガイドライン",
    "summary": {
      "short": "オーバーツーリズム対策と持続可能な観光の推進に関する基本方針",
      "medium": "インバウンド需要の急速な回復を踏まえ...",
      "full": "2023年の訪日外客数が2,500万人を超える水準に回復する中..."
    },
    "sections": [...],
    "tags": ["観光", "ガイドライン", "持続可能な観光"],
    "keywords": ["持続可能な観光", "オーバーツーリズム", "分散型観光"]
  },
  "references": [...],
  "extensions": {}
}
```
