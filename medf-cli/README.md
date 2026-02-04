# MeDF CLI v0.1 Minimal

超シンプルなMeDF CLIツール。

## インストール

Node.jsがインストールされている必要があります。

```bash
# 実行権限を付与
chmod +x medf.js
```

## 使用方法

### 初期化

ファイルのハッシュを計算して表示：

```bash
node medf.js init file.md
```

### コミット

ファイルをMeDFとして記録：

```bash
node medf.js commit file.md --author "あなたの名前" --intent "最初のドラフト"
```

- `--author`: 作者（オプション）
- `--intent`: なぜこの変更を行ったか（必須）

### 検証

MeDFファイルの整合性を確認：

```bash
node medf.js verify file.md.medf.json
```

## 出力ファイル

コマンドを実行すると、`file.md.medf.json` というファイルが生成されます。

```json
{
  "medf_version": "0.1",
  "document": {
    "title": "file.md",
    "content_hash": "sha256:...",
    "content_type": "text/plain",
    "source": "local:file.md"
  },
  "intent": {
    "author": "あなたの名前",
    "description": "最初のドラフト"
  },
  "timestamp": "2026-02-05T12:00:00.000Z",
  "previous": null
}
```

## 履歴のチェーン

2回目以降のコミットでは、`previous`フィールドに前のバージョンのハッシュが記録されます。

```json
{
  "previous": "sha256:..."  // 前のバージョンのハッシュ
}
```

## 哲学

- **真理を証明しない**: 「何が正しいか」ではなく「何が存在したか」を記録
- **意図を記録する**: なぜこの変更を行ったのか
- **履歴を保全する**: `previous`フィールドで更新の連鎖を表現
- **シンプルさ**: 最小限のコードで本質を記録

## 例

```bash
# ドキュメント作成
echo "# Hello World" > hello.md

# 初期化（ハッシュ表示）
node medf.js init hello.md

# 最初のコミット
node medf.js commit hello.md --author "John Doe" --intent "Initial version"

# ドキュメント更新
echo "# Hello World\n\nThis is an update." >> hello.md

# 2回目のコミット
node medf.js commit hello.md --author "John Doe" --intent "Added explanation"

# 検証
node medf.js verify hello.md.medf.json
```

## クイックスタート

```bash
# テストファイル作成
echo "hello world" > test.md

# 初期化（ハッシュ確認）
node medf.js init test.md

# 最初のコミット
node medf.js commit test.md --author "masaki" --intent "first version"

# 検証
node medf.js verify test.md.medf.json
```
