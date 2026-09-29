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
- 将 Translate for Zotero v2.4.7 源码作为未跟踪参考资料放入 `ref/`，并将 `ref/` 加入 `.gitignore`；参考其使用原生控件、面板行距 6px、行内间距 4px 的设计原则，统一收紧 Paper Chat 的下拉框、按钮和顶部控制区，笔记“刷新”改为纯文字按钮。
- 将 Windows/macOS 安装器默认 Codex App Server 从 0.149.1 更新到官方稳定版 0.157.1，并在已安装版本不匹配时自动替换，使模型选择器继续直接跟随 App Server 的账号可用模型目录。
- 在临时目录启动 0.157.1 App Server 验证 `model/list`，确认返回 GPT-6 Astra、GPT-6 Sol、GPT-6 Luna、GPT-5.6 Sol、GPT-5.6 Terra、GPT-5.6 Luna 和 GPT-5.5，与当前 Codex 客户端可选模型一致。
- 经用户确认后完成本机安装：使用已校验的官方 0.157.1 二进制升级并重启 macOS Bridge，通过 Zotero 插件管理器覆盖安装新 XPI；安装目录与构建产物 SHA-256 一致，Bridge launch agent 处于 running 状态。
- 用户复查发现 HTML 控件即便调整 CSS 后仍与 Translate 的原生外观不同，并且侧栏图标与内容区顺序不一致。将模型、推理强度、历史、笔记等下拉框迁移为 Translate 同款的原生 XUL `menulist`，将所有文字操作迁移为原生 XUL `button`；初始化区块时读取侧栏实际图标顺序，并调用 Zotero 自带 `initPaneOrder()` 对齐内容顺序，不恢复全局 monkey patch。
- 进一步确认 Zotero 会将插件注册的短 pane ID 自动扩展为带插件 ID 的完整 ID；此前用短 ID 比较导致顺序修复未命中。现改为识别完整 ID/后缀，并使用 Zotero 自带 `initPaneOrder()` 与 `changePaneOrder()` 将 Chat 内容稳定放在 Translate 内容之后。
- 再次覆盖安装最终 XPI，并通过 Zotero 可访问性树核验：Translate 标题及内容位于 Paper Chat 之前；展开 Paper Chat 后，模型、推理强度、会话、笔记目标均显示为原生组合框，刷新、新对话、重命名、备份笔记、附件和发送均显示为原生按钮。
- 用户复测发现点击侧栏图标仍可能无法定位。进一步核对 Zotero 10 的 `scrollToPane()` 后确认，即使调用官方 `initPaneOrder()`/`changePaneOrder()`，在区块初始化完成后移动 DOM 节点仍会使点击时的 pane 顺序、位置与临时滚动高度不一致。现彻底移除所有区块 DOM 重排，只给 Paper Chat 区块设置 flex `order` 使其在视觉上置底；Zotero 的原始 DOM、滚动定位和懒加载顺序不再被插件修改。
- 覆盖安装该修复后进行实机回归：从 Translate 图标切换到 Paper Chat、再切回 Translate、再次进入 Paper Chat，均直接定位到对应区块，没有出现空白区域；全程未发送聊天或修改文库数据。

## 总结

- 已生成可供用户检查的 0.6.7 XPI；macOS 与 Windows 共用同一个插件包，现有两套平台 Bridge 安装脚本无需因 Zotero 10 调整。
- `python3 scripts/test.py` 与 `git diff --check` 均通过，覆盖 JavaScript 语法、Markdown 渲染、Bridge 生命周期、Shell 语法、XHTML、包内容和可复现构建。
- 最新 XPI SHA-256：`af47094fcd4b59f6f240de79d1e33674fbe2c142ef115c6767d0eb2f0a7597a6`；Zotero 配置目录内已安装 XPI 的校验值相同。
- 本机已安装的 Codex App Server 为 0.157.1，`/models` 已返回与当前 Codex 客户端一致的 7 个可选模型。
- 已仅对 Zotero 侧栏布局与控件类型进行只读 UI 核验，未发送消息或改动文库数据；PDF 上下文、笔记、附件、联网及对话功能仍由用户在 Zotero 10.0.4 上检查。通过后再合并到 `main` 并发布正式版本。
- 针对侧栏点击定位的第二次修复已通过静态检查、自动测试和 Zotero UI 切换回归验证。
