# -*- coding: utf-8 -*-
"""
L4 v0.3: 自动结果 vs 黄金标准对比
- 自动：designs_b_eel_v2_result.json（v0.2.1 配置）
- 黄金：gold_standard_b.json（人工标注）
"""
import json
import os

BASE = r"C:\Users\Administrator\Desktop\成果\EEL\experiments\l4-replication\data"
AUTO = os.path.join(BASE, "designs_b_eel_v2_result.json")
GOLD = os.path.join(BASE, "gold_standard_b.json")

with open(AUTO, encoding="utf-8") as f:
    auto = json.load(f)
with open(GOLD, encoding="utf-8") as f:
    gold = json.load(f)

gold_map = {}
for a in gold["annotations"]:
    gold_map[a["id"]] = a

# 匹配：按名称近似
name_map = {
    "cognitive-memory-engine (间隔重复×决策耦合)": "cognitive-memory-engine",
    "polarization-depolarization-engine (": "polarization-depolarization-engine",
    "delegation-asymmetry-engine (委托责任契约)": "delegation-asymmetry-engine",
    "versioned-workspace-engine (版本化工作区)": "versioned-workspace-engine",
    "capability-collapse-defense (能力塌缩防线)": "capability-collapse-defense",
    "preference-consistency-engine (偏好自洽闸": "preference-consistency-engine",
    "verification-protocol-engine (验证协议引擎)": "verification-protocol-engine",
    "innovation-metric-engine (创新度量引擎)": "innovation-metric-engine",
    "living-benchmark-engine (活基准引擎)": "living-benchmark-engine",
    "preformulation-gap-engine (前表述缺口引擎)": "preformulation-gap-engine",
}

print("=== 自动 vs 黄金标准对比 ===")
print(f"{'引擎':<30} {'自动':<6} {'黄金':<6} {'一致'}")
agree = 0
total = 0
for a in auto:
    aid = name_map.get(a["name"])
    if not aid or aid not in gold_map:
        continue
    g = gold_map[aid]
    same = "✅" if a["kind"] == g["kind"] else "❌"
    if a["kind"] == g["kind"]:
        agree += 1
    total += 1
    print(f"{g['name'][:28]:<30} {a['kind']:<6} {g['kind']:<6} {same}")
    if a["kind"] != g["kind"]:
        print(f"   自动分={a['score']} 黄金理由={g['rationale'][:60]}...")

print(f"\n自动 vs 黄金一致率: {agree}/{total} = {agree/total*100:.0f}%")

# 黄金标准分布
from collections import Counter
kinds = Counter(a["kind"] for a in gold["annotations"])
print(f"\n黄金标准分布: {dict(kinds)}")
print(f"黄金新组合率: {kinds['新组合']}/{len(gold['annotations'])} = {kinds['新组合']/len(gold['annotations'])*100:.0f}%")
print(f"论文基准（AI生成设计）: 3.2%")
