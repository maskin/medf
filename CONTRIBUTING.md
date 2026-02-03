# Contributing to MeDF

MeDFプロジェクトへの貢献を歓迎します！このガイドでは、プロジェクトに貢献する方法を説明します。

## 貢献の種類

### 1. フィードバック・提案

- 仕様に関する質問や提案
- ユースケースの共有
- 改善アイデア

**方法**: GitHubのIssuesで新しいissueを作成してください。

### 2. ドキュメントの改善

- 誤字脱字の修正
- わかりにくい説明の改善
- 翻訳（英語版ドキュメント等）
- 新しい例の追加

**方法**: Pull Requestを作成してください。

### 3. 仕様の拡張・改善

- JSON Schemaの改善
- 新しいフィールドの提案
- 既存仕様の改善

**方法**: まずIssuesで議論し、合意が得られたらPull Requestを作成してください。

### 4. ツールの開発

- バリデーター・パーサーの改善
- 変換ツール（Markdown ⇔ MeDF等）
- ビューア・エディタ
- ライブラリ（Python, JavaScript等）

**方法**: Pull Requestを作成してください。大規模な変更の場合は事前にIssuesで相談してください。

## Pull Requestのガイドライン

### コミットメッセージ

明確で簡潔なコミットメッセージを書いてください。

```
良い例:
- Add validation for metadata.authors field
- Fix typo in SPECIFICATION.md
- Add example for API documentation use case

悪い例:
- Fix bug
- Update
- Changes
```

### ブランチ命名

機能追加や修正ごとに新しいブランチを作成してください。

```
feature/add-api-example
fix/schema-validation-error
docs/improve-usage-guide
```

### Pull Requestの説明

以下の情報を含めてください：

1. **変更の目的**: なぜこの変更が必要か
2. **変更内容**: 何を変更したか
3. **テスト**: どのようにテストしたか（該当する場合）
4. **関連Issue**: 関連するIssue番号（該当する場合）

## コーディング規約

### JSON

- インデント: 2スペース
- 文字コード: UTF-8
- 改行コード: LF (Unix形式)

### Python

- PEP 8に準拠
- Type hints の使用を推奨

### Markdown

- 1行は100文字以内を推奨
- 見出しの前後に空行を入れる

## 仕様変更のプロセス

大きな仕様変更は以下のプロセスで行います：

1. **提案**: Issueで提案し、議論する
2. **RFC**: 必要に応じてRFC（Request for Comments）ドキュメントを作成
3. **レビュー**: コミュニティでレビュー
4. **実装**: 合意が得られたら実装
5. **ドキュメント更新**: SPECIFICATION.md等を更新
6. **バージョンアップ**: 変更の影響に応じてバージョンを更新

## テスト

### JSON Schemaの検証

スキーマを変更した場合は、すべての例が検証を通過することを確認してください。

```bash
python3 validate.py examples/*.medf.json
```

### 新しい例の追加

新しい例を追加する場合は：

1. 適切なファイル名（`{name}.v{version}.medf.json`）で作成
2. バリデータで検証
3. examples/README.md に説明を追加

## ライセンス

このプロジェクトに貢献することにより、あなたの貢献が同じライセンス（LICENSEファイルを参照）の下で公開されることに同意したものとみなされます。

## 行動規範

- 敬意を持って接する
- 建設的なフィードバックを提供する
- 多様な視点を尊重する
- プロフェッショナルな態度を保つ

## 質問・サポート

質問がある場合は：

1. まず[SPECIFICATION.md](SPECIFICATION.md)と[USAGE_GUIDE.md](USAGE_GUIDE.md)を確認
2. 既存のIssuesを検索
3. 解決しない場合は新しいIssueを作成

## メンテナーへの連絡

緊急の問題や非公開で相談したい場合は、プロジェクトメンテナーに直接連絡してください。

---

貢献してくださりありがとうございます！🎉
