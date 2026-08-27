# EEL — 进化证据账本（Evolution Evidence Ledger）

> **一个会改自己的 AI，最危险的不是改错了，而是改错了却没人知道改了啥、为什么改。**
> EEL 给自进化 AI 装一本「不可篡改的进化账本」：每次自我改进（改规则 / 改记忆 / 改策略）都必须记一笔账——何时改、为何改、依据什么。账本只追加、不删除、不修改。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](eel.html)

## 快速开始（1 行命令）

```bash
# 零依赖、零构建：浏览器直接打开即可运行
start eel.html        # Windows
# 或起一个静态服务后访问 http://localhost:8000/eel.html
python -m http.server 8000
```

## 它解决什么问题

[arXiv:2608.18066](https://arxiv.org/abs/2608.18066) 证明：自改进 Agent 的能力是算法 × 任务顺序 × 规格的函数——**换一个任务顺序，能力可能崩盘**。而更可怕的是：当系统改写自己的规则、记忆与策略时，**我们没有任何不可篡改的记录**。

> 恐惧失控是猜测；**没有审计轨迹是事实。**

## 六把锁（G1–G6）

每条护栏 = 一篇论文结论转成的**硬性拒绝**（不是提醒）：

| # | 护栏 | 论文 | 强制规则 |
|---|------|------|---------|
| G1 | 自改进方差闸门 | [2608.18066](https://arxiv.org/abs/2608.18066) | 自改进前后能力差分 **>30% → 拒绝** |
| G2 | 证据保全双环 | [2608.17756](https://arxiv.org/abs/2608.17756) | 记忆编辑必须带**证据指纹**；无指纹 → 拒绝 |
| G3 | 自进化审计账本 | [2608.17684](https://arxiv.org/abs/2608.17684) | 策略变更必须记录**动机 + 数据 + 回测**；缺任一 → 拒绝 |
| G4 | 记忆-策略一致性 | [2608.17247](https://arxiv.org/abs/2608.17247) | 状态转换需一致性校验；未声明状态 → 冻结 |
| G5 | 可复现结论闸门 | [2608.17906](https://arxiv.org/abs/2608.17906) | 结论不可复现 → **降级为「假设」** |
| G6 | 不确定感知闸门 | [2608.17084](https://arxiv.org/abs/2608.17084) | 多模态决策前必须量化不确定性；未量化 → 拒绝 |

## 十个治理引擎（同仓库）

| 引擎 | 主题 | 一句话主张 | 规格 |
|------|------|-----------|------|
| [cognitive-memory](cognitive-memory-engine/) | 记忆 | 记得牢 ≠ 用得对，记忆要喂决策权重 | 40 条 |
| [polarization-depolarization](polarization-depolarization-engine/) | 极化 | 记忆可写+讨论可触发=极化结构 | 12 条 |
| [delegation-asymmetry](delegation-asymmetry-engine/) | 委托 | 风险不在推荐准不准，在边界可否被检查 | 12 条 |
| [versioned-workspace](versioned-workspace-engine/) | 版本化 | 错误不可逆是常态，版本化让错误可逆 | 12 条 |
| [capability-collapse-defense](capability-collapse-defense/) | 塌缩 | 塌缩是结构默认值，不是小概率事故 | 12 条 |
| [preference-consistency](preference-consistency-engine/) | 偏好自洽 | 每条有证据 ≠ 整组不自洽 | 12 条 |
| [verification-protocol](verification-protocol-engine/) | 验证 | 单次成功观测 ≠ 通过检验的估计量 | 12 条 |
| [innovation-metric](innovation-metric-engine/) | 创新度量 | 96.8% 的「新」是重组 | 12 条 |
| [living-benchmark](living-benchmark-engine/) | 活基准 | 结论会过期：真但已过期 = 危险 | 12 条 |
| [preformulation-gap](preformulation-gap-engine/) | 前表述 | 量规评交付物，评不了开场白 | 12 条 |

## 诚实边界（先读再评）

1. **护栏是可执行表达，不是论文复现**——锚点论文的完整方法论比规格复杂得多，部署前须回原文核对。
2. **localStorage 是弱保证**——防误操作，不防有心人篡改；真正的不可篡改需哈希链（v0.2.0 路线图）。
3. **阈值是启发式**（如 30% 方差闸门），未经实证校准。

> 一个审计系统，首先要经得起对自己的审计。这些局限，就是第六条半锁。

## 配套

- 中文导读（费曼学习法助读版）：[docs/中文导读-费曼学习法助读版.md](docs/中文导读-费曼学习法助读版.md)
- 英文版：[README.md](README.md)
- 路线图：哈希链版本 / 接入真实自进化 Agent / i18n / 实证校准

## License

[MIT](LICENSE) © 2026 chenhz01
