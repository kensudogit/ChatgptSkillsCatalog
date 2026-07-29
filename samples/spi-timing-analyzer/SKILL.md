---
name: spi-timing-analyzer
description: SPI / I2C タイミング図を解釈し、セットアップ・ホールド時間の不足を指摘する。
metadata:
  version: "1.1.0"
  author: digital-design
  category: 設計レビュー
tags: [spi, i2c, timing, digital]
---

# SPI タイミング解析

`references/timing-glossary.md` の用語を使い、必要なら `scripts/parse_edges.py` でエッジ一覧を整理します。

## 入力

- クロック周波数
- セットアップ / ホールド（ns）
- スレーブ型番の最小要件

## 出力

- 補正 / 警告 / OK の三段判定
- マージン計算
