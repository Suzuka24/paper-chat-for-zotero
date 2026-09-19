# 流式回复期间 Zotero 界面卡顿

## 计划

- 目标：修复 Paper Chat 收到 Codex 流式回复时 Zotero 主界面卡顿的问题。
- 范围：仅调整聊天消息的流式预览与结束时排版，不改变 Bridge、会话存储或最终回答内容。
- 关键步骤：把每个 delta 都重建完整 Markdown/公式/页码链接的逻辑改为合并增量纯文本预览；回复结束或停止时只完整渲染一次。
- 验证方式：新增高频 delta 单元测试；运行跨平台完整测试与可复现打包；尽可能进行 Zotero 实机验证。

## 实施记录

- 代码审查发现每个 `delta` 都调用 `setMarkdown(answer, markdown)`，随回答增长重复执行完整 Markdown 解析、DOM 重建、KaTeX 排版、页码链接扫描和同步滚动。Bridge 在独立进程解析 PDF，不是主要的 Zotero 主线程阻塞点。
- 实现了按 100 ms 合并的纯文本预览：新片段只追加到同一个文本节点，已收到的完整源码仍可供复制与停止操作使用。正常完成或中止时才一次性执行原有 Markdown、公式和页码链接渲染。
- 增加 5,000 个高频 delta 的测试，检查预览更新次数、最终排版与取消定时器行为。

## 总结

- 已把流式阶段的重复完整排版改为 100 ms 合并更新的轻量纯文本预览；回答结束或停止时仍使用原有完整排版，保存的会话文本格式未变化。
- `node scripts/test_markdown_renderer.js`、`node --check plugin/content/main.js`、`python3 scripts/test.py` 和 `git diff --check` 均通过；跨平台构建的 XPI SHA-256 为 `9683c15892b5e5f60f5fb928adb73f9be477077012ce3cc04a0ef52a5c5a7687`。
- 剩余风险：当前自动测试覆盖高频增量及完成/取消路径，未模拟用户文库中的长时间真实 Codex 回复；升级后可用长回复再次确认交互流畅度。
