# Step Bで固定された思想（重要）

## 思想の法文化

以下の4つがMeDFの核心を定義します。

## 1. block が 最小意味単位

MeDFにおける「ブロック」は、これ以上分割できない最小の意味単位です。

```json
{
  "blocks": [
    {
      "block_id": "abstract",
      "role": "abstract",
      "format": "markdown",
      "text": "...",
      "block_hash": "sha256:..."
    }
  ]
}
```

- `block_id` - ブロックの一意識別子
- `role` - ブロックの役割（abstract, methodology, results等）
- `format` - テキストフォーマット（markdown, plain等）
- `text` - 実際の内容
- `block_hash` - ブロックのハッシュ

### なぜblockが最小単位なのか

- ドキュメントをさらに細かく分割できない
- 各ブロックは独立して参照可能
- `MEDF: paper-2026-xyz@v3#methodology` のような参照が可能

## 2. index は 自由・非正規

`index` フィールドは、検索や表示用の自由なフィールドです。

```json
{
  "index": {
    "title": "...",
    "summary": "...",
    "tags": [...],
    "custom_field": "..."
  }
}
```

- ✅ どのような構造でもOK
- ✅ 必須フィールドはない
- ✅ ハッシュ計算には含まれない
- ✅ MeDFの本質ではない

### なぜindexが自由なのか

- MeDFは「状態の固定」に集中する
- 検索や表示は「外部の問題」
- 実装ごとに最適な構造でOK

## 3. signature は 任意

署名は必須ではなくオプションです。

```json
{
  "signature": {
    "algorithm": "ed25519",
    "value": "base64...",
    "public_key": "base64...",
    "signed_at": "2026-02-05T12:00:00Z",
    "signer": "did:example:123"
  }
}
```

- ✅ あってもなくてもよい
- ✅ ある場合は「誰が固定したか」を示す
- ✅ 信頼を強制しない
- ✅ 「この署名があるから正しい」ではない

### なぜsignatureが任意なのか

- MeDFは「正しさを証明しない」
- 署名は「誰が記録したか」を示すだけ
- 署名なしでもMeDFとして成立

## 4. schema が MEDF の境界線

JSON Schemaが「これはMeDFか？」を判定する境界線になります。

```
✅ JSON Schemaに適合 → これはMeDF
❌ JSON Schemaに不適合 → これはMeDFではない
```

### なぜschemaが境界線なのか

- **CLIの挙動を事後的に正当化しない**
- **第三者が別実装できる状態にする**
- **「これはMEDFか？」を機械で判定できる**

これは思想の法文化フェーズです。

---

## MEDFの境界線

### 必須要素（Core）

```json
{
  "medf_version": "0.2.1",
  "id": "...",
  "snapshot": "...",
  "issuer": "...",
  "blocks": [...]
}
```

### オプション要素（Optional）

```json
{
  "doc_hash": {...},
  "signature": {...},
  "index": {...}
}
```

### MEDFではない例

❌ YAMLファイル
```yaml
version: "0.2.1"
blocks: [...]
```

❌ Markdownファイル
```markdown
# Title
...
```

❌ 不正なJSON（schema不適合）
```json
{
  "version": "0.2.1",  // medf_version ではない
  "block": "single"     // blocks ではない
}
```

---

## まとめ

👉 **「これはMEDFではない」**と言える根拠が生まれました。

| 要素 | 役割 | 必須/任意 |
|------|------|-----------|
| `blocks` | 最小意味単位 | 必須 |
| `index` | 自由・非正規 | 任意 |
| `signature` | 固定者の表明 | 任意 |
| `schema` | MEDFの境界線 | - |

### 設計の原則

1. **block が最小意味単位** - これ以上分割できない
2. **index は自由** - ハッシュ計算対象外
3. **signature は任意** - 信頼の付与ではない
4. **schema が境界線** - 機械的判定可能

これにより、MeDFは明確な境界線を持つフォーマットになりました。
