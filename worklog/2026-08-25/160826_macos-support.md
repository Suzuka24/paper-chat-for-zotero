# macOS 支持

## 计划

### 目标

在保持现有 Windows 行为兼容的前提下，使 Paper Chat for Zotero 可在 macOS（Apple Silicon 与 Intel）安装、自动启动、连接本地 Codex App Server，并完成 Zotero 内的真实对话。

### 范围

- 保留现有 PowerShell 安装、构建和测试入口。
- 新增 macOS 构建、安装、启动与卸载入口。
- 为插件增加 macOS token 自动发现。
- 将公共验证逻辑跨平台化，并在 GitHub Actions 中加入 macOS。
- 更新中英文安装、使用、隐私、支持与发布文档。
- 在本机 Zotero 9.0.6 上完成 XPI 安装和端到端验证。

### 关键步骤

1. 从远端重新 clone，并在 `feat/macos-support` 分支开发。
2. 实现固定版本 Codex App Server 的 macOS 架构选择、下载与摘要校验。
3. 使用用户级 `launchd` 管理 bridge，并确保 token 权限和回环监听边界。
4. 构建 XPI，执行静态检查、可复现构建和 bridge 协议冒烟测试。
5. 在 Zotero 中安装、重启并完成真实对话。
6. 审查差异，提交、推送并核对远端 CI。

### 验证方式

- Python 与 JavaScript 语法检查。
- shell 语法检查。
- 两次构建的 XPI SHA-256 一致。
- XPI 内容及 `updates.json` 校验通过。
- macOS bridge `/health`、模型读取和真实对话通过。
- Zotero 插件界面可见、连接状态正常、对话返回成功。
- GitHub Actions 的 Windows 与 macOS job 均通过。

## 实施记录

- 2026-08-25 16:08：将原无 `.git` 同步目录移至废纸篓 `/Users/suzuka/.Trash/zotero-codex-chat-pre-git-20260825-160826`，从 GitHub 重新 clone 到原路径，并创建 `feat/macos-support`。
- 2026-08-25 16:10：确认本机为 Apple Silicon、Zotero 9.0.6；系统 Python 3.9.6 不满足项目要求，后续安装器将明确检查 Python 3.10+。
- 2026-08-25 16:13：实现 `Install-macOS.py`、macOS bridge 启停脚本、用户级 `launchd`、固定 Release 架构选择、SHA-256 校验、token `0600` 权限及 macOS token 自动发现。
- 2026-08-25 16:14：首次安装成功；`/health`、模型列表和真实 bridge 对话均通过，返回 `MAC_BRIDGE_OK`。
- 2026-08-25 16:18：使用 Zotero 插件管理器安装 XPI；面板自动显示“已连接本地 Codex”，对当前论文提问后获得带“第 3 页”跳转的回答。
- 2026-08-25 16:25：版本升级为 `0.6.0`，新增跨平台测试与 release metadata 工具、macOS CI，并更新中英文文档。
- 2026-08-25 16:28：使用 `--skip-download` 验证安装器幂等升级；原 token 保持不变，`launchd` 正常重载。Zotero 覆盖升级到 0.6.0 后历史问题、回答和页码链接完整保留。
- 2026-08-25 16:32：调整安装器的 Python 运行时发现逻辑；由 macOS 系统 Python 3.9 启动时可自动选中已安装的 Python 3.12，文档命令无需指定小版本。
- 2026-08-25 16:36：首次远端 CI 中 macOS 通过、Windows 的 XPI hash 不一致；定位到 `ZipInfo.create_system` 继承宿主平台，已固定为 Unix ZIP 元数据以实现跨系统可复现构建。
- 2026-08-25 16:38：第二次 CI 表明 zlib Deflate 输出仍存在宿主差异；XPI 内容仅约 1.5 MB，改为 `ZIP_STORED` 消除压缩库差异，确保逐字节跨平台稳定。
- 2026-08-25 16:40：Windows 在无压缩后仍产生不同摘要；CI 改为失败时也上传 XPI，用实际产物对比剩余差异。
- 2026-08-25 16:44：对比失败任务上传的 Windows XPI 与本机 XPI，确认文件内容和 ZIP 元数据一致，仅条目顺序不同；根因是 `Path` 在 Windows 与 POSIX 上的排序规则不同。构建器改为按 XPI 内部 POSIX 路径字符串排序。
- 2026-08-25 16:47：GitHub Actions 运行 `32827311013` 的 Windows 与 macOS job 均通过；确认远端 `main` 未产生新提交，可直接 fast-forward 发布。
- 2026-08-25 16:49：将 `a0f7621` 直接 fast-forward push 到 `main`，未执行 PR 合并操作；GitHub 因 Draft PR 的提交已全部可达而自动将其标记为 merged。`main` push CI 运行 `32827402350` 的双平台 job 均通过。
- 2026-08-25 16:52：最终提交 `68fff2c` 的 `main` CI 运行 `32827520177` 双平台通过；创建并推送 `v0.6.0`，Release workflow `32827594550` 验证并发布 XPI 与 SHA-256 文件成功。

## 总结

### 实际完成内容

- 新增 Apple Silicon/Intel macOS 安装、构建、启动、停止和卸载入口。
- 使用固定 OpenAI Codex App Server Release、官方摘要校验、回环 bridge token 和用户级 `launchd`。
- 保留 Windows 行为，并将测试、release metadata、CI 和文档扩展为跨平台。
- 插件版本升级为 0.6.0。

### 验证结果

- Python、JavaScript、shell、JSON/XML、可复现 XPI 和更新摘要检查通过。
- XPI SHA-256：`6edbc37ddb8bad07d13aadac099905326cc65e44ebe51b30547e613d7c173a9c`。
- macOS 首次安装、重复升级、`launchd` 重载、token 复用、bridge 健康检查、模型读取和真实对话通过。
- Zotero 9.0.6 首次安装、0.5.0 → 0.6.0 覆盖升级、连接、PDF 对话、页码链接和历史保留通过。
- GitHub Actions Windows 与 macOS 双平台验证均通过（分支 run `32827311013`、`main` run `32827402350`）。

### 未完成事项或剩余风险

- Intel Mac 的安装资产选择已实现但缺少 Intel 实机验证；Apple Silicon 本机和 Windows CI 均已验证。
