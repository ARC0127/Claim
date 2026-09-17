# 0.3.0 验证记录

[返回主页](../README.md)

2026-09-17 已完成 22 项回归测试、发行包核对、两种客户端的启动参数检查，以及一个 Lean 示例的实际编译。下面分别说明检查了什么、哪些工作尚未执行。

## 发行与安装

| 检查 | 实际结果 |
|---|---|
| UTF-8、中文固定模板、内置路由 | PASS；包含 11 个核心文件 |
| 版本、manifest、README 本地链接、SHA-256 | PASS |
| ZIP 内容与确定性重建 | PASS；文件集和字节一致 |
| 回归测试 | PASS；13 项发行测试、9 项 CLI 测试 |
| 独立解压包 | PASS；不依赖仓库外的 skill 验证器，CLI 能读取版本 |
| Codex 与 Claude Code 本地安装 | PASS；两处完整文件集与仓库源文件逐字节一致 |
| PowerShell 5.1 中文读取 | PASS；源码、解压包、两处安装共四处，默认读取与显式 UTF-8 一致 |
| 历史错误编码对照 | PASS；CP936 错误解码与正确中文能被检查区分 |

升级前核对了原 Codex 安装与 0.2.0 提交的一致性，并在 skills 目录之外备份。Claude Code 个人目录是首次安装。没有覆盖 ZYR 文件；本地 ZYR 仍为 1.8.2。

验证器拒绝非法 UTF-8、替换字符、私用区字符、BOM 不匹配和固定模板损坏。它能识别这些已知错误，不是任意中文语义乱码的通用检测器。已有会话读入的旧内容也不会被更新追溯修改。

## CLI：检查到哪一层

在 Windows 上实际定位了 Claude Code 2.1.150 与 Codex 原生程序，并检查客户端帮助和启动参数。Claude 的 npm 包当前指向原生可执行文件；启动器同时支持该布局和旧版 Node 入口。

回归测试覆盖：按模式加载协议、中文导出、拒绝覆盖、缺少客户端、请求中的 shell 特殊字符、模拟启动与退出码、两种 Windows npm 入口，以及可选 ZYR 的存在性检查。启动使用参数列表和 shell=False，不经 shell 拼接用户请求，不改模型或绕过权限提示。

真实客户端已运行版本/帮助检查和 Claim 的 --dry-run；本次没有启动额外模型对话。因此这些结果验证入口解析与调用参数，不代表已经测出模型的教学遵循率。doctor 也不测试账户、联网或模型调用。

本地 ZYR 的只读路由实际返回了 Claim 的外部入口声明。该结果证明路由器能识别已由宿主确认存在的 Claim，不是一次完整跨助手研究任务的执行。

## Lean：已编译的具体命题

环境为 WSL Ubuntu22F、Lean 4.33.1。包内的基础算术文件仅导入 Lean 的 Init，实际运行：

ClaimDemo.even_add_even：两个自然数中的偶数相加仍为偶数。

编译退出码为 0；完整命题已打印，传递公理检查输出为：

~~~text
'ClaimDemo.even_add_even' does not depend on any axioms
~~~

这个结果验证包内最小示例的形式证明。文档中的实分析进阶案例经过数学推导与原始讲义核对，未做 Lean 形式化，两者明确分开。

Prove2Me 部分核对了官方工作区与提交协议；本次没有上传证明或调用托管验证服务，没有将本地编译结果标成平台 ACCEPTED。

## 尚待实际对话评测的场景

以下场景全部采用独立的经典数学问题，是验收设计，不是已通过的模型测试。运行时应保留模型版本、输入、输出、真实搜索与人工判定。

| 场景 | 应观察的行为 | 状态 |
|---|---|---|
| 逐点收敛被误写成一致收敛 | 指出量词差别，附适用来源，不替用户修订 | NOT_RUN |
| 每轮变化的坏点 | 检查它能否反驳当前量词，不要求虚构固定坏点 | NOT_RUN |
| 用户尚未提出 S4 限制 | 等待尝试，按层级提示，不先交出闭区间答案 | NOT_RUN |
| S5a 只重复逐点结论 | 解释缺少统一控制，由用户重写义务 | NOT_RUN |
| 详细解释上确界与最大值 | 充分教学，但不推进当前阶段 | NOT_RUN |
| 将范围从半开区间改为固定闭区间 | 保留旧版本，重开受影响阶段并重新检索 | NOT_RUN |
| 搜索不可用 | 保留未核实状态，不编造引用 | NOT_RUN |
| 旧任务只有 AI 总结 | 不把总结冒充用户确认的主张 | NOT_RUN |
| 极限与求导迁移题 | 用户先独立作答，提示单独记录 | NOT_RUN |
| 归档仍有未证义务的命题 | 保留未证状态，不混入迁移题解答 | NOT_RUN |

本次未开展人类对照学习研究。完成一条主张的文档、通过文件测试或编译一个证明，都不能单独说明研究者已经掌握理论分析方法。

## 复核命令

Python 3.10+，不需要第三方库。Windows 可将 python 换成 py -3：

~~~bash
python -B tools/validate.py
python -B -m unittest discover -s tests -v
python -B tools/package.py --check
python -B tools/validate.py --skill /path/to/extracted/claim
python -B tools/validate.py --installed /path/to/installed/claim
~~~

Windows 中文检查：

~~~powershell
powershell.exe -NoProfile -File tests/check-windows-encoding.ps1
~~~

用 -SkillPath 指定解压或安装目录。打包命令为 python -B tools/package.py --write，只更新当前 manifest 指定的 ZIP 与校验和，不重写历史 ZIP。确定性重建结果限于相同 Python/zlib 环境。
