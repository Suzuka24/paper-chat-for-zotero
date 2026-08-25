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

## 总结

待操作完成后补充。
