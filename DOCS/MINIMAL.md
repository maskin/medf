# MeDF Minimal Structure v0.1

最小構造のMeDF v0.1は、ドキュメントの存在と履歴を記録することに焦点を当てています。

## 基本構造

```json
{
  "medf_version": "0.1",
  "document": {
    "title": "example document",
    "content_hash": "sha256:XXXXXXXX",
    "content_type": "text/markdown",
    "source": "local:file.md"
  },
  "intent": {
    "author": "string",
    "description": "why this document exists"
  },
  "timestamp": "2026-02-05T12:00:00Z",
  "previous": null
}
```

## フィールド説明

| フィールド | 説明 |
|-----------|------|
| `medf_version` | MeDFフォーマットバージョン |
| `document.title` | ドキュメントタイトル |
| `document.content_hash` | コンテンツのハッシュ値 |
| `document.content_type` | コンテンツタイプ（MIMEタイプ） |
| `document.source` | コンテンツの所在（URIまたはローカルパス） |
| `intent.author` | 作者 |
| `intent.description` | ドキュメントの存在理由 |
| `timestamp` | タイムスタンプ（ISO 8601） |
| `previous` | 前のバージョンのハッシュ（nullまたはハッシュ値） |

## 履歴チェーン

`previous`フィールドにより、ドキュメントの更新履歴をチェーンとして表現できます。

### 初版（previous: null）

```json
{
  "previous": null
}
```

### 更新版（previous: 前のバージョンのハッシュ）

```json
{
  "previous": "sha256:XXXXXXXX..."
}
```

## v0.2との違い

| 特徴 | v0.1 Minimal | v0.2 |
|------|-------------|------|
| 構造 | シンプル | 機能豊富 |
| コンテンツ | 参照のみ | 埋め込み |
| ID | なし | ID@timestamp形式 |
| 署名 | なし | JWS署名対応 |
| 履歴 | previousフィールド | 別途管理 |
| 用途 | 個人・軽量 | 公的文書・公式 |

## 使用例

### ローカルファイルの管理

```json
{
  "medf_version": "0.1",
  "document": {
    "title": "Meeting Notes",
    "content_hash": "sha256:abc123...",
    "content_type": "text/markdown",
    "source": "local:notes/2026-02-05.md"
  },
  "intent": {
    "author": "John Doe",
    "description": "Weekly team meeting notes"
  },
  "timestamp": "2026-02-05T12:00:00Z",
  "previous": null
}
```

### リモートリソースの参照

```json
{
  "medf_version": "0.1",
  "document": {
    "title": "Project Proposal",
    "content_hash": "sha256:def456...",
    "content_type": "application/pdf",
    "source": "https://example.com/docs/proposal.pdf"
  },
  "intent": {
    "author": "Jane Smith",
    "description": "Q1 project proposal for review"
  },
  "timestamp": "2026-02-05T14:30:00Z",
  "previous": null
}
```

## ハッシュ計算

`content_hash`は、ソースが指すコンテンツのSHA-256ハッシュ値です。

```bash
# ファイルのハッシュ計算
sha256sum file.md

# 出力例
sha256:abc123...  file.md
```

## 哲学

v0.1 Minimalは以下の原則に従います：

1. **真理性を証明しない**: 「何が正しいか」ではなく「何が存在したか」を記録
2. **意図を記録する**: なぜこのドキュメントが存在するのか
3. **履歴を保全する**: `previous`フィールドで更新の連鎖を表現
4. **シンプルさ**: 最小限のフィールドで本質を記録
