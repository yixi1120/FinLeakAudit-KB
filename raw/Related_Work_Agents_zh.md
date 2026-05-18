# 相关工作：金融与时间序列中的多智能体 / Agentic RAG（2024–2026）

**生成日期：** 2026-05-14  
**来源：** arXiv（Agent + RAG + Finance/Trading/TS 组合检索）  
**相关论文数：** 25

---

## 论文总览（核心集成机制）

| # | 论文 | 年份 | 核心机制（中文） |
|---|---|---:|---|
| 1 | Integrating Traditional Technical Analysis with AI | 2025 | 多智能体 + RAG，将艾略特波浪理论与 AI 结合做股市预测 |
| 2 | The New Quant | 2025 | Agentic 工作流 + RAG + 情绪分析 + 多模态融合 + 工具调用 |
| 3 | Enhancing Financial RAG with Agentic AI and Multi-HyDE | 2025 | Agentic RAG + Multi-HyDE，多视角检索，降低幻觉并提准 |
| 4 | A Role-Aware Multi-Agent Framework for Financial Education QA | 2025 | 角色分工多智能体 + RAG + 微调骨干 |
| 5 | Rethinking Retrieval... in Financial Domain | 2025 | 系统比较向量检索与非向量结构检索 |
| 6 | Agentic RAG for Time Series Analysis | 2024 | 分层多智能体编排 + RAG + 小模型任务化微调 |
| 7 | Agentic AI... Institutional Turn | 2026 | 讨论 Agentic AI 与 RAG 在法律与金融治理中的制度化框架 |
| 8 | AI for Climate Finance | 2025 | Agentic 检索 + 多步推理 + 微调，用于气候金融资金追踪 |
| 9 | Adaptive Query Routing | 2026 | 分层路由的混合检索（金融/法律/医疗） |
| 10 | MarketSenseAI 2.0 | 2025 | 多智能体 + RAG 融合财报、财报电话会和宏观报告 |
| 11 | Graph RAG-Tool Fusion | 2025 | 图检索 + 工具调用，显式建模工具依赖关系 |
| 12 | Agentic RAG Survey | 2025 | Agentic RAG 全景综述与分类法 |
| 13 | Learning to Route | 2025 | 规则驱动路由，混合源检索（文档+数据库） |
| 14 | GlyRAG | 2026 | 上下文感知 RAG 用于血糖预测，多模态融合 |
| 15 | FinAgent-RAG | 2026 | 迭代检索-推理-自校验，面向金融文档问答 |
| 16 | Sustainable Digitalization with Multi-Agent RAG | 2025 | 多智能体 RAG 支持企业可持续信息抽取 |
| 17 | Finance Agent Benchmark | 2025 | 金融研究任务智能体基准与评测框架 |
| 18 | Retrieve, Schedule, Reflect | 2026 | Agentic RAG 驱动芯片 QoR 优化调度 |
| 19 | Towards Interpretable and Trustworthy TS Reasoning | 2025 | 可解释时序推理蓝图：多智能体 + 多模态 + 检索增强 |
| 20 | Reimagining RAN Automation in 6G | 2026 | 6G 网络中的分层决策智能体框架 |
| 21 | Rashomon Set Agents | 2026 | 多智能体概率建模社会认知不确定性 |
| 22 | RELOOP | 2025 | 结构感知多跳检索与规划推理 |
| 23 | ERATTA | 2024 | 企业表格问答的极限 RAG 架构 |
| 24 | EnterpriseBench | 2025 | 企业场景下 LLM 智能体评测沙盒 |
| 25 | Long-Term Open-Web Research Benchmark | 2024 | 真实开放网络研究任务的长期基准 |

---

## 论文详解（中文润色，不改原意）

### 1) Integrating Traditional Technical Analysis with AI
- 作者：Michał Wawer, Jarosław A. Chudziak
- arXiv：2506.16813（2025-06-20）
- 摘要译文：论文提出 ElliottAgents，将艾略特波浪理论与多智能体 LLM 结合，用 RAG 与 DRL 持续分析市场数据，识别波浪结构并预测价格走势。作者在美国大型公司历史数据上验证了其在不同时间尺度的模式识别和趋势预测有效性，强调传统技术分析与现代 AI 的可融合性。

### 2) The New Quant
- 作者：Weilong Fu
- arXiv：2510.05533（2025-10-07）
- 摘要译文：综述系统梳理了 LLM 在金融预测与交易中的应用，从情绪/事件抽取、数值推理、多模态理解到 Agentic 系统与工具协同。文章强调评估应覆盖成本、延迟、容量与时间安全性，并指出生产落地中的关键挑战包括时间泄漏、幻觉、可解释性与治理安全。

### 3) Enhancing Financial RAG with Agentic AI and Multi-HyDE
- 作者：Akshay Govind Srinivasan et al.
- arXiv：2509.16369（2025-09-19）
- 摘要译文：该工作引入 Multi-HyDE，多样化生成假设查询以覆盖更多检索视角，并与多步 Agent 推理结合。实验显示在金融问答中准确率提升 11.2%，幻觉降低 15%，说明“多视角检索 + 结构化代理流程”能显著提升高风险场景可靠性。

### 4) A Role-Aware Multi-Agent Framework for Financial Education QA
- 作者：Andy Zhu, Yingjun Du
- arXiv：2509.09727（2025-09-10）
- 摘要译文：论文构建“生成器-检索器-专家评审”三角色单轮协作框架，面向金融教育问答中的多步数值推理需求。基于 3532 道专家题的结果显示，批判式 refinement 相比零样本 CoT 提升 6.6%–8.3%，并在成本上具备优势。

### 5) Rethinking Retrieval...
- 作者：Elias Lumer et al.
- arXiv：2511.18177（2025-11-22）
- 摘要译文：作者系统比较了向量式 Agentic RAG 与非向量层级结构遍历。基于 1200 份 SEC 文件与 150 题评测，向量方案在成对比较中胜率 68%；交叉编码重排与 small-to-big chunking 均显著提升检索质量，但需平衡延迟与成本。

### 6) Agentic RAG for Time Series Analysis
- 作者：Chidaksh Ravuru et al.
- arXiv：2408.14484（2024-08-18）
- 摘要译文：提出分层多智能体框架：主控代理将请求分发给任务化子代理，子代理通过共享提示池检索历史模式知识并进行任务微调。论文声称在多项时序任务基准上表现达到 SOTA，并具备模块化扩展能力。

### 7) Agentic AI... Institutional Turn
- 作者：Marcel Osmond
- arXiv：2603.13244（2026-02-20）
- 摘要译文：文章从法律与金融治理角度讨论 Agentic AI 的制度挑战，主张治理重心应由训练期对齐转向运行期制度设计，如治理图、惩罚函数与可观察行为约束。核心观点是：与其追求模型“完美内化价值”，更关键是构造“合规行为最优”的制度环境。

### 8) AI for Climate Finance
- 作者：Saeid Ario Vaghefi et al.
- arXiv：2504.05104（2025-04-07）
- 摘要译文：针对气候适应资金（特别是 EWS）追踪难题，论文提出结合检索、微调与多步推理的 Agentic 系统。以 CREWS 基金项目文档为例，Agent-RAG 方案在分类任务上达到 87% 准确率，并提供了可复用基准数据。

### 9) Adaptive Query Routing
- 作者：Afshan Hashmi
- arXiv：2604.14222（2026-04-14）
- 摘要译文：工作比较向量检索、树推理与自适应混合检索（AHR），并按查询复杂度分层评测。结果表明不存在单一全胜范式：树推理总体最好，但在多文档综合问题上向量方案更强，支持“按题型动态路由”的设计。

### 10) MarketSenseAI 2.0
- 作者：George Fatouros et al.
- arXiv：2502.00415（2025-02-01）
- 摘要译文：框架通过 LLM 处理新闻、价格、基本面与宏观信息，并用多智能体 + RAG 汇总 SEC 文件与财报电话会信号。作者报告在 S&P100 两年回测中累计收益 125.9%（对比指数 73.5%），并在 S&P500 测试中展现可扩展性。

### 11) Graph RAG-Tool Fusion
- 作者：Elias Lumer et al.
- arXiv：2502.07223（2025-02-11）
- 摘要译文：针对传统 RAG 工具检索忽略工具依赖关系的问题，论文将向量检索与图遍历融合，显式恢复嵌套依赖。其在 ToolLinkOS/ToolSandbox 上相对朴素 RAG 的 mAP@10 分别绝对提升 71.7% 与 22.1%。

### 12) Agentic RAG Survey
- 作者：Aditi Singh et al.
- arXiv：2501.09136（2025-01-15）
- 摘要译文：这是一篇 Agentic RAG 系统综述，给出基于代理数量、控制结构、自主性与知识表示的分类法。文章同时总结了医疗、金融、教育、企业文档场景实践，并指出评估、协同、记忆、效率与治理等开放问题。

### 13) Learning to Route
- 作者：Haoyue Bai et al.
- arXiv：2510.02388（2025-09-30）
- 摘要译文：论文指出文档与关系型数据库在问答中各有优势，盲目融合会带来噪声和成本。其规则驱动路由代理为每个问题选择最优增强路径，并用元缓存复用相似路由决策，在准确率与计算成本之间取得更好平衡。

### 14) GlyRAG
- 作者：Shovito Barua Soumma, Hassan Ghasemzadeh
- arXiv：2601.05353（2026-01-08）
- 摘要译文：GlyRAG 直接从 CGM 序列抽取语义上下文，不依赖额外传感器；LLM 生成临床摘要并与血糖 patch 表征做多模态融合，再通过检索类似历史片段辅助预测。实验显示在两组 T1D 队列上 RMSE 最多降低 39%，低血/高血事件预测显著改善。

### 15) FinAgent-RAG
- 作者：Yang Shu, Yingmin Liu, Zequn Xie
- arXiv：2605.05409（2026-05-06）
- 摘要译文：该方法面向金融文档中的多步数值推理，采用“对比检索器 + 可执行 Python 的 Program-of-Thought + 自适应策略路由”三组件。结果在 FinQA/ConvFinQA/TAT-QA 上相对最强基线提升 5.62–9.32 个百分点，并在保证精度下显著降低 API 成本。

### 16) Sustainable Digitalization with Multi-Agent RAG and LLM
- 作者：Muhammad Arslan et al.
- arXiv：2502.15700（2025-01-06）
- 摘要译文：文章聚焦企业可持续数字化，主张用现成 LLM + RAG 取代高成本新模型训练。通过多智能体分解检索、增强、分类任务，实现更高资源效率，并强调与联合国 SDGs 的一致性。

### 17) Finance Agent Benchmark
- 作者：Antoine Bigeard et al.
- arXiv：2508.00828（2025-05-20）
- 摘要译文：提出真实金融研究任务基准，覆盖 9 类任务、537 道专家题，并配备搜索与 EDGAR 工具链。评测显示当前最优模型准确率仍仅 46.8%，且单题平均成本约 3.79 美元，凸显高风险金融落地仍有明显差距。

### 18) Retrieve, Schedule, Reflect
- 作者：Yikang Ouyang et al.
- arXiv：2603.13767（2026-03-14）
- 摘要译文：该工作将 Agentic LLM 接入 EDA 工具做芯片 QoR 调度优化，并借助 RAG 提供专家知识树。相较黑盒搜索（如 RL），论文报告时序优化提升约 10%、功耗和面积更优、速度超过 4 倍。

### 19) Towards Interpretable and Trustworthy TS Reasoning
- 作者：Kanghui Ning et al.
- arXiv：2510.16980（2025-10-19）
- 摘要译文：文章提出时序推理蓝图：一条线建设“时间理解-多步推理-可信评估”基础能力，另一条线推进“多智能体协作+多模态上下文+检索增强”的系统级推理。目标是实现可解释、可信赖的时序智能。

### 20) Reimagining RAN Automation in 6G
- 作者：Md Arafat Habib et al.
- arXiv：2604.03908（2026-04-05）
- 摘要译文：论文提出 6G 无线网络 Agentic AI 框架，由超代理（H-ODT）统筹资源分配、应用编排与自愈代理，并借助 RAG 汇聚异构知识。实验在吞吐、时延、能效上优于三类基线，并展示了较强的意图校验与故障恢复能力。

### 21) Rashomon Set Agents
- 作者：Jinming Yang et al.
- arXiv：2603.20750（2026-03-21）
- 摘要译文：工作构建 LLM 驱动的多智能体概率框架，模拟学生主观社会认知差异如何在局部信息与同伴交互中演化。代理仅访问各自“主观图”上的局部信息，结合不确定性标注与信任加权更新，重现了多种真实教育场景下的群体动力学。

### 22) RELOOP
- 作者：Ruiyi Yang et al.
- arXiv：2510.20505（2025-10-23）
- 摘要译文：RELOOP 用可逆层次序列统一文本、表格、知识图谱，并通过结构感知迭代检索“刚好足够”的证据。其在 HotpotQA、HybridQA/TAT-QA、MetaQA 上较多类基线取得稳定提升，同时降低不必要的跳转、工具调用与 token 开销。

### 23) ERATTA
- 作者：Sohini Roychowdhury et al.
- arXiv：2405.03963（2024-05-07）
- 摘要译文：论文面向企业级表格问答提出极限 RAG 架构，使用多 LLM 协作进行数据认证、查询路由、检索与定制提示。其在多行业查询中报告高置信度，并提供幻觉检测打分模块，强调企业场景下可扩展性与稳定性。

### 24) EnterpriseBench
- 作者：Harsh Vishwakarma et al.
- arXiv：2510.27287（2025-10-31）
- 摘要译文：该基准模拟企业环境中的数据分散、权限控制与跨部门流程，覆盖 500 项任务。评测显示即便最强智能体任务完成率也只有 41.8%，说明企业级 Agent 系统仍有明显改进空间。

### 25) Long-Term Open-Web Research Benchmark
- 作者：Peter Mühlbacher et al.
- arXiv：2409.14913（2024-09-23）
- 摘要译文：工作提出面向“具经济价值白领任务”的开放网络研究基准，任务形态贴近金融与咨询中的真实杂乱问题。实验显示具备子任务委派能力的 ReAct 架构整体表现最好，并给出了对多模型代理轨迹的定量与定性分析。

---

## 集成模式统计

### 智能体架构模式
- Agentic Workflow：15 篇
- Multi-Agent System：8 篇
- Single Agent：5 篇

### RAG 集成模式
- Standard RAG：4 篇
- Hybrid Retrieval：4 篇
- Vector Retrieval：3 篇
- GraphRAG：1 篇

### 领域侧重点
- Financial Analysis：17 篇
- Time Series / Forecasting：7 篇
- Market Analysis：6 篇
- Trading / Stock：5 篇

---

## 关键结论

- Agent + RAG 正在成为金融智能体的重要范式，尤其在 2025–2026 年快速增长。  
- 复杂金融任务更偏好多角色协作的多智能体架构。  
- RAG 在系统中承担“外部记忆”角色，对时效性决策至关重要。  
- 结构化市场数据与非结构化文本、时序数据的统一融合仍是瓶颈。  
- 评测仍偏碎片化，跨论文横向比较困难。

---

*说明：本文件为中文润色重写版，保持原文结论、机制描述与关键数字含义不变。*
