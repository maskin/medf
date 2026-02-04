# 正規化ルール（A-3）

MVPでは簡易ルールで固定します。

## テキストエンコーディング

- **UTF-8**
- BOMなし

## 改行コード

- **LF** (`\n`)
- CRLF (`\r\n`) は使用しない

## JSON正規化ルール

### 基本ルール

```json
{
  "key_order": "辞書順（アルファベット順）",
  "whitespace": "なし",
  "ensure_ascii": false,
  "encoding": "UTF-8"
}
```

### 出力例

```json
{
  "document": {
    "title": "Example",
    "content_hash": "sha256:..."
  },
  "intent": {
    "author": "Author Name",
    "description": "Intent description"
  },
  "timestamp": "2026-02-05T12:00:00Z",
  "previous": null
}
```

### 変換ルール

1. **key を辞書順にソート**
   ```python
   json.dumps(obj, sort_keys=True)
   ```

2. **空白を入れない**
   ```python
   json.dumps(obj, separators=(',', ':'))
   ```

3. **ensure_ascii=false**
   ```python
   json.dumps(obj, ensure_ascii=False)
   ```

### 完全な例

```python
import json

# 正規化されたJSON出力
canonical_json = json.dumps(
    obj,
    sort_keys=True,      # 辞書順
    separators=(',', ':'),  # 空白なし
    ensure_ascii=False   # UTF-8許容
)
```

## 実装（Python）

```python
import json
from typing import Any

def normalize_json(obj: Any) -> str:
    """MeDF正規化ルールに従ってJSONを正規化"""
    return json.dumps(
        obj,
        sort_keys=True,      # 辞書順
        separators=(',', ':'),  # 空白なし
        ensure_ascii=False   # UTF-8許容
    )
```

## 実装（JavaScript/Node.js）

```javascript
function normalizeJSON(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort(), 0);
}

// 注意: 標準のJSON.stringifyは空白を入れる
// 空白なしバージョンが必要な場合はカスタム実装
```

## JCS（JSON Canonicalization Scheme）への移行

将来的には **JCS (RFC 8785)** に移行可能：

- JCSは同じ正規化ルールを採用
- key順、空白なし、UTF-8
- MeDFの正規化ルールはJCSのサブセット

現在の簡易ルールは、後でJCSに差し替え可能な設計になっています。

## ハッシュ計算

正規化されたJSON文字列に対してハッシュを計算：

```python
import hashlib

def calculate_hash(obj: Any) -> str:
    """正規化されたJSONのSHA-256ハッシュを計算"""
    canonical = normalize_json(obj)
    return f"sha256:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
```

## 検証時の注意

- パーサによっては順序が保持されない場合がある
- 常に正規化関数を通してからハッシュ計算を行う
- 生のJSON文字列を直接ハッシュしない

## テスト

```python
# 正規化ルールのテスト
obj = {
    "timestamp": "2026-02-05T12:00:00Z",
    "document": {"title": "Example"},
    "intent": {"author": "Author"}
}

# 正規化後（辞書順）
expected = '{"document":{"title":"Example"},"intent":{"author":"Author"},"timestamp":"2026-02-05T12:00:00Z"}'

assert normalize_json(obj) == expected
```

## まとめ

| 項目 | ルール |
|------|--------|
| エンコーディング | UTF-8 (BOMなし) |
| 改行 | LF (`\n`) |
| key順 | 辞書順（アルファベット順） |
| 空白 | なし |
| ASCIIエスケープ | なし（ensure_ascii=false） |
| 将来の拡張 | JCS (RFC 8785) に対応可能 |
