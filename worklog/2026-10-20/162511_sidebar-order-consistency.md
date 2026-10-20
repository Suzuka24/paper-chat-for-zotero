# Sidebar order consistency

## 计划

- 目标：使 Paper Chat 与 Translate for Zotero 的侧栏图标顺序和内容区块顺序保持一致。
- 范围：仅调整 Paper Chat 的条目侧栏排序行为及相关回归测试，不修改会话、Bridge 或文库数据。
- 关键步骤：移除内容区块的独立固定排序；以实时侧栏图标顺序为唯一来源同步所有内容区块的 CSS 视觉顺序；监听插件增删与重排；不移动 DOM；构建并执行自动测试。
- 验证方式：运行 `python3 scripts/test.py`、`git diff --check`，并在 Zotero 中分别点击 Translate 与 Paper Chat 图标检查定位及顺序。

## 实施记录

- 确认不一致由 Paper Chat 内容区块的 `style.order` 引起：图标按 Zotero 插件注册顺序排列，内容却被单独强制到末尾。
- 移除 `placeSectionVisuallyLast()` 的固定置底逻辑。
- 新增侧栏顺序监听器，将每个图标的实时索引映射为对应内容区块的 CSS `order`；插件更新、启用/禁用或加载时序改变后会自动重算。
- 监听器只改变视觉顺序，不调用 Zotero 的运行时区块重排方法，不移动 DOM；卸载或窗口关闭时恢复样式并释放观察器。
- 更新回归测试，要求动态监听侧栏变化并禁止重新引入固定末位编号。

## 总结

- 已生成 0.6.8 XPI，SHA-256 为 `c179d6ee91ad03a5ba5d9d4e7fb46e106cb00dc9eff0f420bf0b858ccd3314ae`。
- `node --check plugin/content/main.js`、`python3 scripts/test.py` 与 `git diff --check` 均通过。
- 已覆盖安装到本机 Zotero；插件管理器显示版本 `0.6.8`，已安装 XPI 与构建产物 SHA-256 完全一致。
- 当前图标顺序为 Translate 在上、Paper Chat 在下；分别点击两个图标均能直接定位到对应内容，没有出现空白区或二次滚动，内容视觉顺序与图标顺序一致。
- 插件后续重新注册导致顺序变化时由 `MutationObserver` 自动重算；未额外改变 Zotero 或其他插件的持久排序数据。
- 已将发布版本定为 `0.6.8`，准备合并至 `main`、推送标签并通过 GitHub Actions 发布 XPI 与校验文件。
