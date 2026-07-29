---
name: failure-analysis-coach
description: 電子部品の不具合解析（FA）手順を導く。現象整理・原因仮説・分析手段の選定時に使用する。
metadata:
  version: "1.0.0"
  author: quality-eng
  category: 品質
tags: [fa, quality, 8d]
---

# 不具合解析コーチ

## When to use

- 客先訴え / 工場内不具合
- 再発防止の 8D / FTA 支援

## Instructions

1. **現象**：何が、いつ、どの条件で起きたか
2. **区分**：設計 / 部品 / 工程 / 使用環境
3. **仮説**：3 案以内に絞り、検証手段を提案
4. **証拠**：必要な解析（X線 / SEM / 電気試験）
5. **映像**：映流・再発防止を分けて記述

## Output format

```markdown
## 現象
## 仮説
## 次の動作
## リスク
```

## Examples

**Input:** リフロー後に QFN の開放不良が AOI で多発

**Output:** パスト印刷量 / プロファイル / パッド設計の 3 仮説を優先度付きで提示
