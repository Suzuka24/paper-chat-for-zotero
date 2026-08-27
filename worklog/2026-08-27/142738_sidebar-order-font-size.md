# 侧栏内容顺序与字体大小设置

## 计划

- 目标：使 Paper Chat 的侧栏图标和内容区都固定在其他可排序插件之后，并在插件设置中提供字体大小调节。
- 范围：Zotero 条目侧栏注册与排序兼容逻辑、Paper Chat 面板样式、插件设置页、默认偏好及相关测试。
- 关键步骤：同步调整内容节点顺序；新增 11–20 px 字体滑块；监听偏好变化并实时刷新已打开面板；执行语法、单元、生命周期与可复现构建检查。
- 验证方式：运行 `python3 scripts/test.py`，并检查最终差异及构建产物。

## 实施记录

- 已确认 Zotero 的侧栏图标排序与内容节点排序相互独立，单独设置 `sidenav.orderable: false` 不会改变内容节点顺序。
- 实机调试发现 Zotero 会为注册后的内容区 ID 添加插件命名空间；排序逻辑已改为识别真实注册 ID及其稳定后缀。
- 字体滑块已在设置页正常显示和保存；实机检查后补充了完整偏好键监听所需的全局标记，使已打开面板可实时响应。

## 总结

- Paper Chat 的侧栏图标保持在翻译图标之后，内容节点也会在 Zotero 每次重建顺序后同步移到最下方。
- 设置页新增 11–20 px 的“界面字体大小”滑块，默认 13 px，修改后自动保存并实时更新已打开的 Paper Chat 面板。
- 版本更新为 `0.6.5`，生成的 XPI SHA-256 为 `8d2a2277bbf795f925b3d39136a31c29bddb6415e10c95d8d686feb3acaa7bd4`。
- 实机验证：Zotero 9.0.17 macOS 中内容顺序为“翻译 → Paper Chat”；已打开面板从 17 px 调到 16 px 后计算样式即时变为 16 px；验证结束后恢复默认 13 px。
- 自动验证：`python3 scripts/test.py` 全部通过，包括 JavaScript 语法与单元测试、Python 编译、Shell 语法、bridge 生命周期测试、XHTML 解析和两次可复现构建。
- 未完成事项：尚未提交或推送 GitHub，也尚未创建 `v0.6.5` Release。

## 补充计划：联网检索设置

- 目标：让用户可在 Zotero 插件设置中选择实时联网、缓存检索或关闭检索，并默认启用实时联网。
- 范围：插件偏好界面、聊天请求参数、Bridge 的 App Server 线程配置和相关测试；继续保持本地文件只读。
- 关键步骤：新增 `webSearchMode` 偏好；随每次聊天发送模式；在 `thread/start` / `thread/resume` 中传入 `config.web_search`；验证三种模式、历史会话恢复和构建。
- 验证方式：运行 Bridge 生命周期测试与完整 `python3 scripts/test.py`，并检查最终差异。

## 联网检索实施记录

- 设置页已提供“实时联网 / 仅使用缓存索引 / 关闭联网检索”三种模式，默认实时联网；模式会随聊天请求进入 App Server 的线程级 `config.web_search`。
- 首次实机测试确认配置传递成功，但发现独立 App Server 的实时搜索依赖同版本 `codex-code-mode-host`；安装器原先仅部署 App Server，导致搜索工具启动失败。
- Windows 与 macOS 安装器已补充 Code Mode Host 的官方发布资产下载、SHA-256 校验和本地部署，且继续禁止将二进制打入 XPI。
- macOS 实机已安装并启动同版本 Code Mode Host；临时 Bridge 会话成功通过实时搜索返回 OpenAI 官方 `Codex App Server` 页面，随后已永久删除该测试会话。

## 联网检索总结

- 已完成三档联网设置及中英文界面，默认“实时联网（推荐）”，切换后从下一次提问生效。
- Bridge 对新建和恢复的会话应用 `config.web_search`，现有 Zotero 对话及 Codex thread ID 不变，不会丢失历史。
- Windows/macOS 安装器均会安装并校验实时搜索所需的同版本 Code Mode Host；macOS 实机联网测试通过。
- `python3 scripts/test.py` 全部通过；`0.6.5` 可复现 XPI SHA-256 为 `65ca06929e87b40c9c412515a37525e701d771b14d331436cda5eea0a7d1d389`。
- 发布事项：本次改动将提交到 `main` 并发布为 `v0.6.5`；远端结果需在 GitHub Actions 完成后核验。
