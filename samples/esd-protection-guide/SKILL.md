---
name: esd-protection-guide
description: ポートや IC の ESD 保護設計を指導する。TVS・クランプ・ボードレベル対策の確認時に使用する。
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: 信頼性
tags: [esd, protection, reliability]
---

# ESD 保護ガイド

入出力ポートや IC の ESD 保護設計を確認する Skill です。

## チェックリスト

1. 保護デバイス（TVS 等）がコネクタ直近にある
2. クランプ電圧が被保護端子の耐圧以下
3. 放電パスが短く、グラウンドへの戻りが明確
4. コモンモード / ディファレンシャルの区別
5. IEC 61000-4-2 等の目標レベルと整合

## 出力

不足点と改善案を優先度付きで列挙する。
