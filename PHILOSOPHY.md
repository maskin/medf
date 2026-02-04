# MeDF 思想（v0.1）

## 1. MEDFとは何か

MEDF（Mutable Expression Description Format）は、
文書そのものを保存・配布・評価するための仕組みではない。

MEDFが扱うのは、
「ある文書が、ある意図のもとで、その時点に存在した」
という **状態の記述**である。

---

## 2. 正しさを決めない

MEDFは以下を行わない。

- 真偽の判定
- 内容の評価
- 権威付け
- 優劣の決定

MEDFは「これは正しいか？」ではなく、
「これは *いつ・誰が・どの意図で* 存在したか」を固定する。

---

## 3. 外部保存前提

MEDFは文書の実体を保持しない。

- 文書はローカルファイル、Git、Web、PDF、印刷物など、
  どこにあってもよい
- MEDFはそれらを **参照し、ハッシュで指し示す**

これにより、
保存方式・流通方式・表示方式から自由である。

---

## 4. ハッシュは責任の境界線

MEDFにおけるハッシュは、
改ざん検知のためのものであり、
信用や正当性を保証するものではない。

ハッシュが示すのは、
「この状態からは変わっていない」という事実のみである。

---

## 5. 履歴は鎖として表現される

MEDFは更新を上書きしない。

- 各状態は previous により連結される
- 履歴は分岐してよい
- 正史は存在しない

履歴は議論の材料であり、
統合される必要はない。

---

## 6. オフラインファースト

MEDFは以下を前提とする。

- ネットワーク接続不要
- 中央サーバ不要
- 外部API不要

オンラインサービスは**オプション**であり、
MEDFの成立条件ではない。

---

## 7. JSONを採用する理由

JSONは思想ではなく「妥協」である。

- 人が読める
- 機械が扱える
- CLIで生成できる
- 将来別フォーマットに変換できる

MEDFはJSONに固定されない。

---

## 8. MEDFが目指すもの

MEDFは、
- 論文
- 公的文書
- 仕様書
- 記事
- 個人のメモ

といった文書を、
**評価から切り離したまま**
履歴として扱える世界を目指す。

それは「信頼を強制しない記録」である。

---

## English Version

MeDF is a document intent framework.

This system does not verify truth.
It records existence, authorship, and evolution.

A document may change.
Its history must not disappear.

Hash is not proof of correctness.
Hash is proof of presence.
