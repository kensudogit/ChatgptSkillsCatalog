---
name: soldering-process-qa
description: リフロー・流動はんだ付け工程の品質チェックリスト。SMT プロファイル・不具合・工程窓の確認時に使用する。
metadata:
  version: "1.0.0"
  author: mfg-qa
  category: 製造
tags: [smt, soldering, quality]
---

# はんだ付け工程 QA

プロファイル CSV は `scripts/check_profile.py` で予備検査できます。

## 確認項目

1. 上昇 / ピーク / 冷却が部品要件内
2. パスト厚み・アパーチャ・クリーニング
3. 橋の小屋 / ボイド / 心偏せ / 未はんだ
