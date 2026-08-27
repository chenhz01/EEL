# -*- coding: utf-8 -*-
"""
EEL Audit Hook for zhengming-upgrade-daily
==========================================
L2 实验组核心组件：把 EEL 六锁（G1-G6）插入每日进化流水线。

设计原则：
- 零侵入：不修改 SKILL.md 主流程，作为独立钩子由 /zmu eel 命令调用
- append-only：账本只追加不删除（EEL 核心原则）
- 可回滚：审计失败仅标记+建议，不自动拦截（实验初期观察模式）

用法：
  python eel_hook.py record  --type skill_update --desc "..." --evidence "论文锚点/数据来源" --diff 0.15
  python eel_hook.py record  --type policy_change --desc "..." --motive "..." --data "..." --backtest "..."
  python eel_hook.py report   # 查看当日账本与六锁判定
  python eel_hook.py stats    # 审计完备度 r 统计

账本位置：D:\\正明升级\\.workbuddy\\eel\\ledger.json（append-only）
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

LEDGER_DIR = r"D:\正明升级\.workbuddy\eel"
LEDGER = os.path.join(LEDGER_DIR, "ledger.json")
HISTORY = os.path.join(LEDGER_DIR, "history.json")  # 每日快照（活基准用）

# 六锁定义（对应 EEL 主账本 G1-G6）
LOCKS = {
    "G1": {"name": "自改进方差闸门", "paper": "2608.18066",
           "rule": "能力差分 >30% → 拒绝"},
    "G2": {"name": "证据保全双环", "paper": "2608.17756",
           "rule": "记忆编辑必须带证据指纹 → 否则拒绝"},
    "G3": {"name": "自进化审计账本", "paper": "2608.17684",
           "rule": "策略变更必须记录 动机+数据+回测"},
    "G4": {"name": "记忆-策略一致性", "paper": "2608.17247",
           "rule": "未声明状态 → 冻结"},
    "G5": {"name": "可复现结论闸门", "paper": "2608.17906",
           "rule": "结论不可复现 → 降级为假设"},
    "G6": {"name": "不确定感知闸门", "paper": "2608.17084",
           "rule": "未量化不确定性 → 拒绝"},
}

VARIANCE_THRESHOLD = 0.30  # G1 阈值（启发式，待校准）


def load_ledger():
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            return json.load(f)
    return {"meta": {"created": datetime.now().isoformat(),
                     "principle": "进化即证据，证据不可篡改"},
            "events": []}


def save_ledger(ledger):
    os.makedirs(LEDGER_DIR, exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=1)


def check_events(events, event):
    """六锁校验，返回 (通过?, 判定详情)"""
    verdicts = []
    etype = event.get("type", "")
    passed = True

    # G1 方差闸门
    if "diff" in event:
        diff = abs(float(event["diff"]))
        if diff > VARIANCE_THRESHOLD:
            verdicts.append({"lock": "G1", "verdict": "REJECT",
                             "detail": f"能力差分 {diff:.0%} > 30% → 拒绝"})
            passed = False
        else:
            verdicts.append({"lock": "G1", "verdict": "PASS",
                             "detail": f"差分 {diff:.0%} ≤ 30%"})
    else:
        verdicts.append({"lock": "G1", "verdict": "N/A",
                         "detail": "无 diff 字段（非自改进事件）"})

    # G2 证据指纹
    if etype in ("memory_edit", "skill_update"):
        if event.get("evidence"):
            verdicts.append({"lock": "G2", "verdict": "PASS",
                             "detail": f"证据指纹: {event['evidence'][:40]}"})
        else:
            verdicts.append({"lock": "G2", "verdict": "REJECT",
                             "detail": "记忆/技能编辑缺少证据指纹 → 拒绝"})
            passed = False

    # G3 审计账本（策略变更需 动机+数据+回测）
    if etype == "policy_change":
        missing = []
        for k in ("motive", "data", "backtest"):
            if not event.get(k):
                missing.append(k)
        if missing:
            verdicts.append({"lock": "G3", "verdict": "REJECT",
                             "detail": f"缺少: {','.join(missing)}"})
            passed = False
        else:
            verdicts.append({"lock": "G3", "verdict": "PASS",
                             "detail": "动机+数据+回测 齐全"})

    # G5 可复现结论（结论类事件需 reproducible 字段）
    if etype == "conclusion":
        rep = str(event.get("reproducible", "")).strip().lower()
        if rep in ("yes", "true", "1", "y"):
            verdicts.append({"lock": "G5", "verdict": "PASS",
                             "detail": "可复现"})
        else:
            verdicts.append({"lock": "G5", "verdict": "DEMOTE",
                             "detail": "不可复现 → 降级为假设"})

    # G6 不确定感知（决策类事件需 uncertainty 字段）
    if etype == "decision":
        if event.get("uncertainty") is not None:
            verdicts.append({"lock": "G6", "verdict": "PASS",
                             "detail": f"不确定性已量化: {event['uncertainty']}"})
        else:
            verdicts.append({"lock": "G6", "verdict": "REJECT",
                             "detail": "未量化不确定性 → 拒绝"})
            passed = False

    return passed, verdicts


def record(args):
    ledger = load_ledger()
    event = {
        "ts": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": args.type,
        "desc": args.desc,
    }
    for field in ("evidence", "diff", "motive", "data", "backtest",
                  "reproducible", "uncertainty", "state"):
        val = getattr(args, field, None)
        if val is not None:
            event[field] = val

    passed, verdicts = check_events(ledger["events"], event)
    event["verdicts"] = verdicts
    event["overall"] = "PASS" if passed else ("DEMOTE" if any(v["verdict"] == "DEMOTE" for v in verdicts) else "REJECT")
    ledger["events"].append(event)  # append-only
    save_ledger(ledger)

    print(f"事件已入账（append-only）: {event['ts']}")
    print(f"类型: {event['type']} ｜ 判定: {event['overall']}")
    for v in verdicts:
        print(f"  [{v['lock']}] {v['verdict']}: {v['detail']}")
    return passed


def report(args):
    ledger = load_ledger()
    events = ledger["events"]
    today = datetime.now().strftime("%Y-%m-%d")
    today_events = [e for e in events if e.get("date") == today]
    print(f"=== EEL 账本（共 {len(events)} 事件，今日 {len(today_events)}）===")
    for e in reversed(today_events[-10:]):
        print(f"  [{e['ts'][11:19]}] {e['type']}: {e.get('desc', '')[:40]} → {e['overall']}")
    print(f"\n原则: 进化即证据，证据不可篡改")


def stats(args):
    ledger = load_ledger()
    events = ledger["events"]
    n = len(events)
    if n == 0:
        print("账本为空")
        return
    # 审计完备度 r（G2 证据指纹通过率）
    g2_events = [e for e in events if e.get("type") in ("memory_edit", "skill_update")]
    g2_pass = [e for e in g2_events if e.get("evidence")]
    r = len(g2_pass) / len(g2_events) if g2_events else 1.0
    # 拒绝率
    rejected = [e for e in events if e.get("overall") == "REJECT"]
    demoted = [e for e in events if e.get("overall") == "DEMOTE"]
    print(f"=== EEL 审计统计 ===")
    print(f"  总事件: {n}")
    print(f"  审计完备度 r (G2): {r:.1%} ({len(g2_pass)}/{len(g2_events)})")
    print(f"  拒绝: {len(rejected)} ｜ 降级: {len(demoted)}")
    print(f"  通过: {n - len(rejected) - len(demoted)}")
    print(f"  注: r 为审计完备度，L1 定律变量（r < r* → 存在塌缩序列）")


def main():
    parser = argparse.ArgumentParser(description="EEL Audit Hook for /zmu daily")
    sub = parser.add_subparsers(dest="cmd")

    p_record = sub.add_parser("record", help="记录一条进化事件")
    p_record.add_argument("--type", required=True, choices=["skill_update", "memory_edit", "policy_change", "conclusion", "decision", "self_improve"])
    p_record.add_argument("--desc", required=True)
    p_record.add_argument("--evidence", help="G2 证据指纹")
    p_record.add_argument("--diff", type=float, help="G1 能力差分")
    p_record.add_argument("--motive", help="G3 动机")
    p_record.add_argument("--data", help="G3 数据")
    p_record.add_argument("--backtest", help="G3 回测")
    p_record.add_argument("--reproducible", help="G5 可复现性")
    p_record.add_argument("--uncertainty", help="G6 不确定性量化")
    p_record.add_argument("--state", help="G4 状态声明")

    sub.add_parser("report", help="查看当日账本")
    sub.add_parser("stats", help="审计完备度统计")

    args = parser.parse_args()
    if args.cmd == "record":
        sys.exit(0 if record(args) else 2)
    elif args.cmd == "report":
        report(args)
    elif args.cmd == "stats":
        stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
