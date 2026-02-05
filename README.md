# MeDF

**Mutable Expression Description Format** - 文書の状態を固定するためのフォーマット

> 「これは *いつ・誰が・どの意図で* 存在したか」を固定する

---

## 概要

MeDFは、文書そのものを保存・配布するための仕組みではなく、**「ある文書が、ある意図のもとで、その時点に存在した」という状態の記述**を行うためのフォーマットです。

- ✅ **存在の記録** - いつ・誰が・どの意図で
- ✅ **状態の固定** - ハッシュによる不変性
- ✅ **オフラインファースト** - 中央サーバ不要
- ❌ **正しさの証明** - 真偽判定はしない

---

## クイックスタート

```bash
# テンプレート表示
python3 cli/medf.py init

# ハッシュ計算
python3 cli/medf.py hash document.medf.json

# 検証
python3 cli/medf.py verify document.medf.json

# 署名（オプション）
python3 cli/medf.py sign document.medf.json --key private.key
```

---

## 構造

```json
{
  "medf_version": "0.2.1",
  "id": "document-id",
  "snapshot": "2026-02-05T10:00:00Z",
  "issuer": "issuer-code",
  "blocks": [
    {
      "block_id": "introduction",
      "role": "body",
      "format": "markdown",
      "text": "...",
      "block_hash": "sha256:..."
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": "..."
  }
}
```

- **blocks** - 最小意味単位
- **block_hash** - 各ブロックのハッシュ
- **doc_hash** - 文書全体のハッシュ

---

## 引用形式

```
MEDF: paper-2026-example#methodology
```

- `paper-2026-example` - 文書ID
- `#methodology` - ブロックID

---

## CLI

```bash
# テンプレート表示
python3 cli/medf.py init

# ハッシュ計算
python3 cli/medf.py hash document.medf.json

# 検証
python3 cli/medf.py verify document.medf.json

# 署名（オプション）
python3 cli/medf.py sign document.medf.json --key private.key
```

---

## 仕様・思想

- **思想文書**: [思想.md](思想.md)
- **仕様**: [spec/medf.schema.json](spec/medf.schema.json)
- **貢献ガイド**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **ライセンス**: [LICENSE](LICENSE)

---

## ユースケース

- **論文**: セクション単位の参照 (`MEDF: paper-2026-xyz#methodology`)
- **公的文書**: 改定履歴の記録
- **偽アカウント防止**: 鍵の継続性で「同一人物」を証明
- **署名**: 「私が固定した」という主張（信頼ではない）

---

## ライセンス

MIT License - [LICENSE](LICENSE)

**「信頼を強制しない」「中央管理しない」「フォークを恐れない」** - MeDF思想と完全一致

---

## 関連プロジェクト

- **v0.2**: 公的文書仕様（JSON埋め込み型）
- **v0.1**: 最小構造（外部参照型）

---

## Links

- GitHub: https://github.com/maskin/medf
- スキーマ: [spec/medf.schema.json](spec/medf.schema.json)
