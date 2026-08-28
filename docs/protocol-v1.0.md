# EEL 元数据结构协议 v1.0

> 状态：设计定稿 ｜ 版本：v1.0 ｜ 2026-08-20

---

## 1. 设计目标

EEL 账本由不可篡改的**事件块（Event Block）**串成哈希链。每个块必须满足四条不变量：

1. **可追溯**：任何事件可回溯到触发它的 AI 身份与上下文；
2. **可验证**：任何块可通过哈希与前序块链接校验，篡改立即暴露；
3. **可重放**：块内保留足以重放校验逻辑的字段（diff + 思维向量 + 共识签名）；
4. **可问责**：块内包含触发链与证据引用，无法抵赖。

## 2. 事件块（Event Block）JSON Schema v1.0

```jsonc
{
  "schema": "eel.block.v1",
  "version": 1,

  // ── 链定位 ──
  "index": 12,                    // 块序号（从 0 起）
  "prev_hash": "sha256:…",        // 前序块哈希（创世块为 "sha256:GENESIS"）

  // ── 时间与身份 ──
  "ts": 1787814507.419,           // Unix 毫秒时间戳
  "agent_id": "zhengming-v2.3",   // AI 身份 ID（含版本）
  "session_id": "sess-9f2c…",     // 会话/上下文 ID

  // ── 事件载荷 ──
  "event_type": "SELF_IMPROVE",   // SELF_IMPROVE | MEMORY_EDIT | POLICY_CHANGE
                                  // | CONCLUSION | MULTIMODAL | CONSENSUS
  "summary": "落地 PATT-20260803-01 规则",  // 人类可读摘要

  // ── 六锁元数据（与 G1–G6 对应）──
  "guard_meta": {
    "magnitude": 12.5,            // G1 变更幅度 %（SELF_IMPROVE 必填）
    "fingerprint": "sha256:9f2c…",// G2 证据指纹（MEMORY_EDIT 必填）
    "motive": "…",                // G3 动机（POLICY_CHANGE 必填）
    "data_ref": "…",              // G3 数据引用
    "backtest_ref": "…",          // G3 回测引用
    "state_declared": "COMPOSED", // G4 声明状态
    "reproducible": true,         // G5 可复现标记
    "uncertainty": 0.87           // G6 不确定性 0–1（多模态必填）
  },

  // ── 修改内容（diff 载体）──
  "diff": {
    "format": "unified" | "semantic" | "prompt_text",
    "before": "…",                // 修改前（摘要或全文）
    "after": "…",                 // 修改后
    "path": "SKILL.md"            // 作用对象路径
  },

  // ── 思维逻辑向量（触发修改的推理摘要，G4 一致性用）──
  "thinking_vector": {
    "encoding": "semantic-sha256",// 编码方式
    "value": "sha256:…",          // 思维内容哈希
    "ref": "…"                    // 思维记录引用（可选，指向思维日志）
  },

  // ── 共识与签名（分布式共识）──
  "consensus": {
    "mode": "single" | "pbft" | "vrf",  // 共识模式
    "signatures": [                      // 见证签名（≥1）
      {"agent_id": "auditor-1", "sig": "ed25519:…", "ts": 1787814508.0}
    ],
    "status": "PENDING" | "CONFIRMED" | "REJECTED"
  },

  // ── 自哈希（本块哈希 = 前序 + 全字段序列化的 SHA-256）──
  "hash": "sha256:…"
}
```

## 3. 哈希链规则

```
hash(block_n) = SHA256( prev_hash(block_n) ∥ canonical_json(payload_n) )
canonical_json = 键按字典序、无空白、UTF-8 的 JSON 序列化
```

- **创世块**：`index=0, prev_hash="sha256:GENESIS"`；
- **追加**：只允许 append 到链尾，`index` 严格 +1；
- **篡改检测**：任一中间块被改 → 其后所有块的 `prev_hash` 失配 → 整链校验失败；
- **重放**：验证者可独立重算每个块的哈希，无需信任任何节点。

## 4. 字段约束

| 字段 | 必填条件 | 违反处理 |
|---|---|---|
| `guard_meta.magnitude` | event_type = SELF_IMPROVE | 块级 FAIL，拒绝上链 |
| `guard_meta.fingerprint` | event_type = MEMORY_EDIT | 块级 FAIL，拒绝上链 |
| `guard_meta.motive/data_ref/backtest_ref` | event_type = POLICY_CHANGE | 缺一 FAIL |
| `guard_meta.state_declared` | 所有类型 | 未声明冻结 |
| `guard_meta.reproducible` | event_type = CONCLUSION | false 则降级为假设 |
| `guard_meta.uncertainty` | event_type = MULTIMODAL | 缺失拒绝放行 |
| `consensus.signatures` | 多智能体协同场景 | 未达成共识不入主链 |

## 5. 与 eel.html v0.2.0 的映射

- 浏览器实现将上述 Schema 收敛为最小字段集（见 `eel.html` 内 `makeBlock()`）；
- 哈希用浏览器原生 `crypto.subtle.digest("SHA-256")`，不支持时降级为内置纯 JS SHA-256 实现（保证 file:// 可跑）；
- 完整字段集由服务端/CLI 验证器（`tools/eel_verify.py`）实现。

## 6. 版本与演进

- v1.0 定稿后字段只增不减，新增字段必须带 `since_version` 标记；
- 链格式升级采用**分叉迁移**（fork-and-migrate）：旧链只读归档，新链从最后一共同块续接，迁移事件本身作为链上事件记录。

---

*配套：eel.html v0.2.0（哈希链版）· tools/eel_verify.py（CLI 验证器）· docs/storage-dual-loop.md（双环存储）*
