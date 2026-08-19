# Show HN: EEL — an append-only audit ledger for self-improving AI agents

> **Title:** Show HN: EEL — six guardrails for a self-improving AI, distilled from 6 arXiv papers
> **URL:** https://github.com/chenhz01/EEL
> **Target:** Hacker News · Show HN

---

## Post body (paste this)

I've been reading the 2026 wave of "self-improving agent" papers, and one stopped me:

**[2608.18066 — On the Fragility of Self-Improving Agents](https://arxiv.org/abs/2608.18066)** shows that a self-improving agent does *not* monotonically get better — it can collapse under **variance, task order, and underspecification**. Same algorithm, different task order, capability craters.

The scary part isn't "AI will misbehave." It's simpler: **when a system rewrites its own rules, memory, and policy, we have no immutable record of what it changed or why.** Fear of runaway is speculation; the absence of an audit trail is a fact.

So I built **EEL (Evolution Evidence Ledger)** — a zero-dependency audit layer that turns six arXiv papers into six *enforceable* guardrails:

- **Variance gate** (2608.18066): reject self-improvements >30% change
- **Evidence fingerprint** (2608.17756): no fingerprint on memory edits → reject
- **Audit ledger** (2608.17684): policy changes need motive+data+backtest
- **Memory-policy consistency** (2608.17247): undeclared state → freeze
- **Reproducible conclusion gate** (2608.17906): irreproducible → demote to hypothesis
- **Uncertainty probe** (2608.17084): unquantified uncertainty → reject

It's one self-contained HTML file (~18KB), append-only ledger persisted in localStorage. Open it and it runs.

**What I'm most interested in being wrong about** — please tear these apart:

1. Is `localStorage` immutability even worth shipping, or is a hash chain table-stakes from day one? (I think the latter; it's on the roadmap but not yet built.)
2. Are these six guardrails actually the *right* distillation of those papers, or did I flatten too much?
3. Is "audit the self-improving agent" even the right problem framing, or is this a solved problem I've missed?

Honest limitations are in the README — I'd rather be corrected than be impressive.

---

# EEL — Evolution Evidence Ledger

## From 6 arXiv papers to an enforceable audit layer

### The claim

A system that modifies itself is not most dangerous when it makes a mistake — it is most dangerous when it makes a mistake and **nobody can tell what changed or why**. EEL makes every evolutionary step of an agent auditable.

### The problem, precisely

[2608.18066](https://arxiv.org/abs/2608.18066) finds self-improvement is **brittle**: capability is a function not only of the algorithm but of *task order* and *specification*. This matters because the current generation of "self-evolving" agents — financial, coding, research — rewrite their own prompts, policies, and memory without a paper trail. When one of them regresses, we cannot answer "what did it change to get here?"

### The design principle

> **Evolution is evidence. Evidence is immutable.**

One rule. Every evolutionary event is written append-only. No deletion, no rewrite. An honest system leaves a complete record of every change it made to itself.

### The six locks

| # | Guardrail | Paper | Enforced rule |
|---|-----------|-------|---------------|
| G1 | Self-Improve Variance Gate | 2608.18066 | Diff capability before/after; >30% → reject |
| G2 | Evidence-Preserving Dual-Loop | 2608.17756 | Memory edits require evidence fingerprint |
| G3 | Self-Evolution Audit Ledger | 2608.17684 | Policy changes require motive+data+backtest |
| G4 | Memory-Policy Consistency | 2608.17247 | Undeclared state → freeze |
| G5 | Reproducible Conclusion Gate | 2608.17906 | Irreproducible → demote to hypothesis |
| G6 | Uncertainty Probe Gate | 2608.17084 | Unquantified uncertainty → reject |

The common property: **these are rejections, not reminders.** A rule that cannot stop a bad evolution from landing is not a guardrail; it is a banner.

### What the MVP is, and is not

The MVP (`eel.html`) is one zero-dependency HTML file: overview, six locks, an append-only ledger, an interactive form that fires the matching guardrail, and the six paper anchors.

It is **not** a faithful reimplementation of the six papers. The guardrail logic is an *executable expression* of their conclusions — provenance, not reproduction. `localStorage` immutability is weak. The 30% variance threshold is heuristic. All of this is stated in the README, because an audit system must first survive being audited.

### Why this matters

The self-improving-agent literature is moving fast; the *governance* of self-improving agents is not. Before we argue about whether agents should be allowed to modify themselves, we need the thing that makes the argument possible: **a record of what they changed.** EEL is a first, deliberately small step toward that record.

### References

- [2608.18066] On the Fragility of Self-Improving Agents — https://arxiv.org/abs/2608.18066
- [2608.17756] D2ACCI: Dual-Loop Diagnostic for Evidence-Preserving Agent Memory — https://arxiv.org/abs/2608.17756
- [2608.17684] Auditing Self-Evolution in Financial Agents — https://arxiv.org/abs/2608.17684
- [2608.17247] Explicit State Elicitation Is Not Enough — https://arxiv.org/abs/2608.17247
- [2608.17906] AutoResearch: Insight In, Hallucination Out — https://arxiv.org/abs/2608.17906
- [2608.17084] Uncertainty-Aware Modality Gate — https://arxiv.org/abs/2608.17084
