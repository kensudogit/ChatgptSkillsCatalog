# Sample Skills（書式バリエーション）

書式研究用のサンプル 10 件です。ZIP は `zips/` 以下に生成されます。

```bash
python scripts/build_sample_skills.py
python scripts/sync_sample_skills.py
```

| # | package | 要点 |
|---|---------|------|
| 01 | `sample-pcb-checklist` | 標準：nested `metadata:` + `tags: [...]` |
| 02 | `bom-cost-review` | 階層型 `version`/`author`/`category` + YAML リスト tags + 表 |
| 03 | `datasheet-summarizer` | 引用符 description + `keywords` （tags 代替） + コードブロック |
| 04 | `esd-protection-guide` | `references/` 伴走ドキュメント |
| 05 | `soldering-process-qa` | `scripts/` 伴走スクリプト |
| 06 | `minimal-frontmatter` | 最小：`name` + `description` のみ |
| 07 | `long-description-warn` | description > 200 文字（Claude 注意） |
| 08 | `emc-filter-design` | YAML `>` 折り返し description + `owner` エイリアス |
| 09 | `spi-timing-analyzer` | references + scripts + NOTES.md の完全パッケージ |
| 10 | `failure-analysis-coach` | When/Instructions/Examples 型の長文 body |

## Claude 互換の共通規則

- `name` は半角小文字・数字・ハイフンのみ
- ZIP 内の親フォルダ名 == `name`
- `description` 必須（1024 文字以内、Claude.ai は 200 文字以内推奨）
