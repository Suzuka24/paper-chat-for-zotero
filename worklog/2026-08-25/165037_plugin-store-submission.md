# Zotero 中文社区插件收录

## 计划

### 目标

完善 Paper Chat for Zotero 的公开安装信息，并向 Zotero 中文社区当前使用的插件数据仓库提交正式收录 PR。

### 范围

- 在中英文 README 和 v0.6.0 Release 中明确首次安装需要本地 bridge，避免用户只安装 XPI 后无法连接。
- 完善 GitHub 仓库的 About 描述、主页和 topics。
- 在 `syt2/zotero-addons-scraper` 中新增插件条目，使用 `ai`、`reader` 标签。
- 验证插件 XPI、社区条目格式及两边远端状态。

### 关键步骤

1. 修改并验证插件仓库的公开安装说明。
2. 直接 fast-forward 更新插件仓库 `main`，同步 Release 与 About 信息。
3. fork 社区收录仓库，在独立分支添加 `addons/Suzuka24@paper-chat-for-zotero`。
4. 运行相关校验、提交并创建面向上游 `master` 的正式 PR。
5. 检查 PR 状态和自动检查，记录上线等待项。

### 验证方式

- `scripts/test.py`、`git diff --check` 通过。
- 社区仓库 tag review 和相关测试通过。
- PR 的 base/head、文件差异及 GitHub checks 正确。

## 实施记录

- 2026-08-25 16:50：确认旧 `zotero-chinese/zotero-plugins` 已停止接收新插件，当前应提交至 `syt2/zotero-addons-scraper`；确认 scraper 支持 Zotero 9、GitHub Release XPI 和当前插件 manifest。
- 2026-08-25 16:51：在中英文 README 顶部明确“仅安装 XPI 无法完成首次安装”，插件仓库测试通过并直接 fast-forward push 到 `main`（`48d23d5`）。
- 2026-08-25 16:52：完善 GitHub About 双语描述、Release 主页及 `zotero`、`zotero-plugin`、`codex`、`ai`、`research` topics；重写 v0.6.0 Release 安装说明，提供固定源码包和中英文指南链接。插件仓库 `main` CI `32828793878` 双平台通过。
- 2026-08-25 16:53：fork `syt2/zotero-addons-scraper`，在 `add-paper-chat-for-zotero` 分支新增 `addons/Suzuka24@paper-chat-for-zotero`，标签为 `ai`、`reader`；官方 tag review 与相关 7 个单元测试通过。
- 2026-08-25 16:54：创建正式非 Draft PR `syt2/zotero-addons-scraper#206`；base 为上游 `master`，head 为 `Suzuka24:add-paper-chat-for-zotero`，自动 Addon Tag Review `32828972485` 通过，当前状态可合并。

## 总结

### 实际完成内容

- 完善插件仓库中英文 README、GitHub About、topics 和 v0.6.0 Release 首次安装说明。
- 创建并验证社区收录条目，向当前数据源仓库提交正式 PR：<https://github.com/syt2/zotero-addons-scraper/pull/206>。

### 验证结果

- 插件仓库 `scripts/test.py`、Windows/macOS CI 通过。
- 社区条目官方 tag review、7 个相关单元测试及 PR 自动检查通过。
- PR 仅新增一个预期文件，提交身份、base/head 和标签均正确。

### 未完成事项或剩余风险

- PR 已满足合并条件，但最终合并权限属于 `syt2/zotero-addons-scraper` 维护者；合并及其后定时抓取完成后，插件才会出现在 Zotero 中文社区页面。
