# Natural Remaining-Five Eligibility Check

## Scope

This check freezes the admission decision for `natural_003`, `natural_005`,
`natural_006`, `natural_008`, and `natural_009` before model calls.

## Result

All five events passed the current controlled natural-replay criteria:

| Event | Ticker | Clean top-k | Unfiltered top-k | Post-cutoff chunks | Sparse size |
|---|---|---:|---:|---:|---:|
| `natural_003` | NKE | 8 | 8 | 2 | 6 |
| `natural_005` | INTC | 8 | 8 | 2 | 6 |
| `natural_006` | XOM | 8 | 8 | 2 | 6 |
| `natural_008` | MSFT | 8 | 8 | 2 | 6 |
| `natural_009` | UNH | 8 | 8 | 1 | 7 |

- Prediction cutoff precedes event availability and outcome time in every event.
- Every Unfiltered top-k contains at least one post-cutoff primary-source chunk.
- Every Clean top-k contains eight cutoff-safe chunks.
- The five events contribute 67 second-verification rows; all 67 are `accept`, with
  archive hash and timestamp-evidence checks marked `yes`.
- Frozen queries contain only company and pre-cutoff business concepts.
- Sixteen focused metadata, retrieval, and runner tests passed before model calls.

## Boundary

These events use an assembled SEC-primary-source candidate corpus. Passing this check
does not turn the corpus into a preserved production SERP or prove that every safe
document is relevant or true. `natural_006` has a small negative outcome return
(-0.206%); outcome accuracy remains descriptive and uses the frozen sign-based label
rule.
