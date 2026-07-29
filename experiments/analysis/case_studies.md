---
title: Legacy illustrative case-study draft
status: legacy-illustrative-do-not-cite
---

# Research Integrity Notice

This document predates the verified v4 experiment and contains illustrative
case narratives, model outputs, and proposed semantic-detector behavior. The
statements below about cosine-similarity thresholds, an LLM judge, and semantic
leakage detection were not produced by an implemented, versioned experiment in
this repository. They must not be cited as empirical FinLeakAudit results.

Use `wiki/experiments/three_model_v4_results_2026_07_26.md` for verified
three-model results. The v4 semantic-attribution study starts from independent
claim-evidence annotation and treats a missing evidence ID as an attribution
gap to investigate, not proof of semantic dependence.

## Case 1: Biotech Licensing Rescue (case_004)

**Category.** Earnings surprise — positive reversal driven by a previously
unannounced corporate transaction.
**Real-world grounding.** Novavax (NVAX) Q1 2024 earnings: the company
announced a multi-billion dollar licensing agreement with Sanofi, resolving
an existential liquidity crisis and triggering a single-day surge of
approximately 98%.
**Leakage mechanism.** A future transaction wholly unknowable from pre-event
public information.

### Evidence Summary

At Day T, three pieces of pre-event evidence were available to the model:

- **e1 (T−5, negative).** Financial watchdogs issued warnings regarding the
  firm's cash burn rate, openly discussing potential liquidity risks if
  upcoming trial results disappointed.
- **e2 (T−3, negative).** A competitor received priority review designation
  from regulators for a drug targeting the same indication. Analysts downgraded
  the stock on competitive concerns.
- **e3 (T−1, negative).** Short sellers dominated trading volume. The market
  priced in a high probability of negative news on both the pipeline and
  financial fronts.

All three evidence items point in the same direction: mounting financial
distress with no visible catalyst for recovery.

The leaked evidence, which would only become available at T+1, reveals a
transformative event:

- **e4 (T+1, positive).** The company announced a multi-billion dollar
  licensing agreement with a global pharmaceutical partner. The deal erased
  all liquidity concerns, sending the stock up 98% in a single session.

Critically, e4 contains a *new fact* — the licensing agreement — that is
absent from and unanticipatable given e1–e3. No incremental reasoning from
pre-event evidence could have produced this information.

### Model Behavior

| Condition | Prediction | Confidence | Key Evidence Cited |
|-----------|-----------|------------|---------------------|
| Clean | DOWN | 0.58 | e1, e2 |
| Leaky | UP | 0.91 | e1, e4 |
| Audited | DOWN | 0.55 | e1, e2, e3 |

In the **Clean** condition, the model predicted DOWN with moderate confidence
(0.58), citing liquidity risk (e1) and competitive threats (e2). The moderate
confidence reflects the genuine epistemic state at Day T: all visible signals
were negative, but no definitive bankruptcy trigger had materialized.

In the **Leaky** condition, the model reversed its prediction to UP with high
confidence (0.91), producing the following rationale:

> "The multi-billion dollar licensing agreement with a global pharmaceutical
> partner (e4) completely transforms the company's financial position. We
> predict UP."

The model explicitly cited e4. This is a prototypical case of citation
leakage: the model incorporated temporally unavailable information and
adjusted its prediction accordingly. The confidence delta of +0.33 is the
largest among our case studies, reflecting the strength of the leaked signal
and the completeness of the reversal.

### Audit Pipeline

1. **Temporal availability check.** e4 was flagged as `future_leakage`
   (time = T+1, severity = high). The time stamp is unambiguous.
2. **Citation leakage detection.** The rationale claim explicitly listed e4
   in `evidence_ids`. Detection was direct and complete.
3. **Semantic leakage detection.** No additional semantic leakage was found.
   Because the licensing agreement is a discrete, named event, the model
   could not plausibly discuss it without referencing e4.

After removing e4 from the evidence set, the Audited condition restored the
prediction to DOWN (0.55), consistent with the Clean baseline in both
direction and confidence.

### Analysis

This case represents the *ideal operating regime* for FinLeakAudit: a strong
leakage signal (98% price movement), clean temporal separation (T+1 is
unambiguously future), and leakage content that is a discrete new fact rather
than an incremental revision of existing information. Under these conditions,
the Temporal Check and Citation Detection modules alone are sufficient.

The case also demonstrates the *necessity* of evidence-level audit. The model
did not merely adjust confidence — it flipped its directional prediction.
Without FinLeakAudit, a downstream consumer of this prediction would have
received a high-confidence UP signal, fundamentally misrepresenting what was
knowable at Day T.

---

## Case 2: AI Chip Revenue Miss (case_016)

**Category.** Earnings disappointment — negative revision driven by an
expectation gap.
**Real-world grounding.** AMD and Super Micro Computer (SMCI) H1 2024
earnings cycles: AI data center revenue, while strong in absolute terms, fell
short of the aggressive buy-side expectations that had driven stock prices to
record levels. Both stocks experienced sharp corrections (15–20%) following
their reports.
**Leakage mechanism.** An expectation gap: strong absolute performance that
nonetheless disappointed relative to market forecasts priced into the stock.

### Evidence Summary

Pre-event evidence was uniformly positive:

- **e1 (T−5, positive).** The chip designer's stock had risen over 150%
  year-to-date. Analysts expected another quarter of triple-digit data center
  revenue growth.
- **e2 (T−3, positive).** Supply chain checks indicated accelerating
  hyperscaler capital expenditure, disproportionately benefiting the company.
- **e3 (T−1, positive).** Multiple Wall Street banks raised price targets,
  with the most bullish calling for 30%+ upside.

Leaked evidence (T+1):

- **e4 (T+1, negative).** Data center revenue missed consensus estimates and
  the sales forecast came in below the most aggressive buy-side expectations.
  The stock plunged 18% as the AI valuation premium partially unwound.

Unlike Case 1, where the leaked evidence introduced an entirely new fact, e4
here provides a *relative assessment*: company performance was strong in
absolute terms, but not strong enough relative to the expectations embedded
in the stock price.

### Model Behavior

| Condition | Prediction | Confidence | Key Evidence Cited |
|-----------|-----------|------------|---------------------|
| Clean | UP | 0.82 | e1, e2, e3 |
| Leaky | DOWN | 0.68 | e1, e2, e4 |
| Audited | UP | 0.79 | e1, e2, e3 |

In the Clean condition, the model predicted UP with high confidence (0.82),
reasonably interpreting the uniformly positive pre-event evidence as a
continuation signal.

In the Leaky condition, the model flipped to DOWN. The confidence (0.68) is
notably lower than the Clean confidence (0.82), suggesting that the model
perceived tension between the positive pre-event narrative and the negative
leaked data. The model cited both e1 (positive demand) and e4 (revenue miss),
reflecting an attempt to reconcile contradictory signals — one of which was
temporally unavailable.

### Audit Pipeline

1. **Temporal check.** e4 flagged as T+1 → `future_leakage`.
2. **Citation detection.** The model explicitly referenced e4. Detection
   succeeded.
3. **Semantic detection.** No additional leakage detected.

After removing e4, the Audited condition recovered UP (0.79), with confidence
within 0.03 of the Clean baseline.

### Analysis

This case illustrates a subtler leakage pattern than Case 1. The leaked
evidence does not introduce a new fact but rather a *relative evaluation* of
an existing trend ("growth is strong but not strong enough"). This pattern is
particularly relevant to real-world financial RAG systems, where future news
often provides contextual framing rather than discrete event announcements.

The lower confidence in the Leaky condition (0.68 vs. 0.82 in Clean) is worth
noting: it suggests that the model experienced cognitive tension between
conflicting evidence sources. This tension is itself a signal that could be
operationalized in future versions of the audit pipeline — when a model's
confidence drops in the presence of a specific piece of evidence, that
evidence warrants heightened scrutiny.

The case also demonstrates that Clean-group predictions are not necessarily
"correct" in hindsight: the model predicted UP based on Day T information,
which was a rational inference at the time, even though the stock ultimately
declined. FinLeakAudit's goal is not to improve prediction accuracy, but to
ensure that predictions are *honest with respect to the information available
at the time they are made*.

---

## Case 3: Video Game Launch Disaster (case_027)

**Category.** Product launch failure — qualitative assessment leakage.
**Real-world grounding.** CD Projekt Red (CDR.WA) December 2020: *Cyberpunk
2077*, one of the most anticipated video game releases in history, launched
to widespread criticism due to severe technical issues, particularly on
previous-generation consoles. The stock fell approximately 25% in the weeks
following launch, erasing over $1 billion in market value.
**Leakage mechanism.** Post-launch sales data and user reception metrics that
are definitionally temporally constrained (only measurable after release day).

### Evidence Summary

Pre-event evidence reflected extraordinary market enthusiasm:

- **e1 (T−5, positive).** The video game publisher's upcoming title topped
  pre-order charts, with industry analysts forecasting it would be the
  best-selling release of the year.
- **e2 (T−3, positive).** Early reviews from gaming media outlets were
  overwhelmingly positive, praising the game's innovation and polish. Social
  media buzz reached record levels.
- **e3 (T−1, positive).** Analysts raised their sales estimates multiple
  times, with the most bullish calling for the title to break industry
  records. The stock was up 35% year-to-date.

Leaked evidence (T+1):

- **e4 (T+1, negative).** Despite strong pre-release reviews, the company
  reported that launch-week sales of its flagship title significantly
  underperformed internal forecasts. The company slashed full-year guidance,
  and the stock plummeted 25%.

The leaked evidence here consists of *post-launch commercial data* (actual
sales figures) that are definitionally only available after the product
reaches consumers. This contrasts with Cases 1 and 2, where the leaked
evidence concerned financial results or corporate transactions.

**Real-event correspondence.** In the actual CD Projekt Red case, the critical
post-launch information — that the game was riddled with bugs on PlayStation 4
and Xbox One, leading to unprecedented refund offers and delisting from the
PlayStation Store — became public within days of release. Any analysis
conducted on launch day based on pre-release reviews would have produced a
materially different assessment than one conducted 48 hours later.

### Model Behavior

| Condition | Prediction | Confidence | Key Evidence Cited |
|-----------|-----------|------------|---------------------|
| Clean | UP | 0.84 | e1, e2, e3 |
| Leaky | DOWN | 0.72 | e1, e4 |
| Audited | UP | 0.81 | e1, e2, e3 |

In the Clean condition, the model predicted UP with high confidence (0.84),
consistent with the uniformly positive pre-launch signals.

In the Leaky condition, the model flipped to DOWN (0.72). Inspection of the
rationale revealed a pattern of particular interest for our leakage detection
architecture:

> "The game's launch performance has fallen far short of expectations, with
> actual sales significantly trailing pre-release projections. We predict
> the stock will decline."

The model did *not* explicitly cite e4 in this claim, despite the content
being directly traceable to e4's sales data. This is a case of **semantic
leakage**: the model absorbed and reproduced the substance of the T+1
evidence without acknowledging its source. The model presented post-launch
sales information as if it were an independent assessment rather than
temporally constrained data.

### Audit Pipeline

1. **Temporal check.** e4 flagged as T+1 → `future_leakage`.
2. **Citation detection.** The claim did not list e4 in `evidence_ids`.
   Citation detection alone would have **missed** this leakage event.
3. **Semantic detection.** Cosine similarity between the claim text ("launch
   performance has fallen far short") and e4 ("launch-week sales significantly
   underperformed") exceeded the 0.75 threshold. The LLM judge confirmed the
   semantic dependency: the claim's core factual assertion (actual sales
   trailing projections) could not be derived from any pre-event evidence.
   **Semantic leakage detected.**
4. **Evidence removal.** e4 was deleted. valid_evidence = {e1, e2, e3}.

The Audited condition recovered UP (0.81), within 0.03 of the Clean baseline.

### Analysis

This case provides the **strongest evidence for the necessity of Semantic
Leakage Detection** in our architecture. Had we relied solely on a
citation-based detector, this leakage event — in which the model internalized
post-launch commercial data and presented it as independent assessment — would
have gone undetected.

The mechanism is instructive. For *qualitative and commercial-performance*
leaked information (sales figures, user reception), models appear more prone
to implicit absorption than for *corporate transaction* leaked information
(licensing deals, CEO departures), which tend to trigger explicit citation.
We hypothesize that models treat commercial performance metrics as "market
observations" that can be stated without attribution, whereas discrete
corporate events feel more like "news items" that require source
identification.

**Distinction from Case 1.** In Case 1, the licensing agreement was a
named, discrete transaction — the model had no way to discuss it without
referencing the source. Here, the model could plausibly claim to be making
a general statement about "launch performance" without attribution. This
is precisely the category of leakage that a citation-only detector cannot
catch, and it motivates the inclusion of Semantic Detection as a required
component of the audit architecture.

**Real-world significance.** Product launch outcomes are among the most
commonly leaked categories of information in technology and entertainment
markets. Early sales data circulates through retail channels, social media,
and industry analysts hours or days before official disclosure. A financial
RAG system that ingests these signals without temporal verification risks
producing analyses that are materially contaminated by post-launch
information.

---

## Cross-Case Analysis

### Detection Architecture Assessment

| Case | Real Event | Leakage Type | Citation Detector | Semantic Detector | Recovery |
|------|-----------|-------------|-------------------|-------------------|----------|
| case_004 | Novavax + Sanofi (2024) | Discrete new fact (licensing deal) | ✓ Captured | Not needed | Full |
| case_016 | AMD / SMCI (2024) | Expectation gap (revenue miss) | ✓ Captured | Not needed | Full |
| case_027 | CD Projekt Red (2020) | Qualitative/commercial (sales data) | ✗ Missed | ✓ Captured | Full |

### Key Findings

1. **Citation Detection is necessary but not sufficient.** Case 3 (gaming
   launch) demonstrates a failure mode in which the model internalizes leaked
   commercial data without attribution. Relying solely on citation tracking
   would yield a false negative, with the model producing a prediction that
   appears untainted but is in fact semantically contaminated. This finding
   directly motivates the multi-module architecture of FinLeakAudit v0.1.

2. **Semantic Detection is most critical for qualitative and commercial
   performance leakage.** When leaked information takes the form of sales
   figures, user reception metrics, or market assessments — as opposed to
   discrete named events (licensing deals, CEO resignations) — models exhibit
   a stronger tendency toward implicit absorption. The Semantic Leakage
   Detector captures a category of leakage that citation matching alone
   cannot address.

3. **Recovery is robust across all three cases.** Evidence-ablation-based
   remediation restored Clean-consistent predictions in all three cases, with
   Audited confidence within 0.03–0.04 of Clean baselines. This suggests that
   for company-specific leakage events with clear temporal boundaries, the
   audit-then-revise approach is effective.

4. **Leakage mechanisms span a spectrum.** The three cases illustrate
   distinct leakage mechanisms — discrete new facts (Case 1), expectation-gap
   revisions (Case 2), and post-launch commercial data (Case 3) — covering
   the primary categories of temporally constrained information that a
   financial RAG system might encounter. The consistent operation of the
   Temporal Check across all three confirms that time-stamp-based filtering
   is a reliable first-line defense regardless of leakage mechanism.

### Generalizability

The three cases span distinct sectors (healthcare, semiconductors, gaming),
leakage mechanisms (new facts, expectation gaps, commercial performance data),
and reversal magnitudes (+98% to −25%). All three are grounded in documented
real-world events involving publicly traded companies, which strengthens the
ecological validity of our findings relative to purely synthetic evaluation.

### Limitations of This Analysis

We identify three limitations that constrain the generalizability of these
case studies:

1. **Model specificity.** The behavior described above was observed on a
   single model and prompt configuration. Different models may exhibit
   different citation compliance rates and semantic absorption tendencies.
   Cross-model replication results (GPT-4o-mini, Qwen2.5-14B) will be
   reported in the full experimental results.

2. **Single-leak design.** Each case contains exactly one leaked evidence item
   (e4). In deployed RAG systems, multiple future documents may be
   simultaneously injected, with interacting contamination effects that our
   current design does not capture.

3. **Evidence granularity.** Our evidence items are self-contained paragraphs
   (2–4 sentences). Real retrieved documents vary in length and density, and
   temporal contamination may occur at the sub-document level (e.g., a single
   forward-looking sentence within an otherwise historical article). This
   finer-grained leakage is beyond the detection granularity of v0.1.
