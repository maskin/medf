# MEDF v0.1

MEDF（Mutable Expression Description Format）は、
文書の「内容」ではなく「状態」を固定するためのフォーマットです。

これはCMSでも、ブロックチェーンでも、認証基盤でもありません。

---

## 何ができるか

MEDFは次のことを可能にします。

- 文書をブロック単位で分割し、意味を付与する
- 各ブロックと文書全体にハッシュを付ける
- 「いつ・誰が・どの状態を作ったか」を固定する
- オフラインで改ざん検出を行う
- 履歴を分岐可能な形で残す

---

## 何をしないか

MEDFは以下を行いません。

- 内容の正しさの判定
- 信頼性や権威の付与
- 中央サーバによる管理
- オンライン必須の認証

MEDFは「これは正しいか？」ではなく
「これは *その時点で存在したか*」だけを扱います。

---

## 想定ユースケース

- 論文・技術文書のバージョン固定
- 公的文書・ガイドラインの改訂履歴管理
- 記事・声明文の改ざん検出
- AI生成文書のスナップショット化
- 個人メモや草稿の履歴保存

---

## フォーマット概要

MEDFはJSONで表現されます。

- 文書は `blocks[]` に分割されます
- 各ブロックは意味（role）を持ちます
- 文書全体は `doc_hash` により固定されます
- index や表示用情報は再生成可能です

---

## CLI

MEDFはCLIで生成・検証できます。

```bash
medf init
medf hash document.json
medf verify document.json
```

---

## Node.js CLI (medf-cli/)

```bash
node medf-cli/medf.js init file.md
node medf-cli/medf.js commit file.md --author "you" --intent "first version"
node medf-cli/medf.js verify file.md.medf.json
```

---

## Python CLI (cli/)

```bash
python cli/medf.py init file.md
python cli/medf.py commit file.md --intent "first version" --author "you"
python cli/medf.py verify file.md.medf.json
```

---

## 関連ドキュメント

- [PHILOSOPHY.md](PHILOSOPHY.md) - 思想・哲学
- [DOCS/MINIMAL.md](DOCS/MINIMAL.md) - 最小構造の詳細
- [DOCS/SPEC.md](DOCS/SPEC.md) - v0.2仕様書
