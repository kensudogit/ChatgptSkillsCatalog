---
name: emc-filter-design
description: >
  EMI/EMC フィルタ設計を支援する。
  コモンモードチョーク・X/Y コンデンサ選定時に使用する。
owner: emc-lab
metadata:
  version: "0.9.0"
  author: emc-lab
  category: 設計レビュー
tags:
  - emc
  - filter
  - noise
---

# EMC フィルタ設計

## 手順

1. 対象ポート（AC / DC / I/O）を特定
2. 差動モードとコモンモードを分離
3. L / Cx / Cy の初期値を提案
4. 安全規格（洗聴電流等）を確認

## 出力

- ブロック図（文字）
- 部品候補リスト
- 測定項目
