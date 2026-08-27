# EEL — Evolution Evidence Ledger

> 🇨🇳 **中文版见 [README.zh-CN.md](README.zh-CN.md)** ｜ 中文导读（费曼学习法助读版）：[docs/中文导读-费曼学习法助读版.md](docs/中文导读-费曼学习法助读版.md) ｜ **定律草案（L1–L6）**：[docs/laws.md](docs/laws.md)

> **TL;DR (中文)**：一个会改自己的 AI，最危险的不是改错了，而是改错了却没人知道改了啥、为什么改。EEL 是一本 append-only 的「进化账本」：AI 每次自我改进（改规则/改记忆/改策略）必须记一笔账——何时改、为何改、依据什么。6 篇 arXiv 论文 → 6 条硬性拒绝护栏（G1–G6）。

> **Quick start (1 行命令)**：`start eel.html`（零依赖零构建，浏览器直接打开即用；或 `python -m http.server 8000` 后访问 `/eel.html`）

---

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

Open [`eel.html`](eel.html) in any browser. No build step, no server, no dependencies. This is the **public demo edition** — it shows the six-lock rules and guardrail logic.

- **Ledger overview** — total blocks, pass / rollback / demote counts
- **Six locks** — each with its paper anchor (clickable arXiv link)
- **Record an event** — pick an event type, the matching guardrail fires and returns PASS / ROLLBACK / DEMOTE
- **Simulate** — see how each of the six locks rejects bad evolution

> 💡 **The full edition (hash-chain engine) is available to collaborators only.**
> The complete deliverable — SHA-256 hash-chain engine with tamper detection, dual-loop storage design, value-alignment kernel, consensus protocol, CLI verifier and 17 invariant tests — is **not published here** by design. It is offered to serious collaborators who want to build on it together.
> **Contact for the full manuscript: see "Collaborate" below.**

### v0.2.0 deliverable map (public: blueprint only)

| Area | Public blueprint | Full edition (collaborators) |
|---|---|---|
| Block protocol | [`docs/protocol-v1.0.md`](docs/protocol-v1.0.md) — schema & chain rules | — |
| Hash-chain engine | conceptual (tamper detection described) | **working engine + CLI verifier + 17 invariant tests** |
| Dual-loop storage | [`docs/storage-dual-loop.md`](docs/storage-dual-loop.md) | — |
| Value kernel | [`docs/value-alignment-core.md`](docs/value-alignment-core.md) | — |
| Consensus & notify | [`docs/consensus-protocol.md`](docs/consensus-protocol.md) | — |
| Recursive sandbox | [`docs/recursive-sandbox.md`](docs/recursive-sandbox.md) | — |
| Toolchain & formal checks | [`docs/toolchain-roadmap.md`](docs/toolchain-roadmap.md) | **test suite + verifier** |

## Collaborate

EEL is an open research direction — **the ideas are public, the implementation is the manuscript.** If you are building self-improving-agent governance, AI alignment tooling, or agent audit infrastructure and want the full working edition, reach out:

- **Email:** `zhengming.eel@gmail.com` (replace with actual address before pushing) <!-- CONTACT-PLACEHOLDER -->

Let's exchange notes on what you're building — the full manuscript goes to serious collaborators.

## Honest limitations (read before judging)

This project is honest about what it is and is not:

1. **The guardrail logic is an *executable expression of rules*, not a faithful reimplementation of the 6 papers.** D2ACCI's full dual-loop protocol, for example, is far more elaborate than one `if`. Treat the anchors as provenance, not as "we shipped the paper."
2. **The public edition has no hash-chain engine.** The SHA-256 chain implementation exists in the full manuscript (collaborators only). Even there, `localStorage` is a weak guarantee against a determined local adversary — an attacker who rewrites the chain and re-hashes every block produces a "valid-looking" chain. The defense is **external anchoring** (publishing the chain head to git / a notary) per `docs/storage-dual-loop.md`. Server-side signing remains the hard answer.
3. **Thresholds (e.g. the 30% variance gate) are heuristic**, not empirically calibrated.
4. **The design documents (value kernel, consensus, sandbox) are blueprints, not shipped code** — P0 items are flagged in each doc; production deployment requires implementing and validating them.

An audit system must first survive being audited itself. These limitations *are* the sixth-and-a-half lock.

## Roadmap

- [x] **Hash-chain version** — designed (protocol v1.0, tamper-detection architecture); **working implementation is in the full manuscript, offered to collaborators**
- [ ] **Integration** — hook EEL into a live self-evolving agent's daily loop
- [ ] **i18n** — English UI (current UI is Chinese)
- [ ] **Empirical calibration** — run EEL on a real self-improving agent, measure variance / rollback rate, and publish numbers
- [ ] **External anchoring** — publish chain head hash weekly to git / notary (design in `docs/storage-dual-loop.md`)
- [ ] **Multi-agent consensus** — implement PBFT+VRF per `docs/consensus-protocol.md` (P0 messaging first)

## Paper anchors

- [2608.18066] *On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification* — https://arxiv.org/abs/2608.18066
- [2608.17756] *D2ACCI: A Dual-Loop Diagnostic Protocol for Evidence-Preserving Agent Memory* — https://arxiv.org/abs/2608.17756
- [2608.17684] *Auditing Self-Evolution in Financial Agents* — https://arxiv.org/abs/2608.17684
- [2608.17247] *Explicit State Elicitation Is Not Enough: Memory-Policy Audit* — https://arxiv.org/abs/2608.17247
- [2608.17906] *AutoResearch: Insight In, Hallucination Out* — https://arxiv.org/abs/2608.17906
- [2608.17084] *Uncertainty-Aware Modality Gate* — https://arxiv.org/abs/2608.17084

## Also in this repo

- **[cognitive-memory-engine](cognitive-memory-engine/)** (中文) — *Spaced Repetition × Decision-Coupling Memory Engine*: a design article plus 40 actionable specs (cog-001~040) from a cognitive-scientist advisor, anchored to 20 arXiv papers. Core claim: spaced repetition should feed the decision system's confidence weights, not just memory consolidation.
- **[polarization-depolarization-engine](polarization-depolarization-engine/)** (中文) — *Multi-Agent Group Polarization & Depolarization Engine*: GraphWake (2608.17665) memory-mediated polarization cascade turned into a four-layer defense (detect → dampen → immunize → audit) with 12 actionable specs (depol-001~012) distilled from four advisor brainstorms.
- **[delegation-asymmetry-engine](delegation-asymmetry-engine/)** (中文) — *Delegation Responsibility Asymmetry Engine*: three-dimensional delegation asymmetry (information / goal / capability) from 2608.18058 turned into a four-layer defense (contract → execute → monitor → audit), with 12 specs (deleg-001~012) anchored on an auditable delegation contract.
- **[versioned-workspace-engine](versioned-workspace-engine/)** (中文) — *Versioned Workspace Engine*: StagedWorkspace (2608.18050) turned into a four-layer versioning mechanism (staging → commit → recovery → collaboration), turning irreversible knowledge-work errors into reversible ones, with 12 specs (vers-001~012).
- **[capability-collapse-defense](capability-collapse-defense/)** (中文) — *Capability Collapse Defense*: the fragility of self-improving agents (2608.18066) turned into a runtime defense line (detect → isolate → recover → benchmark) that complements EEL's audit ledger, with 12 specs (clps-001~012).
- **[preference-consistency-engine](preference-consistency-engine/)** (中文) — *Preference Consistency Gate*: LLM-derived preference judgments are not self-consistent (2608.17644) — each-with-evidence judgments can still fight each other. Adds the third loop (set-level consistency) after EEL's G2 evidence loop, with 12 specs (cons-001~012): multi-framing scoring, transitivity & indifference-point checks, interval pricing instead of point estimates, regret tracking, drift audits.
- **[verification-protocol-engine](verification-protocol-engine/)** (中文) — *Verification Protocol Engine*: a single successful observation is not a validated estimate (2608.17744 noise floor: random-seed swaps move scores 7.7 pts; 2608.17724 VERaiPHY statistical standards). Any "prove it then scale it" move needs an explicit protocol: what to test, sample size, confidence line — with 12 specs (verf-001~012).
- **[innovation-metric-engine](innovation-metric-engine/)** (中文) — *Innovation Metric Engine*: 96.8% of AI-generated "new" methods live inside the human design space and nearly half are exact copies (2608.17471). Any claim of "new" must carry a module-level diff report (reuse / recombine / new), with 12 specs (innv-001~012).
- **[living-benchmark-engine](living-benchmark-engine/)** (中文) — *Living Benchmark Engine*: conclusions expire — static-benchmark leaders re-rank dramatically under prequential evaluation on future data (2608.17299). Every deposited claim needs a time-sensitivity tag and a re-test cycle; expired conclusions auto-demote, with 12 specs (live-001~012).
- **[preformulation-gap-engine](preformulation-gap-engine/)** (中文) — *Preformulation Gap Engine*: rubrics grade the deliverable, not the opening — 9/12 model units gave advice before the patient answered a single question (2608.17330). Assessment must move to first-contact behavior, with 12 specs (pref-001~012).

## License

[MIT](LICENSE)
