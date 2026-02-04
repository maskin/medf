# MeDF CLI Reference

## コマンド一覧

```bash
medf init        # 雛形JSONを作る
medf hash file   # block_hash / doc_hash を計算
medf verify file # ハッシュ整合性を検証
```

---

## Node.js CLI

```bash
# 雛形JSONを作る
node medf-cli/medf.js init file.md

# ハッシュ計算
node medf-cli/medf.js hash file.md

# 意図を付与してコミット
node medf-cli/medf.js commit file.md --author "name" --intent "description"

# 検証
node medf-cli/medf.js verify file.md.medf.json
```

---

## Python CLI

```bash
# 雛形JSONを作る
python cli/medf.py init file.md

# ハッシュ計算
python cli/medf.py hash file.md.medf.json

# 意図を付与してコミット
python cli/medf.py commit file.md --intent "description" --author "name"

# 検証
python cli/medf.py verify file.md.medf.json
```

---

## 使用例

### 1. ドキュメントの初期化

```bash
# Markdownファイルのハッシュを確認
medf init document.md

# 出力例:
# sha256:abc123...
```

### 2. コミット（意図の記録）

```bash
# 最初のバージョン
medf commit document.md --intent "Initial version" --author "Author Name"

# 更新版
medf commit document.md --intent "Added conclusion section"
```

### 3. ハッシュ計算

```bash
# ドキュメント全体のハッシュ
medf hash document.md.medf.json

# 出力例:
# doc_hash: sha256:abc123...
```

### 4. 検証

```bash
# 整合性確認
medf verify document.md.medf.json

# 出力例:
# ✅ content hash OK
```

---

## ファイル命名規則

- MeDFファイル: `document.md.medf.json`
- 元ファイル: `document.md`
- `.medf.json` 拡張子がMeDFメタデータを示す

---

## 出力形式

### init コマンド

```
sha256:abc123def456...
```

### hash コマンド

```
doc_hash: sha256:abc123...
block_hash: sha256:def456...
```

### verify コマンド

```
✅ content hash OK
```

または

```
❌ content hash MISMATCH
Expected: sha256:abc123...
Actual: sha256:def456...
```

---

## Gitライクなワークフロー

```bash
# 1. ドキュメント作成
echo "# Hello World" > hello.md

# 2. ハッシュ確認
medf init hello.md

# 3. 最初のコミット
medf commit hello.md --intent "First draft"

# 4. ドキュメント更新
echo "" >> hello.md
echo "## Introduction" >> hello.md

# 5. 2回目のコミット
medf commit hello.md --intent "Added introduction"

# 6. 検証
medf verify hello.md.medf.json
```

---

## 論文ユースケース

### ブロック単位のハッシュ計算

```bash
# 論文全体のハッシュ
medf hash paper.md.medf.json

# 出力:
# doc_hash: sha256:abc123...
# block_hash[abstract]: sha256:def456...
# block_hash[methodology]: sha256:789ghi...
# block_hash[results]: sha256:jklmno...
# block_hash[discussion]: sha256:pqrstu...
```

### 論文の引用

```
MEDF: paper-2026-xyz@v3#methodology
```

- `paper-2026-xyz` - 論文ID
- `@v3` - バージョン
- `#methodology` - ブロックID

---

## 偽アカウント防止ユースケース

### 署名付き声明の作成

```bash
# 声明文を作成
echo "This is my official statement." > statement.md

# 署名付きでコミット
medf commit statement.md \
  --intent "Official statement on X" \
  --author "did:example:123" \
  --sign-key ed25519
```

### 同一鍵での継続性検証

```bash
# 過去の声明と同じ鍵か確認
medf verify statement1.md.medf.json
medf verify statement2.md.medf.json

# 両方の public_key が一致すれば「同一人物の継続性」を証明
```

---

## トラブルシューティング

### エラー: File does not exist

```bash
# ファイルパスを確認
ls -la document.md

# 相対パスではなく絶対パスを使用
medf init /path/to/document.md
```

### エラー: Hash mismatch

```bash
# 元ファイルが変更されていないか確認
medf verify document.md.medf.json

# 再コミットが必要
medf commit document.md --intent "Re-commit after changes"
```

### 複数のバージョン管理

```bash
# バージョンごとに別ファイルを作成
cp document.md.medf.json document.v1.md.medf.json
cp document.md.medf.json document.v2.md.medf.json

# それぞれのバージョンを検証
medf verify document.v1.md.medf.json
medf verify document.v2.md.medf.json
```

---

## 仕様との整合性

- ✅ 「正しさを証明しない」→ hash/verify は整合性のみ確認
- ✅ 「存在を記録する」→ commit が状態を記録
- ✅ 「信頼を強制しない」→ 署名は「誰が固定したか」を示すだけ
- ✅ 「オフラインファースト」→ 全コマンドがローカルで動作
