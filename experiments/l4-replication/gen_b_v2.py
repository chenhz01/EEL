# -*- coding: utf-8 -*-
"""
L4 v0.2: 从 EEL 仓库各引擎 specs.json 生成 B 组数据（原文驱动，消除术语偏差）
输出：data/designs_b_eel_v2.json
"""
import json
import os
import glob

EEL = r"C:\Users\Administrator\Desktop\成果\EEL"
OUT = os.path.join(EEL, "experiments", "l4-replication", "data", "designs_b_eel_v2.json")

engines = [
    ("cognitive-memory-engine", "cognitive-memory-engine (间隔重复×决策耦合)"),
    ("polarization-depolarization-engine", "polarization-depolarization-engine (群体极化防御)"),
    ("delegation-asymmetry-engine", "delegation-asymmetry-engine (委托责任契约)"),
    ("versioned-workspace-engine", "versioned-workspace-engine (版本化工作区)"),
    ("capability-collapse-defense", "capability-collapse-defense (能力塌缩防线)"),
    ("preference-consistency-engine", "preference-consistency-engine (偏好自洽闸门)"),
    ("verification-protocol-engine", "verification-protocol-engine (验证协议引擎)"),
    ("innovation-metric-engine", "innovation-metric-engine (创新度量引擎)"),
    ("living-benchmark-engine", "living-benchmark-engine (活基准引擎)"),
    ("preformulation-gap-engine", "preformulation-gap-engine (前表述缺口引擎)"),
]

designs = []
for folder, disp_name in engines:
    specs_path = os.path.join(EEL, folder, "specs.json")
    if not os.path.exists(specs_path):
        print(f"SKIP {folder}: no specs.json")
        continue
    with open(specs_path, encoding="utf-8") as f:
        data = json.load(f)
    specs = data.get("specs", [])
    # 汇总 problem 与 solution 原文
    problems = " ".join(s.get("problem", "") for s in specs)
    solutions = " ".join(s.get("solution", "") for s in specs)
    triggers = " ".join(s.get("problem", "")[:100] for s in specs[:6])
    design = {
        "name": disp_name,
        "trigger": problems[:400],
        "flow": solutions[:600],
        "output": " ".join(s.get("name", "") for s in specs)[:200],
        "deps": " ".join(s.get("integration", "") for s in specs)[:200],
    }
    designs.append(design)
    print(f"  {disp_name[:40]}: {len(specs)} specs, prob={len(problems)}ch")

payload = {
    "meta": {
        "dataset": "B组v0.2: EEL 仓库 specs.json 原文驱动（problem/solution 原文）",
        "source": "EEL 仓库各引擎 specs.json",
        "date": "2026-08-24",
        "note": "消除人工描述术语偏差，用规格原文"
    },
    "designs": designs,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print(f"\n已生成: {OUT} ({len(designs)} 引擎)")
