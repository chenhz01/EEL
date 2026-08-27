# -*- coding: utf-8 -*-
"""
L4 Replication Tool: Design-Space Mapping
==========================================
复现 arXiv:2608.17471 核心方法（简化版）：
  1. 四模块拆解：触发条件 / 处理流程 / 输出格式 / 依赖组件
  2. 已知算法设计空间（人类已有方法库）
  3. 模块级重合度计算 → 复用/重组/新组合 三选一
  4. 统计：空间内占比 / 精确复刻占比 / 新组合占比

用法：
  python l4_tool.py --data data/designs.json
  或 import 本模块作为库
"""
import json
import os
import sys
from collections import Counter

# 尝试加载扩展版已知空间（v0.2），失败则用内置基础版
try:
    from known_space_extended import KNOWN_SPACE_EXTENDED
    KNOWN_SPACE = KNOWN_SPACE_EXTENDED
    print(f"[l4_tool] 使用扩展已知空间: {len(KNOWN_SPACE)} 个范式")
except ImportError:
    print("[l4_tool] 扩展空间未找到，使用内置基础空间")

# ---------- 已知算法设计空间（人类已有方法，L4 参照系） ----------
# 每项: {name, trigger, flow, output, deps} 关键词集合
KNOWN_SPACE = [
    {"name": "Spaced Repetition (SRS)", "trigger": ["遗忘", "复习", "调度", "到期"],
     "flow": ["间隔", "调度", "复习", "遗忘曲线", "retrievability"],
     "output": ["复习计划", "调度", "提醒"],
     "deps": ["记忆库", "时间戳"]},
    {"name": "RAG (Retrieval-Augmented)", "trigger": ["检索", "查询", "召回"],
     "flow": ["嵌入", "向量", "检索", "召回", "排序", "top-k"],
     "output": ["文档", "上下文", "片段"],
     "deps": ["向量库", "embedding", "索引"]},
    {"name": "ReAct (Reason+Act)", "trigger": ["工具调用", "推理", "行动"],
     "flow": ["思考", "推理", "行动", "观察", "循环", "tool"],
     "output": ["动作", "工具结果", "推理链"],
     "deps": ["工具", "LLM"]},
    {"name": "Chain-of-Thought (CoT)", "trigger": ["推理", "复杂", "逐步"],
     "flow": ["逐步", "推理", "思考链", "中间步骤", "分解"],
     "output": ["推理链", "中间结论"],
     "deps": ["LLM"]},
    {"name": "Tree-of-Thought (ToT)", "trigger": ["探索", "分支", "搜索"],
     "flow": ["分支", "搜索", "评估", "回溯", "树", "广度", "深度"],
     "output": ["多条路径", "最优路径"],
     "deps": ["LLM", "评估器"]},
    {"name": "Reflection / Self-Critique", "trigger": ["自我", "批评", "反思", "改进"],
     "flow": ["生成", "批评", "反思", "修改", "迭代", "自评"],
     "output": ["修订版", "批评意见"],
     "deps": ["LLM"]},
    {"name": "Plan-Execute", "trigger": ["计划", "规划", "任务分解"],
     "flow": ["计划", "分解", "执行", "验证", "子任务"],
     "output": ["计划", "执行结果"],
     "deps": ["任务管理器"]},
    {"name": "Ensemble / Voting", "trigger": ["投票", "集成", "多数"],
     "flow": ["多个", "采样", "投票", "汇总", "多数"],
     "output": ["多数结论", "聚合结果"],
     "deps": ["LLM", "聚合器"]},
    {"name": "Memory Bank / Episodic Memory", "trigger": ["记忆", "存储", "检索", "经验"],
     "flow": ["写入", "存储", "检索", "经验", "案例"],
     "output": ["记忆条目", "检索结果"],
     "deps": ["记忆库", "索引"]},
    {"name": "Chain-of-Verification (CoVe)", "trigger": ["验证", "事实", "核对"],
     "flow": ["验证", "核对", "事实检查", "修正"],
     "output": ["验证报告", "修正版"],
     "deps": ["LLM", "验证器"]},
    {"name": "RLHF / Reward Model", "trigger": ["奖励", "偏好", "对齐"],
     "flow": ["奖励", "偏好", "训练", "对齐", "feedback"],
     "output": ["策略", "奖励模型"],
     "deps": ["训练框架", "人类反馈"]},
    {"name": "Audit Log / Ledger", "trigger": ["审计", "日志", "留痕", "追溯"],
     "flow": ["记录", "追加", "append", "审计", "追溯"],
     "output": ["日志", "账本", "审计记录"],
     "deps": ["存储", "时间戳"]},
    {"name": "Version Control (git-like)", "trigger": ["版本", "提交", "回滚", "暂存"],
     "flow": ["暂存", "提交", "回滚", "分叉", "快照", "diff"],
     "output": ["版本", "快照", "diff"],
     "deps": ["存储", "哈希"]},
    {"name": "Rule-based Guardrails", "trigger": ["规则", "校验", "闸门", "拒绝"],
     "flow": ["规则", "校验", "拒绝", "放行", "条件"],
     "output": ["判定", "拒绝/放行"],
     "deps": ["规则引擎"]},
    {"name": "Statistical Hypothesis Testing", "trigger": ["统计", "检验", "显著性", "置信"],
     "flow": ["样本", "统计", "检验", "置信", "显著性", "噪声"],
     "output": ["p值", "置信区间", "结论"],
     "deps": ["统计库", "数据"]},
    {"name": "A/B Testing / Controlled Experiment", "trigger": ["对照", "实验", "分组", "A/B"],
     "flow": ["对照", "分组", "实验", "控制组", "对比"],
     "output": ["对比结果", "效应量"],
     "deps": ["实验框架", "数据"]},
    {"name": "Time-Series Monitoring / Benchmark", "trigger": ["监控", "滚动", "基准", "复测"],
     "flow": ["滚动", "监控", "复测", "基准", "时序"],
     "output": ["监控指标", "基准分数"],
     "deps": ["数据源", "评估器"]},
    {"name": "Contract / SLA Framework", "trigger": ["契约", "委托", "授权", "边界"],
     "flow": ["契约", "边界", "委托", "审计", "责任"],
     "output": ["契约", "授权记录"],
     "deps": ["文档", "审计"]},
    {"name": "Fault Detection / Circuit Breaker", "trigger": ["故障", "熔断", "异常", "检测"],
     "flow": ["检测", "熔断", "隔离", "恢复", "告警"],
     "output": ["告警", "隔离状态"],
     "deps": ["监控", "阈值"]},
    {"name": "Content Filtering", "trigger": ["过滤", "内容", "审核"],
     "flow": ["过滤", "审核", "拦截", "标记"],
     "output": ["放行/拦截"],
     "deps": ["分类器"]},
]


def tokenize(text):
    """分词：小写 + 简单切分"""
    text = text.lower()
    for ch in "，。；：！？、（）()[]{}《》【】\"'|/\\-—–·":
        text = text.replace(ch, " ")
    return set(text.split())


def tokenize_mix(text):
    """中英文混合分词：英文单词 + 中文 bigram（解决长句 vs 关键词鸿沟）"""
    import re
    text = text.lower()
    tokens = set()
    for w in re.findall(r"[a-z0-9][a-z0-9\-_]{1,}", text):
        tokens.add(w)
    zh = re.sub(r"[a-z0-9\s\-_（）()\[\]{}《》【】\"'，。；：！？、/\\|·—–]+", "", text)
    if zh:
        for i in range(len(zh) - 1):
            bg = zh[i:i+2]
            if bg.strip():
                tokens.add(bg)
    return tokens


def similarity(s1, s2):
    """Jaccard 相似度"""
    if not s1 or not s2:
        return 0.0
    inter = len(s1 & s2)
    union = len(s1 | s2)
    return inter / union if union else 0.0


def get_known_space():
    """已知空间（扩展版 + 中文关键词）"""
    space = []
    try:
        from known_space_extended import KNOWN_SPACE_EXTENDED
        space = [dict(k) for k in KNOWN_SPACE_EXTENDED]
    except ImportError:
        space = [dict(k) for k in KNOWN_SPACE]
    try:
        from zh_keywords import KNOWN_SPACE_ZH
        zh_map = {k["name"]: k["zh"] for k in KNOWN_SPACE_ZH}
        for item in space:
            zh = zh_map.get(item["name"], [])
            item["zh_keywords"] = zh
    except ImportError:
        pass
    return space


def classify(design, verbose=False):
    """
    对单个设计做四模块拆解 + 与已知空间比对（中英混合）。
    返回 (类型, 最佳匹配, 各模块得分)
    """
    trig = tokenize_mix(design["trigger"])
    flow = tokenize_mix(design["flow"])
    out = tokenize_mix(design["output"])
    deps = tokenize_mix(design["deps"])

    space = get_known_space()
    best = None
    best_score = 0.0
    module_scores = {}
    for known in space:
        zh = " ".join(known.get("zh_keywords", []))
        # v0.2.1 配置（C 组阳性对照最优）：zh 仅补充 trigger 模块，避免稀释英文流程匹配
        kt = tokenize_mix(" ".join(known.get("trigger", [])) + " " + zh)
        kf = tokenize_mix(" ".join(known.get("flow", [])))
        ko = tokenize_mix(" ".join(known.get("output", [])))
        kd = tokenize_mix(" ".join(known.get("deps", [])))
        s_t, s_f, s_o, s_d = similarity(trig, kt), similarity(flow, kf), similarity(out, ko), similarity(deps, kd)
        total = 0.4 * s_f + 0.25 * s_t + 0.2 * s_o + 0.15 * s_d
        if total > best_score:
            best_score = total
            best = known["name"]
            module_scores = {"trigger": round(s_t, 3), "flow": round(s_f, 3), "output": round(s_o, 3), "deps": round(s_d, 3)}

    # 判定（对齐 innv-003/innv-005）；v0.2.1 阈值校准：多范式空间下降低基准
    if best_score >= 0.45:
        kind = "精确复刻"
    elif best_score >= 0.22:
        kind = "重组"
    else:
        kind = "新组合"
    return kind, best, round(best_score, 3), module_scores


def analyze(data, verbose=True):
    results = []
    for d in data:
        kind, match, score, mods = classify(d)
        match_disp = match if match else "(无匹配)"
        results.append({"name": d["name"], "kind": kind, "best_match": match_disp,
                        "score": score, "modules": mods})
        if verbose:
            print(f"  {d['name'][:36]:38s} → {kind:5s} (match: {match_disp[:28]:30s} score={score})")
    cnt = Counter(r["kind"] for r in results)
    n = len(results)
    print(f"\n=== 统计（n={n}）===")
    for k in ["精确复刻", "重组", "新组合"]:
        c = cnt.get(k, 0)
        print(f"  {k}: {c} ({c/n*100:.1f}%)" if n else f"  {k}: 0")
    # 空间内占比 = 精确复刻 + 重组（落在人类设计空间内）
    in_space = cnt.get("精确复刻", 0) + cnt.get("重组", 0)
    if n:
        print(f"\n  落在人类设计空间内: {in_space}/{n} = {in_space/n*100:.1f}%  (论文声称 ≈96.8%)")
        print(f"  新组合(潜在跳出): {cnt.get('新组合', 0)}/{n} = {cnt.get('新组合', 0)/n*100:.1f}%")
    return results, cnt


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/designs.json"
    with open(data_path, encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, dict) and "designs" in raw:
        data = raw["designs"]
    else:
        data = raw
    print(f"=== 设计空间映射分析：{os.path.basename(data_path)}（n={len(data)}）===")
    results, _ = analyze(data)
    out_path = data_path.replace(".json", "_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"\n结果已保存: {out_path}")
