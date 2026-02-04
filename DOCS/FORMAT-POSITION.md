# Step 2｜YAML / Markdown 拡張案（採用しない理由を仕様化）

## 結論

**MEDFの正規表現は JSON のみ**

YAML / Markdown は 入力・表示の派生表現に限定

これは技術選択ではなく、**事故防止の思想**です。

---

## なぜ YAML を正にしないか

### 問題点

1. **同一意味でも表現が無限にある**
   ```yaml
   # これらは全て同じ意味だが、異なるハッシュ
   key: value
   key: "value"
   key: 'value'
   key:
     value
   ```

2. **パーサ差異でハッシュ不一致が起きる**
   - YAML 1.1 vs 1.2
   - ライブラリごとの実装差異
   - 暗黙的な型変換ルール

3. **コメント・アンカー・暗黙型が事故源**
   - コメントはハッシュ計算に含まれるべきか？
   - アンカー（&ref, *ref）はどう扱う？
   - 暗黙的な文字列/数値変換

👉 **ハッシュ前提の仕様と相性が悪い**

### 位置づけ

- YAML → JSONに変換してから MEDF 化
- YAMLファイルそのものは元本にならない
- YAMLは入力フォーマットに過ぎない

---

## なぜ Markdown を正にしないか

### 問題点

1. **レンダラ差異が大きい**
   - CommonMark vs GFM vs Pandoc
   - 改行の解釈（スペース1個 vs 2個）
   - リストのネスト解釈

2. **拡張（GFM / Pandoc 等）が地雷**
   - GitHub独自の拡張構文
   - Pandocの独自フィルタ
   - 各種レンダラの方言

3. **メタ埋め込み（YAML Frontmatter）が思想破壊**
   ```markdown
   ---
   title: "Document"
   ---
   ```
   これはMarkdownそのものではなく、YAML+Markdownの複合フォーマット

👉 **レンダラ依存でハッシュが不安定**

### 位置づけ

- Markdownは `blocks[].text` の `format` の一種
- 解釈はレンダラ責任、MEDFは関知しない
- Markdownファイルそのものは元本にならない

---

## 仕様としての一文（重要）

```
MEDFは、意味の正規化を行わない。
MEDFは、状態の固定のみを行う。
```

これで拡張論争は仕様上終了です。

---

## 変換プロセス

### YAML → MeDF

```
YAMLファイル
  ↓ (yaml2json)
JSON
  ↓ (medf commit)
MeDF (.medf.json)
```

### Markdown → MeDF

```
Markdownファイル
  ↓ (ファイル読み込み)
内容のハッシュ計算
  ↓ (medf commit)
MeDF (.medf.json)
```

**重要**: Markdownの内容そのものではなく、ファイル全体のハッシュを記録

---

## JSON のみを正規表現とする理由

| 特性 | JSON | YAML | Markdown |
|------|------|------|----------|
| 表現の一意性 | ✅ | ❌ | ❌ |
| パーサの安定性 | ✅ | ⚠️ | ❌ |
| ハッシュ計算の容易さ | ✅ | ❌ | ❌ |
| 人間可読性 | ✅ | ✅ | ✅ |
| 機械可読性 | ✅ | ✅ | ⚠️ |

---

## 派生表現としての扱い

### 入力フォーマットとしての YAML/Markdown

- YAMLファイル → JSON変換 → MeDF作成
- Markdownファイル → ハッシュ計算 → MeDF作成
- これらは「ワークフロー」であり「フォーマット」ではない

### 表示フォーマットとしての Markdown

- MeDFの `content` フィールドにMarkdownを含めることはOK
- あくまで「文字列データ」として扱う
- レンダリングは外部の責任

---

## 仕様上の明確化

### 認めること

- YAMLファイルを入力として使用する
- Markdownファイルを入力として使用する
- MeDFの `content` にMarkdownを含める
- MeDFからMarkdownを生成する

### 認めないこと

- YAMLファイルそのものをMeDFとして扱う
- MarkdownファイルそのものをMeDFとして扱う
- YAML/Markdownの構文的正規化をMeDFが行う

---

## 実装ガイドライン

### CLI ツールの実装

```bash
# ✅ 良い例
medf commit document.md --intent "..."  # Markdownを入力として使用
medf convert config.yaml document.medf.json  # YAML→JSON変換して使用

# ❌ 悪い例
medf init document.md  # MarkdownそのものをMeDFとして扱う
medf validate document.yaml  # YAMLそのものを検証
```

### ハッシュ計算

```javascript
// ✅ 正しいアプローチ
const hash = sha256(jsonString);  // 正規化されたJSON

// ❌ 誤ったアプローチ
const hash = sha256(yamlString);  // パーサ依存のYAML
```

---

## よくある質問

### Q1. YAMLの方が人間に優しくない？

A: YAMLは人間に優しいが、ハッシュ計算には不向き。YAMLで書いて、JSONで保存するワークフローを推奨。

### Q2. Markdownはなぜ `content` に含めるの？

A: `content` は「文字列データ」として扱っているだけで、Markdown構文を解釈していない。レンダリング差異は利用者の責任範囲。

### Q3. 将来的にYAML/Markdownサポートも？

A: 「派生表現」としてのサポートはあるが、「正規表現」として採用することはない。これは仕様上の決定。

---

## まとめ

1. **MeDFの正規表現はJSONのみ** - これは技術選択ではなく思想
2. **YAML/Markdownは派生表現** - 入力・表示に限定
3. **意味の正規化は行わない** - 状態の固定のみ
4. **事故防止の思想** - パーサ差異やレンダラ差異を排除
