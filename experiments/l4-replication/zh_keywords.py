# -*- coding: utf-8 -*-
"""
L4 v0.2.1: 中英文混合匹配
- tokenize 增加中文 bigram 切分（解决长句 vs 关键词鸿沟）
- 已知空间增加中文关键词
"""
import re

def tokenize_mix(text):
    """中英文混合分词：英文单词 + 中文 bigram"""
    text = text.lower()
    tokens = set()
    # 英文/数字
    for w in re.findall(r"[a-z0-9][a-z0-9\-_]{1,}", text):
        tokens.add(w)
    # 中文：去除标点和英文后做 bigram
    zh = re.sub(r"[a-z0-9\s\-_（）()\[\]{}《》【】\"'，。；：！？、/\\|·—–]+", "", text)
    if zh:
        for i in range(len(zh) - 1):
            bigram = zh[i:i+2]
            if bigram.strip():
                tokens.add(bigram)
    return tokens

# 已知空间中文关键词扩展（每范式补 zh 关键词集）
KNOWN_SPACE_ZH = [
    {"name": "Spaced Repetition (SRS)", "zh": ["间隔重复", "复习", "遗忘曲线", "调度复习", "到期复习"]},
    {"name": "Memory Bank / Episodic Memory", "zh": ["记忆库", "经验存储", "案例检索", "写入存储"]},
    {"name": "Working Memory / Context Mgmt", "zh": ["上下文", "窗口管理", "压缩", "裁剪"]},
    {"name": "Knowledge Graph Memory", "zh": ["知识图谱", "实体关系", "图谱查询"]},
    {"name": "Semantic Cache", "zh": ["缓存", "语义相似", "命中复用"]},
    {"name": "Plan-Execute", "zh": ["计划", "规划", "任务分解", "子任务"]},
    {"name": "Hierarchical Task Decomposition", "zh": ["分层", "分解", "任务树", "递归"]},
    {"name": "Replanning / Dynamic Plan", "zh": ["重计划", "偏差", "动态调整"]},
    {"name": "Chain-of-Thought (CoT)", "zh": ["思维链", "逐步推理", "中间步骤", "推理分解"]},
    {"name": "Tree-of-Thought (ToT)", "zh": ["思维树", "分支搜索", "回溯", "剪枝"]},
    {"name": "Graph-of-Thought (GoT)", "zh": ["思维图", "聚合", "多路径"]},
    {"name": "Self-Consistency Sampling", "zh": ["多次采样", "投票", "多数", "一致性"]},
    {"name": "Least-to-Most Prompting", "zh": ["由易到难", "子问题", "渐进"]},
    {"name": "Program-aided Language (PAL)", "zh": ["代码生成", "程序执行", "计算"]},
    {"name": "RAG (Retrieval-Augmented)", "zh": ["检索增强", "向量检索", "召回", "topk"]},
    {"name": "HyDE", "zh": ["假设文档", "查询扩展"]},
    {"name": "BM25 / Lexical Retrieval", "zh": ["词法检索", "倒排", "词频"]},
    {"name": "Reranking", "zh": ["重排", "精排", "相关性"]},
    {"name": "Query Decomposition", "zh": ["查询分解", "多跳", "子查询"]},
    {"name": "Reflection / Self-Critique", "zh": ["反思", "自评", "批评", "自我改进"]},
    {"name": "Self-Refine", "zh": ["精炼", "迭代改进", "反馈修改"]},
    {"name": "Constitutional AI", "zh": ["宪法", "原则", "规则批评"]},
    {"name": "Expert Iteration / Self-play", "zh": ["自对弈", "专家迭代", "自我博弈"]},
    {"name": "Evolver (Evolutionary)", "zh": ["进化", "遗传", "变异", "选择"]},
    {"name": "RLHF / Reward Model", "zh": ["奖励模型", "人类反馈", "对齐"]},
    {"name": "DPO", "zh": ["直接偏好", "隐式奖励"]},
    {"name": "GRPO", "zh": ["组相对", "组内归一化"]},
    {"name": "RLVR", "zh": ["可验证奖励", "规则奖励"]},
    {"name": "Reward Shaping", "zh": ["奖励塑形", "中间奖励"]},
    {"name": "Curriculum Learning", "zh": ["课程", "由易到难", "难度排序"]},
    {"name": "Distillation", "zh": ["蒸馏", "教师学生", "软标签"]},
    {"name": "Version Control (git-like)", "zh": ["版本", "提交", "回滚", "暂存", "快照", "分支"]},
    {"name": "Audit Log / Ledger", "zh": ["审计", "日志", "留痕", "追溯", "账本"]},
    {"name": "Circuit Breaker", "zh": ["熔断", "隔离", "降级"]},
    {"name": "Retry with Backoff", "zh": ["重试", "退避"]},
    {"name": "Rate Limiting", "zh": ["限流", "配额", "令牌"]},
    {"name": "Message Queue / Event Bus", "zh": ["消息队列", "事件总线", "异步"]},
    {"name": "Publish-Subscribe", "zh": ["发布订阅", "主题"]},
    {"name": "MapReduce", "zh": ["映射", "归约", "并行"]},
    {"name": "Contract / SLA Framework", "zh": ["契约", "委托", "授权", "边界", "责任"]},
    {"name": "Four-Eyes / Maker-Checker", "zh": ["复核", "制衡", "分离", "检查"]},
    {"name": "RBAC / Permission Model", "zh": ["权限", "角色", "访问控制"]},
    {"name": "Compliance Checklist", "zh": ["合规", "检查清单"]},
    {"name": "Immutable Ledger / Hash Chain", "zh": ["哈希链", "不可篡改", "防篡改"]},
    {"name": "Approval Workflow", "zh": ["审批", "流程", "会签"]},
    {"name": "Statistical Hypothesis Testing", "zh": ["统计检验", "显著性", "置信", "样本量"]},
    {"name": "A/B Testing / Controlled Experiment", "zh": ["对照", "控制组", "随机化", "实验"]},
    {"name": "Noise Floor Measurement", "zh": ["噪声地板", "波动", "方差"]},
    {"name": "Bootstrap / Resampling", "zh": ["自助法", "重采样"]},
    {"name": "Anomaly Detection", "zh": ["异常检测", "离群", "告警"]},
    {"name": "Control Charts (SPC)", "zh": ["控制图", "过程控制"]},
    {"name": "Time-Series Monitoring", "zh": ["监控", "滚动", "复测", "基准"]},
    {"name": "Content Filtering", "zh": ["内容过滤", "审核", "拦截"]},
    {"name": "Sandboxing / Isolation", "zh": ["沙箱", "隔离执行"]},
    {"name": "Input Validation", "zh": ["输入验证", "清洗", "白名单"]},
    {"name": "Multi-Agent Debate", "zh": ["辩论", "多方", "共识"]},
    {"name": "Role-based Team (Crew)", "zh": ["角色", "团队", "分工"]},
    {"name": "Blackboard Architecture", "zh": ["黑板", "共享"]},
    {"name": "Agent Voting / Committee", "zh": ["委员会", "投票"]},
    {"name": "Orchestrator-Workers", "zh": ["编排", "工人"]},
    {"name": "Conversational Agent", "zh": ["对话", "轮次", "消息"]},
    {"name": "Clarification-First", "zh": ["澄清", "提问", "需求"]},
    {"name": "Structured Handoff", "zh": ["交接", "摘要", "移交"]},
    {"name": "Rule-based Guardrails", "zh": ["规则", "校验", "闸门", "拒绝"]},
]
