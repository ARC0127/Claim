# Claim

<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>

![Claim — 明确一项研究主张究竟需要证明什么](docs/assets/claim-cover.svg)

## AI 把答案写完整了，你却可能完全没有理解。

把一个想法交给 AI，它可以接着列出假设、推荐定理，再写出一段看似完整的证明。你读着觉得合理，讨论也顺利推进了。可当别人追问“为什么需要这个假设”“换一个量词还成立吗”“哪种反例能推翻它”，你才发现：自己接受了答案，却没有走过形成判断的过程。

**研究不能只剩下 AI 负责推理，你负责确认。** 尤其是理论工作：如果主张、假设和证明目标都由 AI 决定，你可能拿到一份越来越成熟的文本，却仍然说不清它为什么成立。

Claim 把这些关键判断留在对话里，让你亲自完成。AI 可以解释概念、搜索文献、构造反例和检查推理；你先说出想证明什么，决定愿意接受哪些条件，再尝试写出**证明义务**——让论证成立所缺少的精确结论。它是一套面向科研对话的 skill，目标是让 AI 的帮助成为理解的支撑，而不只是答案的来源。

需要直接审计已有论证或继续写形式证明时，也可以明确切换路线；直接交付与独立练习分别记录。

**0.3.0 · internal** · 支持通用 CLI、Claude Code 和 Codex · Python 3.10+

[快速开始](#快速开始) · [完整安装](#完整安装) · [逐轮辅导](#逐轮辅导怎样进行) · [具体案例](#看一次具体反馈) · [形式证明](#继续完成形式证明) · [常见问题](#常见问题)

## Claim 适合处理什么

**前提成立，结论却没有接上。** 每个点分别成立的结论，未必能同时覆盖整个范围。Claim 检查尚未成立的推理，帮助你发现结论真正要求的量词。

**反例出现，假设越加越多。** 新增条件可能排除原本最关心的情形。Claim 先让你尝试提出最小条件，再检查它阻断了什么反例、牺牲了什么范围，以及是否只是重述结论。

**知道定理名字，却写不出要证明哪一句。** “用集中不等式”还不是证明义务。Claim 对照你写出的输入、输出、量词与误差，解释关键缺项，再进入理论工具检索。

**已有证明，却不确定证明了原来的主张。** Claim 核对形式命题、前提、证明依赖和应用条件，区分数学命题成立与具体实现满足条件。

Coaching 路线用于练习自己的理论判断；Review 路线用于直接获得检查结果。Claim 不会因为上下文已经足够，就默认把辅导变成代写完整理论。

## 快速开始

下载 [Claim-0.3.0.zip](dist/Claim-0.3.0.zip)，解压后保留完整的 `claim/` 文件夹。下面的启动命令在仓库根目录，或包含该文件夹的解压目录执行。

已安装 Claude Code：

```bash
python claim/scripts/claim.py run --client claude --request "逐轮引导我分析论文主张，不要替我完成理论"
```

使用 Codex CLI：

```bash
python claim/scripts/claim.py run --client codex --request "逐轮引导我分析论文主张"
```

Windows 没有 `python` 命令时可换成 `py -3`；macOS / Linux 可使用 `python3`。客户端需要已安装并能从命令行找到，账户与认证由客户端处理。

进入对话后，用自己的话说明希望读者相信什么。不需要先知道定理名称，也不需要提前写好一整套理论框架。

## 完整安装

### 方式一：直接运行 CLI

无需复制到个人 skills 目录。保留解压后的文件夹，即可使用：

```bash
python claim/scripts/claim.py --version
python claim/scripts/claim.py doctor
python claim/scripts/claim.py run --client claude --mode coach --request "我的主张是……"
```

启动器调用所选客户端，沿用其模型、账户和交互权限，不指定模型，不绕过权限提示。每次 `run` 都启动新会话；后续交流在该会话中继续。

### 方式二：安装为客户端 skill

| 客户端 | 个人安装位置 | 项目安装位置 | 调用 |
|---|---|---|---|
| Claude Code | `~/.claude/skills/claim/` | `.claude/skills/claim/` | `/claim` |
| Codex | `$CODEX_HOME/skills/claim/`；默认 `~/.codex/skills/claim/` | 按客户端实际配置 | `$claim` |
| 其他助手 | 将完整文件夹放在助手可读取的位置 | 按助手的文件入口配置 | 明确要求读取 `claim/SKILL.md` |

首次安装到 Claude Code，Windows PowerShell：

```powershell
$claimSkillsRoot = Join-Path $env:USERPROFILE ".claude\skills"
Expand-Archive -LiteralPath ".\Claim-0.3.0.zip" -DestinationPath $claimSkillsRoot
```

首次安装到 Codex，Windows PowerShell：

```powershell
$claimSkillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME "skills"
} else {
    Join-Path $env:USERPROFILE ".codex\skills"
}
Expand-Archive -LiteralPath ".\Claim-0.3.0.zip" -DestinationPath $claimSkillsRoot
```

macOS / Linux：

```bash
# Claude Code
mkdir -p "$HOME/.claude/skills"
unzip Claim-0.3.0.zip -d "$HOME/.claude/skills"

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
unzip Claim-0.3.0.zip -d "${CODEX_HOME:-$HOME/.codex}/skills"
```

上述安装命令假定下载包位于当前目录；从仓库安装时，路径改为 `dist/Claim-0.3.0.zip`。也可以直接复制完整 `claim/` 文件夹。

已有安装时不要直接混合两版文件：先检查个人改动，将旧目录备份到 skills 目录之外，再替换完整目录。安装完成后开启新会话，重新读取入口。

### 方式三：导出上下文给其他助手

```bash
python claim/scripts/claim.py prompt --mode coach --request "我的论文主张是……" --output claim-context.md
```

导出文件包含入口与所选模式的主要协议，编码为 UTF-8；同名文件已存在时拒绝覆盖。仍需让助手能读取完整 `claim/` 文件夹，以便后续按需加载其他协议。

文本导出不会给助手增加联网或执行工具。科学来源核验需要真实网页检索；形式证明需要可用的 Lean 环境。

## CLI 命令速查

| 命令或选项 | 用途 |
|---|---|
| `--version` | 显示包内版本 |
| `doctor` | 检查客户端路径和本地 Lean/Lake；不登录、不联网 |
| `run --client claude\|codex` | 启动显式选定的原生客户端 |
| `--mode coach` | 默认模式，逐轮辅导 |
| `--mode review` | 直接检查主张与论证 |
| `--mode proof` | 处理已明确的形式证明任务 |
| `--request "…"` | 本次请求，启动与导出时必填 |
| `--dry-run` | 只打印启动参数，不发起对话 |
| `prompt --output 文件名` | 创建上下文文件；省略 output 则输出到终端 |

例如：

```bash
python claim/scripts/claim.py run --client claude --mode review --request "检查当前目录里的主张与证明"
python claim/scripts/claim.py run --client codex --mode proof --request "读取已确认的证明义务，先核对形式命题"
python claim/scripts/claim.py run --client claude --request "逐轮辅导我" --dry-run
```

归档和深入讲解属于对话内请求，不是额外的 CLI 模式。启动器不会根据历史文件自动补齐用户确认。

## 逐轮辅导怎样进行

每轮只推进一个决定。你保留主张、排除范围、假设和失败规则的决定权，也先尝试写出需要证明的结论。

| 阶段 | 你需要作出的判断 | Claim 的帮助 |
|---|---|---|
| S1 主张 | 希望读者相信什么，对象与范围是什么 | 拆解对象、条件、比较对象和结论，不补新方法 |
| S2 形式化 | 数学命题是否仍是原意 | 写清量词，逐一解释符号，等待确认 |
| S3 反例 | 反例是否在范围内，是否愿意排除 | 检查前提并构造反例，不同时给出修复 |
| S4 假设 | 先尝试最小限制，再接受、拒绝或保留未知 | 检查是否阻断反例、是否循环，以及范围代价 |
| S5a 证明义务 | 先写需要的输入、输出、量词和误差结论 | 指出最影响下一步推理的一处缺项 |
| S5b 理论类型 | 先解释为什么推不下去，再尝试归类 | 允许多个类别、其他或未知，再检索适用工具 |
| S6 失败条件 | 什么结果足以让自己放弃当前主张 | 检查证伪条件是否对应当前量词与范围 |
| S7 归档 | 前置判断确认后，明确要求整理 | 只导出已确认版本，保留未证义务与未知项 |

不需要为了“通关”虚构条件。纯数学命题可能没有方法比较对象；确定性结论可能不涉及概率；没有找到反例也可以如实记录查找范围，由你决定是否条件化继续。

### 固定格式与状态

S1–S6 使用四个固定标题。状态块紧跟第一个标题，当前普通辅导轮示例为：

```text
1. **你刚才表达了什么**

`阶段 S1 · GATE OPEN`
`模式：STANDARD`
`检索：NO_NEW_SCIENTIFIC_CONTENT`

2. **我如何形式化**

3. **当前最大歧义**

4. **一个需要你亲自回答的问题**
```

`OPEN` 表示当前判断尚未解决；通过需要你的明确作答满足要求。“继续”不替代缺失的决定。最后一节保留一个需要你回答的问题。

中英文 README 介绍同一套协议。当前固定辅导标题、状态前缀和公式符号解释采用中文；英文主页不会自动把执行协议改成全英文。维护文件、查版本等请求不套这个教学模板。

### 卡住时可以怎样问

- **“详细解释这个概念，但不要推进。”** 进入 `DEEP_DIVE`，可充分展开当前概念，阶段不变。
- **“我还想不出怎么限制这个反例。”** 先解释反例利用的自由度，再给无关领域的中性例子；仍无法表达时才给候选条件。
- **“检查我写的证明目标，不要直接给答案。”** Claim 解释你的目标已经覆盖什么、还缺哪一处，再让你修订。
- **“这次我希望你直接审计。”** 明确切换到 Review；不会把 AI 写出的答案记成你的独立完成。

每次关键判断后，可以做一句简短学习回看：刚才用了什么分析能力，它为什么决定下一步需要哪类结论。

## 看一次具体反馈

> **学习者：**“每个点的函数值都趋于零，所以整个区间的误差最终可以同时任意小。”
>
> **Claim：**“每个点分别等到误差足够小，不代表存在一个所有点共用的起点。你还缺少整个区间上的统一误差控制。”
>
> **留给学习者的问题：**“要让所有点同时满足要求，你需要的结论与已有逐点结论有什么不同？”

这个实分析问题可以继续训练：量词顺序、随序号改变的反例、上确界与最大值、缩小定义域的代价，以及如何提出统一误差义务。

[完整进阶案例](docs/examples.md)附有作答后才展开的数学核对和“极限与求导”迁移题。所有案例独立于具体研究项目；迁移题不提前给答案，也不混入原主张归档。

## 文献、反对意见与公式

### 每次实质性修改都重新检索

新增或改变主张、假设、量词、定义、证据或证明步骤时，Claim 要求针对这次变化重新搜索网页。旧文献只能作为候选，重新打开并核对适用性后才能继续使用；书目可以不变，但核对过程不能省略。

纯粹确认已展示的内容、调整排版或原样导出，不算新增科学内容。搜索失败时明确记录未核实，不用模型记忆伪装已经查证。

### 反对意见必须有依据

遇到与已知结果存在实质冲突的思路，Claim 先检索，再说明冲突位置、原命题条件、适用范围和直接来源。引用应包含作者或发布机构、标题、年份、出处、DOI 或稳定链接，以及支持哪句话。

反对的是可检查的推理，不是研究者本人。发现反证不授权 AI 替你选择新的主张或接受假设。

### 每个符号都要解释

公式附近必须说明变量、函数、集合、下标、量词和概率对象的含义、取值域、单位及依赖关系。首次出现的英文缩写要展开并解释。符号缺少定义时保留未知，不能用一串英文标签代替说明。

## 修订、归档与迁移

你可以随时修改已经确认的主张。Claim 保留旧文本、修改原因与范围代价，并重开受影响的下游阶段，避免为了躲避反例悄悄换命题。

当前对话中的用户原话可直接沿用；跨对话恢复必须找到逐字原话，先标记 `UNCONFIRMED_PRIOR_USER_CLAIM`，展示后由你确认。AI 总结只能定位，不能替代确认。

S1–S6 完成后，可明确请求导出 Theory Specification、论证依赖图或定理义务清单。归档保存已确认判断，未证目标仍未证，`UNKNOWN` 不会因排版而变成事实。

迁移练习另行进行：对相邻但不同的主张，独立识别对象、量词和第一处推理缺口。记录提示与独立作答的区别；共同完成当前主张不等于已经掌握方法。

## 继续完成形式证明

明确证明义务后，可以请求：

```text
把当前确认的证明义务写成 Lean 证明。
先核对自然语言命题与形式命题，再拆分引理并检查实际编译结果。
```

工作链为：

```text
已确认主张
  → 精确证明义务
  → 自然语言论证与子引理
  → 固定环境中的 Lean 形式化
  → 编译、完整命题与传递公理检查
  → 可选 Prove2Me 目标、依赖与提交状态
  → 回查应用是否满足定理前提
```

Lean 检查形式证明；Prove2Me 可组织目标、拆分义务并核对提交。依赖图应区分编译器提取的逻辑依赖、尚未证明的分解和实现或实验支持，不能把所有箭头都画成已证明的蕴含。

检查不止看“编译成功”，还要确认命题没有被弱化、没有借助未证明的目标或占位公理。平台的等待、分解接受与证明接受是不同状态；任何状态都只适用于实际核对的目标。

包内 [ClaimDemo.lean](claim/assets/proof-demo/ClaimDemo.lean)证明两个偶数相加仍为偶数，仅用于最小编译检查。在已有 Lean 项目环境中运行：

```bash
lake env lean /path/to/claim/assets/proof-demo/ClaimDemo.lean
```

文件会打印完整命题和公理依赖。实际研究应固定工具链与依赖版本。实分析教学案例尚未做 Lean 形式化，不要把最小算术示例的通过当作它的机器证明。[证明路线详情](docs/proof-workflow.md)

## 已验证什么

| 层次 | 已有结果 |
|---|---|
| 文件与发行 | UTF-8、固定中文模板、manifest、链接、校验和、ZIP 字节与确定性重建通过 |
| 程序回归 | 22 项测试覆盖发行与 CLI；模拟调用测试不等于真实模型对话 |
| 本地安装 | Codex 与 Claude Code 副本完成文件集和字节比较 |
| Windows 中文 | PowerShell 5.1 默认与显式读取核对，并使用错误编码作为对照 |
| 最小形式证明 | Lean 4.33.1 实际编译通过，偶数加法命题无公理依赖 |
| 模型与教学 | 尚未开展实际辅导遵循率或人类学习效果评测 |

当前更新保持 0.3.0，压缩包已重新构建，请以[当前 SHA-256](dist/SHA256SUMS.txt)核对下载。完整命令与记录见[验证说明](docs/validation.md)。

## 常见问题

**必须使用 Codex 吗？** 不需要。可以使用 Claude Code、通用 CLI，或将协议交给能读取文件的其他助手。客户端提供模型、搜索和执行工具，Claim 提供对话规则。

**下载 ZIP 后为什么没有测试脚本？** ZIP 是可安装的 `claim/` skill；完整验证工具、测试和文档在仓库中。只运行 skill 不需要下载整套仓库。

**看不到 skill 或仍用旧格式怎么办？** 检查路径是否恰好是 `skills/claim/SKILL.md`，不要多套一层文件夹；更新后开启新会话，明确读取入口。

**中文乱码怎么办？** 不复制旧对话里的损坏标题。重新显式读取 UTF-8；辅导协议使用兼容 Windows 的 BOM，Python 可用 `utf-8-sig`。磁盘更新不能修复已经生成的历史文字。

```powershell
Get-Content -LiteralPath "实际路径/claim/SKILL.md" -Encoding UTF8
```

**没有搜索工具或 Lean 怎么办？** 没有搜索时不能完成科学来源核验，应保留未核实状态；没有 Lean 时可以整理形式目标与运行说明，但不能声称编译通过。

**可以直接让 AI 写答案吗？** 可以明确请求 Review 或形式证明。区别是直接交付不会被记成研究者独立完成的辅导阶段。

## 仓库与维护

```text
README.md / README.zh-CN.md  中英文完整入口
claim/                      可独立安装的 skill
  SKILL.md                  模式路由与共享规则
  references/               辅导、检查、归档、证明协议
  scripts/claim.py           CLI
  assets/proof-demo/         最小 Lean 示例
docs/                       专题指南与验证记录
tools/                      验证与打包程序
tests/                      回归与 Windows 编码检查
dist/                       安装 ZIP 与校验和
```

维护者在仓库根目录运行：

```bash
python -B tools/validate.py
python -B -m unittest discover -s tests -v
python -B tools/package.py --check
python -B tools/validate.py --installed /path/to/skills/claim
```

需要重新打包时使用 `python -B tools/package.py --write`。先检查源文件，再比较 ZIP 与安装副本，不以文件存在代替验证。

[使用指南](docs/guide.md) · [CLI 详解](docs/cli.md) · [进阶案例](docs/examples.md) · [证明路线](docs/proof-workflow.md) · [设计依据](docs/design-notes.md) · [验证记录](docs/validation.md) · [版本记录](docs/changelog.md)
