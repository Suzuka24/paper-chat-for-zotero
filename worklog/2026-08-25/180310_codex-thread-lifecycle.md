# Codex thread lifecycle

## 计划

- 目标：避免 Paper Chat for Zotero 的会话长期出现在 Codex 桌面的“最近”列表，同时保留 Zotero 本地消息与 Codex 上下文。
- 范围：桥接服务的 Codex thread 来源与归档生命周期、旧会话迁移和备份、删除同步、版本与文档、自动化及实机验证。
- 关键步骤：
  1. 新建 thread 改用 App Server 来源；已有归档 thread 在继续提问时自动恢复。
  2. 每轮完成后自动归档；插件首次升级时按本地保存的 thread ID 精确归档旧会话。
  3. 迁移前在 Zotero 数据目录生成一次性历史备份；删除 Zotero 对话时同步永久删除对应 Codex thread。
  4. 增加生命周期测试，构建 XPI，并在本机 Zotero/Codex 中验证历史保留、续聊和“最近”列表行为。
- 验证方式：运行语法检查、生命周期单元测试、可复现构建与元数据校验；安装到本机后核对备份、原有消息数量、续聊结果和 Codex UI。

## 实施记录

- 2026-08-25 18:03：建立分支 `fix/codex-thread-lifecycle`，开始实施。
- 将 App Server 启动来源由 `vscode` 改为 `app-server`；新增归档、恢复、批量迁移和删除接口。
- 每轮 `turn/completed` 后自动归档 thread；继续旧会话时先尝试恢复，归档操作支持重复执行和已不存在的历史 thread。
- 插件首次迁移前一次性备份 `conversations.json`，迁移全部成功后写入 `threadLifecycleVersion: 1`；删除对话时先删除 Codex thread，失败则保留 Zotero 对话。
- 实机发现并修复 macOS `NS_ERROR_FILE_NOT_FOUND` 错误文本兼容，以及 Zotero 热重载场景下迁移标记未经过普通写队列落盘的问题。
- 新增 6 个 bridge 生命周期测试，并将其纳入 `scripts/test.py`。
- 更新中英文 README、安装/使用文档、隐私说明、版本记录和 Zotero 更新元数据。

## 总结

- 实际完成：v0.6.1 的 thread 生命周期、旧数据安全迁移、删除同步、文档与发布元数据均已完成。
- 自动验证：JavaScript/Python/shell 语法检查、6 个生命周期测试、双次可复现 XPI 构建、manifest/update hash 一致性全部通过。
- 实机验证：
  - 迁移前后均为 62 篇论文、63 个对话、36 个 thread；原 118 条消息无丢失。
  - 自动备份与迁移前人工备份 SHA-256 均为 `fd647a84673116aea08baa2c102e577f095ea01ebfed9bb4e1f6ccdc910601f3`。
  - 已有对话续聊成功，消息数由 2 增至 4；完成后 rollout 位于 `~/.codex/archived_sessions/`，活跃目录无该 thread。
  - 新建一次性测试 thread 的来源为 App Server 内部兼容值 `mcp`，完成后自动归档，随后通过删除接口清理成功。
  - Codex 最近 50 项中不再包含迁移的论文会话；此前的 macOS smoke test 任务也已归档。
- 最终 XPI SHA-256：`a8bd7b826c657a33ea37866e3d91a3a39baecb685c6268f69812ffdb28ca6849`。
- 剩余风险：Codex 桌面端当前正打开某个旧 thread 时，归档会提示稍后重试；关闭或切走该任务后插件会在下一次连接时继续，不会写迁移完成标记或删除 Zotero 数据。
