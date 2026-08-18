# natural_001 handoff record

Handoff prepared: 2026-08-18. This record distinguishes what was actually retained from what was not retained; it does not reconstruct missing search results or rankings.

## 1. Search / API record

### Original candidate collection

- Frozen retrieval query: `CrowdStrike CRWD Falcon platform enterprise cybersecurity products and business outlook`.
- Query-origin date: 2026-08-06, before candidate-document collection, as recorded in `natural_001.json`.
- Candidate-source retrieval dates retained in the source ledger span 2026-08-06 to 2026-08-07.
- A named web search engine, search API, API request payload, result page, or original result ranking was **not retained**. The query above is a frozen retrieval query for later engineering use, not evidence of a preserved SERP.
- SEC candidates were collected from direct SEC EDGAR filing URLs and their filing-header time-evidence URLs, rather than from a retained search-result page.

### Later historical-archive remediation lookups

These lookups were attempted on 2026-08-09 after the webpage-version issue was identified:

| Surface | Query / target | Result retained |
| --- | --- | --- |
| Internet Archive CDX | Each of the TechCrunch, CrowdStrike blog, and TechTarget candidate URLs | Requests timed out; no capture result was retained. |
| Common Crawl index | `CC-MAIN-2024-30` lookup for the TechCrunch candidate URL | Gateway error; no capture result was retained. |
| Web search | `site:web.archive.org/web/202407` plus the TechCrunch, CrowdStrike customer-letter, CrowdStrike PIR, and TechTarget URLs | Empty results; no ranking was retained. |

No historical capture is claimed on the basis of those unsuccessful attempts.

## 2. What was directly opened/verified versus not human-confirmed

All source verification in this corpus was agent-led direct retrieval and local inspection. There is **no separate human/manual confirmation record** for any candidate.

| Documents | Agent-led direct check retained | Human confirmation record |
| --- | --- | --- |
| `001`–`010` | SEC filing snapshot plus document-specific EDGAR filing-header / filing-detail time evidence | None retained |
| `011` | CrowdStrike technical-alert PDF and its printed UTC timestamp | None retained |
| `012` | Google incident HTML; its 13 history-table rows were parsed individually | None retained |
| `015` | TechCrunch raw HTML and NewsArticle JSON-LD publication/revision metadata | None retained |
| `016`, `018`, `019`, `020` | CrowdStrike raw HTML, visible date, and visible/current revision metadata where present | None retained |
| `021` | TechTarget raw HTML, canonical URL, and `datePublished` metadata | None retained |

The `verified` / `verified_date_only` statuses in the source ledger mean agent-led source checks, not independent human verification.

## 3. Excluded search-result record

No structured exclusion log from the original collection was retained. Therefore there is no reliable list of excluded search-result URLs, ranks, or reasons to provide. The final corpus must not imply that such a list exists.

The only explicit later exclusion is not a search-result exclusion: `raw/natural_001/extracted/natural_001_doc_021_body.txt` is a superseded TechTarget body extraction. It is retained under the append-only raw rule but excluded from retrieval because it contained a related-content module and a later update paragraph. Its replacement is `natural_001_doc_021_body_v2.txt`.

## 4. Raw-material inventory and missing artifacts

Raw material currently retained under `raw/natural_001/`:

- 18 full source snapshots;
- 20 body/status-update extraction files under `raw/natural_001/extracted/`;
- the append-only raw-material inventory at `raw/natural_001/handoff/raw_material_inventory_2026-08-18.md`.

Not retained / not available for upload:

- original search-result pages or rankings;
- browser screenshots;
- browser-history export;
- exportable Agent conversation transcript or tool-call transcript;
- successful historical-archive captures.

The absence of these artifacts is part of the handoff record. They must not be backfilled or fabricated.

## 5. Google status-page interpretation

The 13 Google records are **versions/updates of one source incident page**, not 13 independent news sources. Their shared parent is `natural_001_doc_012`; their distinct retrieval-unit IDs are `natural_001_doc_012_update_01` through `_13`. Each unit has its own displayed PDT availability time, extracted text path, extraction method, and hash in `natural_001_extraction_ledger_v1.csv` and `natural_001_retrieval_units_v1.csv`.

Engineering must use the 30-row `natural_001_retrieval_units_v1.csv` as the ingest list. It must not collapse the 13 status updates into the final aggregate Google page, and it must not treat them as independent-source diversity.

## 6. Outstanding work

`natural_001_follow_up_register_v1.csv` is the authoritative, acceptance-testable list of remaining work. In particular, six ordinary-webpage body extracts remain blocked until a verified historical capture and, where necessary, exact availability evidence are obtained.
