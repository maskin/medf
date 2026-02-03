# MeDF ユースケース集

このドキュメントでは、MeDFフォーマットの具体的な活用例を紹介します。

## 目次

1. [プロジェクト管理](#プロジェクト管理)
2. [ナレッジマネジメント](#ナレッジマネジメント)
3. [AI活用](#ai活用)
4. [技術文書管理](#技術文書管理)
5. [研究・分析](#研究分析)

---

## プロジェクト管理

### ユースケース1: プロジェクト状態スナップショット

**課題**: 
プロジェクトの現在の状態を、関係者全員が一目で理解できる形で記録・共有したい。

**MeDFでの解決**:

```json
{
  "medf": { "version": "1.0", "schema": "..." },
  "metadata": {
    "id": "project-alpha-snapshot-2026-02",
    "title": "プロジェクトAlpha 2月度状況報告",
    "type": "snapshot",
    "status": "official",
    "created": "2026-02-28T17:00:00Z"
  },
  "index": {
    "toc": [
      {"id": "overview", "title": "概要", "level": 1},
      {"id": "progress", "title": "進捗", "level": 1},
      {"id": "issues", "title": "課題", "level": 1},
      {"id": "decisions", "title": "決定事項", "level": 1}
    ],
    "keywords": [
      {"term": "マイルストーン1", "contexts": ["progress"]},
      {"term": "リスク", "contexts": ["issues"]}
    ]
  },
  "content": {
    "sections": [
      {
        "id": "progress",
        "title": "進捗",
        "type": "data",
        "body": {
          "milestones": [
            {"name": "M1", "status": "完了", "completion": 100},
            {"name": "M2", "status": "進行中", "completion": 65}
          ]
        }
      }
    ]
  },
  "references": {
    "external": [
      {
        "id": "jira-board",
        "type": "other",
        "title": "JIRAボード",
        "url": "https://jira.example.com/board/alpha"
      }
    ]
  }
}
```

**メリット**:
- 特定時点の状態を正確に記録
- 過去のスナップショットと比較可能
- AIが進捗傾向を分析可能
- 外部ツール（JIRA等）へのリンクで詳細確認も容易

---

### ユースケース2: 意思決定の記録

**課題**: 
プロジェクトで行われた重要な決定を、背景・理由・影響と共に記録したい。

**MeDFでの解決**:

```json
{
  "metadata": {
    "id": "decision-log-2026-q1",
    "title": "2026年Q1 意思決定記録",
    "type": "report"
  },
  "content": {
    "sections": [
      {
        "id": "decision-001",
        "title": "フレームワーク選定",
        "type": "data",
        "body": {
          "decision": "React を採用",
          "date": "2026-01-15",
          "decidedBy": ["CTO", "テックリード"],
          "background": "モダンなUIフレームワークが必要",
          "options": [
            {"name": "React", "pros": ["大規模コミュニティ", "豊富なライブラリ"], "chosen": true},
            {"name": "Vue", "pros": ["学習曲線が緩やか"], "chosen": false}
          ],
          "impact": "開発速度20%向上の見込み"
        },
        "annotations": [
          {
            "type": "note",
            "text": "3ヶ月後に効果を再評価",
            "author": "CTO"
          }
        ]
      }
    ]
  }
}
```

**メリット**:
- 意思決定の透明性確保
- 新メンバーへのオンボーディング支援
- 後からの振り返りが容易
- AIが類似状況での決定パターンを学習可能

---

## ナレッジマネジメント

### ユースケース3: 分散ナレッジの統合スナップショット

**課題**: 
Notion、Confluence、GitHub Wikiなど、複数のツールに散在する情報を、特定時点で統合して保存したい。

**MeDFでの解決**:

```json
{
  "metadata": {
    "id": "knowledge-snapshot-2026-02",
    "title": "エンジニアリングナレッジ 2月度スナップショット",
    "type": "snapshot"
  },
  "index": {
    "toc": [
      {"id": "architecture", "title": "アーキテクチャ", "level": 1},
      {"id": "best-practices", "title": "ベストプラクティス", "level": 1},
      {"id": "troubleshooting", "title": "トラブルシューティング", "level": 1}
    ]
  },
  "content": {
    "sections": [
      {
        "id": "architecture",
        "title": "アーキテクチャ",
        "type": "text",
        "body": "2026年2月時点のシステムアーキテクチャ概要...",
        "metadata": {
          "lastVerified": "2026-02-15T10:00:00Z",
          "confidence": 0.95
        }
      }
    ]
  },
  "references": {
    "external": [
      {
        "id": "ref-notion",
        "type": "document",
        "title": "Notion アーキテクチャページ",
        "url": "https://notion.so/team/architecture",
        "accessed": "2026-02-15T10:00:00Z",
        "checksum": "sha256:..."
      },
      {
        "id": "ref-github-wiki",
        "type": "document",
        "title": "GitHub Wiki",
        "url": "https://github.com/team/repo/wiki",
        "accessed": "2026-02-15T10:00:00Z"
      }
    ]
  }
}
```

**メリット**:
- 分散した情報を1つのスナップショットに集約
- 元のソースへのトレーサビリティ保持
- 時系列での変化を追跡可能
- AIが統合ナレッジベースを構築可能

---

### ユースケース4: オンボーディングパッケージ

**課題**: 
新入社員が必要な情報をすべて把握できるパッケージを作りたい。

**MeDFでの解決**:

インデックスを活用して、必要な情報に素早くアクセス：

```json
{
  "metadata": {
    "id": "onboarding-package-2026",
    "title": "新入社員オンボーディング パッケージ",
    "type": "report"
  },
  "index": {
    "toc": [
      {"id": "week1", "title": "1週目", "level": 1, "summary": "環境セットアップと基礎知識"},
      {"id": "week2", "title": "2週目", "level": 1, "summary": "実際の開発プロセス"},
      {"id": "week3-4", "title": "3-4週目", "level": 1, "summary": "チーム協働とベストプラクティス"}
    ],
    "keywords": [
      {"term": "環境セットアップ", "contexts": ["week1"], "definition": "開発環境の構築手順"},
      {"term": "コードレビュー", "contexts": ["week2"], "definition": "PRレビューのガイドライン"}
    ]
  },
  "content": {
    "sections": [
      {
        "id": "week1",
        "type": "text",
        "body": "...",
        "annotations": [
          {"type": "todo", "text": "メンターと1on1を設定"}
        ]
      }
    ]
  }
}
```

**メリット**:
- 構造化された学習パス
- 必要な情報への素早いアクセス
- AIチャットボットがガイドとして機能可能

---

## AI活用

### ユースケース5: AI対話セッションの記録

**課題**: 
AIとの対話で得た知見を、後から検索・参照できる形で保存したい。

**MeDFでの解決**:

```json
{
  "metadata": {
    "id": "ai-session-2026-02-03-design",
    "title": "AI対話: データベース設計レビュー",
    "type": "analysis",
    "authors": [
      {"name": "山田太郎", "role": "creator"},
      {"name": "ChatGPT-4", "role": "contributor"}
    ]
  },
  "index": {
    "toc": [
      {"id": "context", "title": "コンテキスト", "level": 1},
      {"id": "dialogue", "title": "対話ログ", "level": 1},
      {"id": "insights", "title": "得られた知見", "level": 1}
    ],
    "keywords": [
      {"term": "正規化", "frequency": 8, "contexts": ["dialogue"]},
      {"term": "インデックス最適化", "frequency": 5, "contexts": ["insights"]}
    ]
  },
  "content": {
    "sections": [
      {
        "id": "dialogue",
        "type": "data",
        "body": {
          "exchanges": [
            {
              "speaker": "Human",
              "timestamp": "2026-02-03T14:00:00Z",
              "message": "このテーブル設計で問題ありますか？"
            },
            {
              "speaker": "AI",
              "timestamp": "2026-02-03T14:00:30Z",
              "message": "いくつか改善点があります：1. 正規化が不十分..."
            }
          ]
        }
      },
      {
        "id": "insights",
        "type": "text",
        "body": "この対話から得られた主な知見：\n1. 第3正規形まで正規化すべき\n2. クエリパターンに応じたインデックス設計..."
      }
    ]
  }
}
```

**メリット**:
- 対話の完全な記録
- 後から検索・参照可能
- 同様の問題に直面した際の参考資料
- AIが過去の対話から学習可能

---

### ユースケース6: RAG（検索拡張生成）のデータソース

**課題**: 
AIシステムが参照できる、構造化された高品質なドキュメント集が必要。

**MeDFでの解決**:

MeDFドキュメントはそのままRAGのデータソースとして活用可能：

1. **セクション単位でEmbedding生成**
   - 各`section`のbodyをベクトル化
   - メタデータ（importance, confidence）で重み付け

2. **インデックスで効率的検索**
   - キーワード、エンティティで事前フィルタリング
   - 関係性情報で関連セクションを連鎖的に取得

3. **コンテキスト提供**
   - セクションのsummaryで概要把握
   - TOCで全体構造を理解
   - アノテーションで注意事項を確認

**実装例**:

```python
def retrieve_relevant_sections(query, medf_docs, top_k=5):
    # 1. キーワードマッチで候補を絞り込み
    candidates = filter_by_keywords(query, medf_docs)
    
    # 2. Embedding類似度で上位k件を取得
    sections = []
    for doc in candidates:
        for section in doc['content']['sections']:
            embedding = generate_embedding(section['body'])
            score = cosine_similarity(query_embedding, embedding)
            
            # メタデータで重み付け
            if 'metadata' in section:
                if section['metadata'].get('importance') == 'high':
                    score *= 1.5
                score *= section['metadata'].get('confidence', 1.0)
            
            sections.append((section, score))
    
    # 3. 関連セクションも取得
    top_sections = sorted(sections, key=lambda x: x[1], reverse=True)[:top_k]
    related = get_related_sections(top_sections, doc['index']['relationships'])
    
    return top_sections + related
```

**メリット**:
- 構造化データでRAGの精度向上
- メタデータによる信頼性評価
- 関係性情報で文脈を豊かに

---

## 技術文書管理

### ユースケース7: API仕様書のバージョン管理

**課題**: 
API仕様の変更履歴を明確に記録し、各バージョンを参照可能にしたい。

**MeDFでの解決**:

```json
{
  "metadata": {
    "id": "api-spec-users",
    "title": "Users API 仕様書",
    "type": "specification",
    "status": "official",
    "version": "2.1.0",
    "previousVersion": "api-spec-users-v2.0.0",
    "created": "2026-02-01T00:00:00Z"
  },
  "content": {
    "sections": [
      {
        "id": "endpoint-create-user",
        "title": "POST /users - ユーザー作成",
        "type": "data",
        "body": {
          "method": "POST",
          "path": "/users",
          "request": {
            "headers": {"Authorization": "Bearer {token}"},
            "body": {
              "name": "string",
              "email": "string",
              "age": "integer (optional, new in v2.1)"
            }
          },
          "response": {
            "200": {"id": "string", "name": "string", "email": "string", "age": "integer"}
          }
        },
        "metadata": {
          "importance": "high"
        },
        "annotations": [
          {
            "type": "info",
            "text": "v2.1で age フィールドを追加",
            "timestamp": "2026-02-01T00:00:00Z"
          }
        ]
      }
    ]
  }
}
```

バージョン間の差分を別ドキュメントとして記録：

```json
{
  "metadata": {
    "id": "api-changelog-v2.0-to-v2.1",
    "title": "API変更履歴: v2.0 → v2.1",
    "type": "report"
  },
  "content": {
    "sections": [
      {
        "id": "changes",
        "type": "data",
        "body": {
          "added": [
            {"endpoint": "POST /users", "field": "age", "type": "integer"}
          ],
          "deprecated": [],
          "removed": []
        }
      }
    ]
  },
  "references": {
    "internal": [
      {"sourceSection": "changes", "targetSection": "endpoint-create-user"}
    ]
  }
}
```

**メリット**:
- 各バージョンが独立したドキュメント
- 変更履歴の明確な追跡
- 後方互換性の検証が容易

---

## 研究・分析

### ユースケース8: 調査レポート

**課題**: 
市場調査や技術調査の結果を、ソースへの参照と共に記録したい。

**MeDFでの解決**:

```json
{
  "metadata": {
    "id": "market-research-ai-tools-2026",
    "title": "AIツール市場調査レポート 2026",
    "type": "analysis",
    "status": "official",
    "created": "2026-02-10T00:00:00Z",
    "validUntil": "2026-05-10T00:00:00Z"
  },
  "index": {
    "toc": [
      {"id": "executive-summary", "title": "エグゼクティブサマリー", "level": 1},
      {"id": "market-size", "title": "市場規模", "level": 1},
      {"id": "competitors", "title": "競合分析", "level": 1},
      {"id": "trends", "title": "トレンド", "level": 1}
    ],
    "entities": [
      {"name": "OpenAI", "type": "organization", "mentions": ["competitors"]},
      {"name": "Anthropic", "type": "organization", "mentions": ["competitors"]}
    ]
  },
  "content": {
    "sections": [
      {
        "id": "market-size",
        "type": "data",
        "body": {
          "2025": {"size": 150, "unit": "billion USD"},
          "2026": {"size": 200, "unit": "billion USD", "growth": "33%"}
        },
        "metadata": {
          "confidence": 0.85,
          "lastVerified": "2026-02-08T00:00:00Z"
        }
      }
    ]
  },
  "references": {
    "external": [
      {
        "id": "ref-gartner-report",
        "type": "document",
        "title": "Gartner AI Market Report 2026",
        "url": "https://gartner.com/reports/ai-2026",
        "accessed": "2026-02-05T00:00:00Z",
        "status": "active"
      }
    ]
  }
}
```

**メリット**:
- データのソースが明確
- 信頼度（confidence）で情報の確度を表現
- 有効期限で情報の鮮度を管理
- AIが複数レポートを横断分析可能

---

## まとめ

MeDFは以下のシーンで特に有効です：

| シーン | 主な利点 |
|--------|----------|
| プロジェクト管理 | 状態のスナップショット、意思決定の記録 |
| ナレッジマネジメント | 分散情報の統合、検索性の向上 |
| AI活用 | 対話記録、RAGデータソース |
| 技術文書管理 | バージョン管理、変更追跡 |
| 研究・分析 | ソース追跡、信頼度管理 |

MeDFの柔軟な構造により、これら以外のユースケースにも対応可能です。あなたのユースケースをぜひ共有してください！
