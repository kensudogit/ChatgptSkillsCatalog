---
name: datasheet-summarizer
description: 電子部品のデータシートから主要仕様・定格・注意点を要約する。PDF やテキストの読み解き時に使用する。
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: ドキュメント
tags: [datasheet, specs, components]
---

# データシート要約

電子部品のデータシートから、設計に必要な仕様と注意点を抽出する Skill です。

## 抽出項目

1. 型番・パッケージ・ピン配置
2. 絶対最大定格（電圧 / 電流 / 温度）
3. 推奨動作条件と電気特性
4. デライティング・動作時間・インターフェース
5. 実装上の注意（デカプリング、布線、熱）

## 出力

表形式で要約し、不明点は「要確認」と明記する。
