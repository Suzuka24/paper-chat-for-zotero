# Sidenav icon bottom placement

## 计划

- 目标：让 Paper Chat 图标始终位于 Zotero 条目侧栏所有可排序面板图标之后。
- 范围：仅调整 Item Pane section 的 `sidenav` 注册配置，不修改 Zotero DOM 或其他插件。
- 关键步骤：使用 Zotero 原生的不可排序侧栏面板配置；加入配置回归检查；更新版本与发布元数据。
- 验证：确认 Zotero 当前实现会将不可排序面板追加到按钮组末尾；运行语法检查、回归测试、bridge 生命周期测试和可复现 XPI 构建。

## 实施记录

- 2026-08-26 16:08：检查本机 Zotero 9 的 `ItemPaneManager` 与 `item-pane-sidenav` 实现；确认 `sidenav.orderable: false` 会把面板追加到所有可排序面板之后，并禁止拖动重排。
- Paper Chat section 已设置为不可排序，且加入构建时配置检查，防止后续误删该约束。
- 版本更新至 v0.6.4，并同步 changelog 与 Zotero 更新元数据。

## 总结

- Paper Chat 图标现在由 Zotero 原生排序机制固定在所有可排序面板图标之后；不会覆盖用户的其他侧栏顺序偏好。
- 自动验证通过：侧栏配置回归检查、Markdown 渲染测试、6 个 bridge 生命周期测试、JavaScript/Python/shell 语法检查、双次可复现 XPI 构建和更新哈希检查。
- XPI SHA-256：`406c10245a5d94636f0e263f5c08cd91e58ff942a89e11a236230185051ffa25`。
- 未在 Zotero 中覆盖安装本地构建；本地来源软件安装需要单独确认，发布后的正式 Release 可用于升级验证。
