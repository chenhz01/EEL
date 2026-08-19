# EEL — Evolution Evidence Ledger

> An append-only audit layer that turns **6 arXiv papers into enforceable guardrails** for self-improving AI agents.

**The claim:** a system that modifies itself is not most dangerous when it makes a mistake — it is most dangerous when it makes a mistake and *nobody can tell what changed or why*. EEL makes every evolutionary step of an agent auditable.

---

## The problem

[arXiv:2608.18066](https://arxiv.org/abs/2608.18066) — *On the Fragility of Self-Improving Agents* — shows that self-improving agents do **not** monotonically get better: they can collapse under **variance, task order, and underspecification**. Same algorithm, different task order, and capability can crater.

The deeper point is not "AI will misbehave." It is that **we currently have no immutable record of how a self-modifying system changed itself.** Fear of runaway is speculation; *the absence of an audit trail is a fact.*

## What EEL is

EEL is a minimal, zero-dependency audit layer. Its one design principle:

> **Evolution is evidence. Evidence is immutable.**

Every evolutionary event — self-improvement, memory edit, policy change, conclusion emission, multimodal decision — is written **append-only** and never deleted or rewritten.

## The six locks

Each guardrail is a *paper conclusion turned into an enforceable rule* — not a reminder, a **rejection**:

| # | Guardrail | Paper | Enforced rule |
|---|-----------|-------|---------------|
| G1 | Self-Improve Variance Gate | [2608.18066](https://arxiv.org/abs/2608.18066) | Diff capability before/after each self-improvement; **reject if change > 30%** |
| G2 | Evidence-Preserving Dual-Loop | [2608.17756](https://arxiv.org/abs/2608.17756) | Memory edits must carry an **evidence fingerprint**; no fingerprint → reject |
| G3 | Self-Evolution Audit Ledger | [2608.17684](https://arxiv.org/abs/2608.17684) | Policy changes must record **motive + data + backtest**; missing any → reject |
| G4 | Memory-Policy Consistency | [2608.17247](https://arxiv.org/abs/2608.17247) | Verify memory↔policy consistency on state transition; undeclared state → freeze |
| G5 | Reproducible Conclusion Gate | [2608.17906](https://arxiv.org/abs/2608.17906) | Conclusions must be reproducible; otherwise **demote to "hypothesis"** |
| G6 | Uncertainty Probe Gate | [2608.17084](https://arxiv.org/abs/2608.17084) | Quantify uncertainty before multimodal decisions; unquantified → reject |

## Quick start

Open [`eel.html`](eel.html) in any browser. No build step, no server, no dependencies.

- **Ledger overview** — total events, pass / rollback / demote counts
- **Six locks** — each with its paper anchor (clickable arXiv link)
- **Event ledger** — append-only table, newest first
- **Record an event** — pick an event type, the matching guardrail fires and returns PASS / ROLLBACK / DEMOTE
- **Persistence** — the ledger survives reloads via `localStorage`

## Honest limitations (read before judging)

This project is honest about what it is and is not:

1. **The guardrail logic is an *executable expression of rules*, not a faithful reimplementation of the 6 papers.** D2ACCI's full dual-loop protocol, for example, is far more elaborate than one `if`. Treat the anchors as provenance, not as "we shipped the paper."
2. **`localStorage` immutability is a weak guarantee.** It prevents accidents, not adversarial local tampering. Real immutability needs a **hash chain** (each event carries the previous event's SHA-256) or server-side signing. That is the next step, not yet shipped.
3. **Thresholds (e.g. the 30% variance gate) are heuristic**, not empirically calibrated.

An audit system must first survive being audited itself. These limitations *are* the sixth-and-a-half lock.

## Roadmap

- [ ] **Hash-chain version** — SHA-256 linkage so tampering is detectable
- [ ] **Integration** — hook EEL into a live self-evolving agent's daily loop
- [ ] **i18n** — English UI (current UI is Chinese)
- [ ] **Empirical calibration** — run EEL on a real self-improving agent, measure variance / rollback rate, and publish numbers

## Paper anchors

- [2608.18066] *On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification* — https://arxiv.org/abs/2608.18066
- [2608.17756] *D2ACCI: A Dual-Loop Diagnostic Protocol for Evidence-Preserving Agent Memory* — https://arxiv.org/abs/2608.17756
- [2608.17684] *Auditing Self-Evolution in Financial Agents* — https://arxiv.org/abs/2608.17684
- [2608.17247] *Explicit State Elicitation Is Not Enough: Memory-Policy Audit* — https://arxiv.org/abs/2608.17247
- [2608.17906] *AutoResearch: Insight In, Hallucination Out* — https://arxiv.org/abs/2608.17906
- [2608.17084] *Uncertainty-Aware Modality Gate* — https://arxiv.org/abs/2608.17084

## License

[MIT](LICENSE)
