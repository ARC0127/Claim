# CLI 与客户端

[返回主页](../README.md)

Claim 可以从命令行启动，也可以安装为客户端 skill。两种方式读取同一套协议；无需为了换客户端维护第二份教学规则。

## 命令行启动

在解压目录或仓库根运行，Python 版本至少为 3.10：

Windows 若没有 `python` 命令，可将下列命令中的 `python` 换成 `py -3`。

```bash
python claim/scripts/claim.py --version
python claim/scripts/claim.py doctor
python claim/scripts/claim.py run --client claude --mode coach --request "逐轮引导我分析研究主张"
```

`run` 打开所选原生客户端的交互会话。可选客户端是 `claude`、`codex`，可选模式是 `coach`、`review`、`proof`。它将 Claim 目录交给客户端读取，不另建 API 账户，也不指定模型。账户、权限提示和工具访问仍由客户端处理。

例如，直接检查或准备形式证明：

```bash
python claim/scripts/claim.py run --client claude --mode review --request "检查当前目录中的主张和论证"
python claim/scripts/claim.py run --client codex --mode proof --request "读取我已确认的定理义务，先核对形式化目标"
```

每次 `run` 启动新会话。后续交流在该会话中继续，历史确认不会由启动器自动恢复。模型读取已有记录时，仍须按 Claim 的原话确认与版本规则处理。

加上 `--dry-run` 只打印参数，不启动客户端。`doctor` 只检查本地路径，不尝试登录、调用模型或连接证明平台。缺少客户端时会明确报错，可以改用上下文导出。

## 导出给其他助手

```bash
python claim/scripts/claim.py prompt --mode coach --request "我希望论文说明……" --output claim-context.md
```

输出包含入口和所选模式的主要参考协议，采用 UTF-8。目标文件已经存在时拒绝覆盖。需要更换文件名，或自行确认并处理旧文件。

将上下文文件交给助手，同时提供完整 `claim/` 文件夹供后续按需读取。能读文本不等于能搜索网页；没有检索工具时，助手应指出哪些来源尚未核验。

## Claude Code

个人安装目录为 `~/.claude/skills/claim/`，项目安装目录为 `.claude/skills/claim/`。安装后使用 `/claim`。这些目录与调用方式来自 [Claude Code 官方 skills 文档](https://code.claude.com/docs/en/skills)，于 2026-09-17 核对。

首次个人安装，Windows PowerShell：

```powershell
$claimSkillsRoot = Join-Path $env:USERPROFILE ".claude\skills"
Expand-Archive -LiteralPath ".\dist\Claim-0.3.0.zip" -DestinationPath $claimSkillsRoot
```

macOS / Linux：

```bash
mkdir -p "$HOME/.claude/skills"
unzip dist/Claim-0.3.0.zip -d "$HOME/.claude/skills"
```

也可直接复制整个 `claim/` 文件夹到上述目录。项目内安装把目标改成该项目的 `.claude/skills/`。网页端或云端会话不一定读取本机个人目录，应使用对应客户端的上传或项目文件入口。

## Codex

安装到配置的 `CODEX_HOME/skills/claim/`；没有自定义位置时通常为 `~/.codex/skills/claim/`。调用 `$claim`。

```powershell
$claimSkillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME "skills"
} else {
    Join-Path $env:USERPROFILE ".codex\skills"
}
Expand-Archive -LiteralPath ".\dist\Claim-0.3.0.zip" -DestinationPath $claimSkillsRoot
```

## 升级已有安装

先查看旧目录是否有自己的改动，并将完整旧目录备份到 skills 目录之外。然后替换为新版完整 `claim/`，不要混合两个版本。用下面的命令核对版本：

```bash
python /path/to/skills/claim/scripts/claim.py --version
```

维护者可用仓库的 `tools/validate.py --installed /path/to/skills/claim` 比较完整文件集和字节。客户端已经读入的旧内容不会被磁盘更新追溯修改；新会话应重新读取入口。

## 可选本地工具交接

显式指定要检查的本地 skill 目录：

```bash
python claim/scripts/claim.py doctor --companion /path/to/selected/skill
```

`ENTRY_PRESENT_NOT_EXECUTED` 只表示入口文件存在，尚未执行。助手应按用户请求读取该入口，交接当前主张版本、已确认条件、证明义务和剩余任务。未指定工具时不自动查找个人安装。

[本地交接协议](../claim/references/local-tools.md)保留辅导阶段的用户决定权，不预设其他工具的品牌、能力或内部结构。
