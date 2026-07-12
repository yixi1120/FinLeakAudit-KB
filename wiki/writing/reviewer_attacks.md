# Reviewer Attack Bank

## Attack 1: "This is just an if-statement."

**Risk:** High
**Response:** FinLeakAudit is not merely timestamp filtering. It includes five distinct operators: multi-level temporal availability checking (timezone, after-hours, revision tracking), claim-evidence attribution, support/contradiction verification, quantitative evidence ablation (measuring each evidence's marginal impact on prediction), and leakage-driven forecast revision.

## Attack 2: "Synthetic leakage is artificial."

**Risk:** Medium
**Response:** Synthetic injection is only a controlled premise test. Experiment B must add real timestamped retrieval outputs and manual semantic-leakage labels for ecological validity. We describe leave-one-out changes as marginal sensitivity, not as a causal estimate.

## Attack 3: "LLM may memorize historical events, confusing your results."

**Risk:** Medium
**Response:** We anonymize all entities, dates, products, and events in our PoC experiments to isolate evidence leakage from pretraining memorization. See Experiment A design.

## Attack 4: "Where is the trading simulation / backtest?"

**Risk:** Medium
**Response:** FinLeakAudit is an audit framework, not a trading system. Our evaluation focuses on prediction reliability metrics (leakage rate, evidence support rate, revision effectiveness) rather than backtest returns. However, we include Sharpe and return as supplementary metrics.

## Attack 5: "CARAG already does leakage-free evaluation."

**Risk:** High
**Response:** CARAG is the financial Agentic RAG host-system prior and includes temporal structure in its forecasting setup. FinLeakAudit targets a different output: an evidence-level audit report that identifies which retrieved items were unavailable, which claims they were linked to, how sensitive the forecast was to their removal, and how the forecast was revised.

## Attack 6: "Why not just filter by timestamp?"

**Risk:** High
**Response:** Timestamp filtering is insufficient because: (1) publish_time ≠ available_time (after-hours releases, timezone issues), (2) revised articles have ambiguous timestamps, (3) the key question is not just "is there future evidence?" but "does this future evidence actually drive the prediction?" Timestamp filtering cannot answer question 3.

## Attack 7: "The cost of ablation is too high."

**Risk:** Medium
**Response:** We report the computational cost of ablation and discuss cost-reliability trade-offs. For production use, ablation can be selective (only when leakage is detected) or approximated (using lightweight reranking instead of full re-prediction).

## Attack 8: "Profit Mirage already studies financial-agent leakage."

**Risk:** Critical
**Response:** Profit Mirage is essential prior art and must be cited. Its central leakage lens is agent-level/model-knowledge contamination and leakage-robust financial evaluation. FinLeakAudit narrows the unit of audit to retrieved evidence items and links point-in-time validity to claim attribution, marginal forecast sensitivity, and revision. We do not claim to be the first financial-agent leakage study.

## Attack 9: "Look-Ahead-Bench and leakage-aware forecasting already solve this."

**Risk:** High
**Response:** These works establish the importance of point-in-time and decision-time constraints at the benchmark or forecasting-system level. Our claim is narrower: measure whether a specific retrieved item was unavailable, cited, supportive or contradictory, influential, and removable through an auditable revision. We must include them as baselines or related work rather than presenting temporal validity as an untouched problem.

## Attack 10: "Evidence ablation is already known."

**Risk:** High
**Response:** Correct. Evidence ablation is not our standalone method novelty. The candidate contribution is its integration with financial publication availability, claim-evidence attribution, support/contradiction labels, and leakage-driven forecast revision. We must cite recent forecasting-faithfulness work that already uses ablation and diversionary injection.

## Attack 11: "The 5-case pilot is too artificial to support a paper."

**Risk:** Critical
**Response:** Agree. The pilot only validates the engineering premise. The paper requires a larger timestamped dataset, natural leakage cases, semantic-leakage annotation, filtering baselines, and uncertainty-aware model comparisons. The pilot should be presented as a preliminary study, not the main evidence.
