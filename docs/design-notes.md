# 设计依据

[返回主页](../README.md)

本版聚焦一项任务：让研究者亲自提出能够接上论文论证的证明义务。保留逐轮判断、渐进提示和独立迁移检查；加入更具体的义务反馈与窄范围检查协议。

## 教学参考

以下来源于 2026-09-17 重新检索并打开原始页面。检索使用认知学徒制、scaffolding/fading、AI guardrails 和 unassisted learning 等关键词；只纳入直接支持所述设计判断的原文，不把未读全文的候选文献计入证据。

**Allan Collins, John Seely Brown, Ann Holum（1991）. Cognitive Apprenticeship: Making Thinking Visible. American Educator, Winter.** [原文](https://www.aft.org/ae/winter1991/collins_brown_holum)

原文的 Traditional Apprenticeship 与 Teaching Methods 部分讨论示范、辅导、脚手架和逐步撤去支持。Claim 据此采用“先看研究者尝试，再给有限提示，并单独检查独立迁移”的设计方向。这是教学框架的启发，不是对 Claim 的实验验证。

**Hamsa Bastani, Osbert Bastani, Alp Sungu, Haosen Ge, Özge Kabakcı, Rei Mariman（2025）. Generative AI without guardrails can harm learning: Evidence from high school mathematics. PNAS, 122(26), e2422633122.** DOI: [10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122)

核对位置：Abstract、Experimental Design 和正文主结果。该高中数学随机试验区分了有工具的练习成绩与撤去工具后的考试表现。带教学约束的 GPT Tutor 缓解了负面学习效应，但文中没有观察到正向的独立考试效果。Claim 因此将辅助完成、独立迁移和文档完成分别记录，不能用漂亮答案替代学习指标。

适用边界：该研究使用 GPT-4，任务是高中数学，不是科研理论训练；它不证明 Claim、当前模型或本版提示规则具有教学效果。已核对 [2025 年 8 月 20 日更正](https://doi.org/10.1073/pnas.2518204122)：更正为作者单位的制作错误，不是结果更正。

## 设计落实

Claim 将定理义务反馈集中在输入、输出、量词、比较对象和误差之间的对应关系。每轮指出最影响当前结论的一处缺项，让研究者解释并修订，而不是同时接收一份完整答案。

形式证明路线另行处理：先核对数学目标，再编译 Lean 并检查依赖，最后回查应用条件。Prove2Me 可组织分解和提交状态；本地 ZYR 可接手研究、证明或写作中的具体任务。它们通过明确的任务交接配合，不改变辅导阶段的用户决定权。

主教学案例采用逐点与一致收敛，迁移题涉及极限与求导；基础整数算术只用于 Lean 编译检查。这些案例均独立于研究项目。CLI、原生客户端说明和教学协议分别验证。
