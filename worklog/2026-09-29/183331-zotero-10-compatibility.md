# Zotero 10 兼容性更新

## 计划

- 目标：让 Windows 和 macOS 版 Paper Chat 可在 Zotero 10.0.4 上安装和运行，同时保留 Zotero 9.0.x 支持。
- 范围：检查 Zotero 10 官方兼容变更及插件使用的 Zotero API；更新插件兼容范围、版本、文档和自动检查；不操作 Zotero、不发布正式版本。
- 关键步骤：核对条目侧栏、PDF Reader、偏好设置、条目/笔记和文件 API；生成跨平台共用 XPI；执行 JavaScript、Python、Shell、生命周期与可复现构建测试。
- 验证方式：运行 `python3 scripts/test.py`、`git diff --check`，并由用户在 Zotero 10.0.4 的 macOS 和 Windows 环境中完成功能检查。

## 实施记录

- Zotero 官方说明：Zotero 10 与 Zotero 9 使用相同的 Firefox 140 ESR；经确认本插件不使用 Zotero 10 中变更的多分类选择、全文索引、Advanced Search、Local API 写入或数据库直读接口。
- 对本机 Zotero 10.0.4 包内实现进行了只读核对，插件依赖的 `ItemPaneManager.registerSection`、Reader 事件、`item-pane-custom-section`、`item-details` 排序等接口仍存在且调用形式兼容。
- 将插件版本更新为 0.6.7，支持范围由 Zotero 9.0.x 扩展到 9.0.x–10.0.x，并同步更新中英文安装及开发文档。
- 用户测试发现新打开 PDF 后首次点击较靠下的插件图标，约一秒后会落入空白区域。根因是 Paper Chat 为强制内容区块置底而全局改写 `item-details.initPaneOrder`，并在 `onInit` 再次移动 DOM；这会使 Zotero 10 在 `scrollToPane()` 中计算的目标位置和临时最小滚动高度失效，因此也会影响其他插件。
- 移除全局排序 monkey patch 和 `onInit` DOM 移动，保留 Zotero 官方支持的 `sidenav.orderable: false` 固定图标位置；内容区块顺序交由 Zotero 管理。
- 按用户反馈将 Paper Chat 外层改为无边框、无圆角、透明背景的原生侧栏布局，并移除各区域多余的横向内边距。模型、推理强度、新对话、历史、笔记和底部操作行在窄侧栏中保持单行，文本过长时使用省略显示。

## 总结

- 已生成可供用户检查的 0.6.7 XPI；macOS 与 Windows 共用同一个插件包，现有两套平台 Bridge 安装脚本无需因 Zotero 10 调整。
- `python3 scripts/test.py` 与 `git diff --check` 均通过，覆盖 JavaScript 语法、Markdown 渲染、Bridge 生命周期、Shell 语法、XHTML、包内容和可复现构建。
- XPI SHA-256：`217a53d313c0c8a729f006ab35b8b0b7431b2bdfa72613a7118b2984ec0b3889`。
- 未按用户要求启动或操作 Zotero；实际 UI、PDF 上下文、笔记、附件、联网及对话功能由用户在 Zotero 10.0.4 上检查。通过后再合并到 `main` 并发布正式版本。
