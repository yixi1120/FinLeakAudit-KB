# Reviewer Attack Bank

## Attack 1: "This is just an if-statement."

**Risk:** High
**Response:** FinLeakAudit is not merely timestamp filtering. It includes five distinct operators: multi-level temporal availability checking (timezone, after-hours, revision tracking), claim-evidence attribution, support/contradiction verification, quantitative evidence ablation (measuring each evidence's marginal impact on prediction), and leakage-driven forecast revision.

## Attack 2: "Synthetic leakage is artificial."

**Risk:** Medium
**Response:** We include BOTH synthetic leakage injection (Experiment A) and natural leakage audit on real RAG outputs (Experiment B). Synthetic experiments establish causality; natural audits establish ecological validity.

## Attack 3: "LLM may memorize historical events, confusing your results."

**Risk:** Medium
**Response:** We anonymize all entities, dates, products, and events in our PoC experiments to isolate evidence leakage from pretraining memorization. See Experiment A design.

## Attack 4: "Where is the trading simulation / backtest?"

**Risk:** Medium
**Response:** FinLeakAudit is an audit framework, not a trading system. Our evaluation focuses on prediction reliability metrics (leakage rate, evidence support rate, revision effectiveness) rather than backtest returns. However, we include Sharpe and return as supplementary metrics.

## Attack 5: "CARAG already does leakage-free evaluation."

**Risk:** High
**Response:** CARAG evaluates leakage at the system level (post-cutoff evaluation). FinLeakAudit audits leakage at the evidence level — identifying WHICH specific pieces of evidence caused leakage, WHICH prediction claims they supported, and HOW removing them changes the forecast.

## Attack 6: "Why not just filter by timestamp?"

**Risk:** High
**Response:** Timestamp filtering is insufficient because: (1) publish_time ≠ available_time (after-hours releases, timezone issues), (2) revised articles have ambiguous timestamps, (3) the key question is not just "is there future evidence?" but "does this future evidence actually drive the prediction?" Timestamp filtering cannot answer question 3.

## Attack 7: "The cost of ablation is too high."

**Risk:** Medium
**Response:** We report the computational cost of ablation and discuss cost-reliability trade-offs. For production use, ablation can be selective (only when leakage is detected) or approximated (using lightweight reranking instead of full re-prediction).
