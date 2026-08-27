# -*- coding: utf-8 -*-
"""
L2 Baseline Collector: 从正明升级系统历史日志提取对照组基线
=============================================================
提取指标：审计分数 / P0 数 / Token 消耗 / 新模式数 / Skill 更新数 / 已知模式复发数
数据源：D:\\正明升级\\.workbuddy\\memory\\*.md
"""
import os
import re
import json
import glob
from datetime import datetime

MEM_DIR = r"D:\正明升级\.workbuddy\memory"

def read_text(path):
    for enc in ("utf-8", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None

def extract_metrics(text, date):
    m = {}
    m["date"] = date
    # 审计分数：优先"通过(89分)"，其次"条件通过(89分)"，避免误抓"20行"
    m2 = re.search(r"通过[（(]?(\d{2,3})\s*分", text)
    if m2:
        m["audit_score"] = int(m2.group(1))
    else:
        # 趋势行格式：88→88→87→89→89
        trend = re.search(r"(\d{2,3})\s*(?:→|->)\s*\d{2,3}", text)
        if trend:
            m["audit_score"] = int(trend.group(1))
        else:
            # 最后一个 8x 分（排除 20行 之类）
            cands = [int(s) for s in re.findall(r"(\d{2,3})\s*分", text) if 50 <= int(s) <= 100]
            if cands:
                m["audit_score"] = cands[-1]
    # P0 错误
    p0 = re.search(r"P0[=＝]?(\d+)", text)
    m["p0"] = int(p0.group(1)) if p0 else None
    p0b = re.search(r"P0(?:错误|阻断)[=＝]?(\d+)", text)
    if p0b:
        m["p0"] = int(p0b.group(1))
    # Token 消耗
    tok = re.search(r"~?(\d+)\s*K\s*/\s*(\d+)\s*K", text)
    if tok:
        m["token_k"] = int(tok.group(1))
        m["token_budget_k"] = int(tok.group(2))
    tok2 = re.search(r"Token(?:消耗)?[:：]?\s*~?(\d+)K", text)
    if tok2:
        m["token_k"] = int(tok2.group(1))
    # 新模式数（PATT- 数量）
    patt_new = re.findall(r"PATT-\d{8}-\d+", text)
    # 模式数：以"3个新模式"等描述
    newm = re.search(r"(\d+)\s*个新模式", text)
    m["new_patterns"] = int(newm.group(1)) if newm else None
    if m.get("new_patterns") is None and patt_new:
        # 按日期过滤当天新模式
        day_patts = [p for p in patt_new if date.replace("-", "") in p]
        m["new_patterns"] = len(day_patts) if day_patts else None
    # Skill 更新数：多种格式
    su = re.search(r"Skill更新[^：:]*[:：]?\s*(\d+)\s*处", text)
    m["skill_updates"] = int(su.group(1)) if su else None
    if m.get("skill_updates") is None:
        su2 = re.search(r"(\d+)\s*处Skill更新", text)
        if su2:
            m["skill_updates"] = int(su2.group(1))
    if m.get("skill_updates") is None:
        su3 = re.search(r"Skill更新[^：:]*[:：]\s*(\d+)", text)
        if su3:
            m["skill_updates"] = int(su3.group(1))
    # 已知模式复发
    rec = re.search(r"已知\s*(\d+)个模式.*?(\d+)个(?:零)?复发", text)
    if rec:
        m["known_patterns"] = int(rec.group(1))
        m["recurrences"] = int(rec.group(2))
    rec2 = re.search(r"(\d+)个中(\d+)个零复发", text)
    if rec2:
        m["known_patterns"] = int(rec2.group(1))
        m["recurrences"] = int(rec2.group(1)) - int(rec2.group(2))
    # 状态
    m["success"] = "✅" in text or "完整闭环" in text or "成功" in text
    return m

def main():
    files = sorted(glob.glob(os.path.join(MEM_DIR, "2026-*.md")))
    rows = []
    for f in files:
        base = os.path.basename(f)
        date = base[:10]
        text = read_text(f)
        if not text:
            print(f"SKIP {base}: cannot decode")
            continue
        m = extract_metrics(text, date)
        rows.append(m)
        print(f"{date}: 分数={m.get('audit_score')} P0={m.get('p0')} "
              f"Token={m.get('token_k')}K 新模式={m.get('new_patterns')} "
              f"Skill更新={m.get('skill_updates')} 复发={m.get('recurrences')} "
              f"成功={m.get('success')}")

    # 汇总统计
    scores = [r["audit_score"] for r in rows if r.get("audit_score")]
    p0s = [r["p0"] for r in rows if r.get("p0") is not None]
    tokens = [r["token_k"] for r in rows if r.get("token_k")]
    newps = [r["new_patterns"] for r in rows if r.get("new_patterns") is not None]
    print("\n=== 对照组基线汇总（无 EEL 审计时期）===")
    if scores:
        print(f"  审计分数: n={len(scores)}, 均值={sum(scores)/len(scores):.1f}, 范围={min(scores)}-{max(scores)}")
    if p0s:
        print(f"  P0 错误: n={len(p0s)}, 全为0={all(p==0 for p in p0s)}")
    if tokens:
        print(f"  Token消耗: n={len(tokens)}, 均值={sum(tokens)/len(tokens):.0f}K, 趋势={tokens}")
    if newps:
        print(f"  新模式: n={len(newps)}, 均值={sum(newps)/len(newps):.1f}/天")
    print(f"  有效样本天数: {len(rows)}")
    print(f"  数据日期范围: {rows[0]['date']} ~ {rows[-1]['date']}")

    with open(r"D:\正明升级\.workbuddy\memory\_l2_baseline.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print("\n已保存: _l2_baseline.json")

if __name__ == "__main__":
    main()
