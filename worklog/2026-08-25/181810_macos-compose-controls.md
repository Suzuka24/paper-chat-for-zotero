# macOS compose controls

## 计划

- 目标：修复 macOS Zotero 中“备份笔记”和“附件”按钮边缘被裁切的问题。
- 范围：仅调整输入区和通用按钮的 CSS，保持 Windows 行为与现有布局结构不变。
- 步骤：关闭 macOS 原生按钮外观造成的边缘溢出，给工具栏保留绘制空间并防止输入区被 flex 压缩；构建后在 Zotero 实机检查。
- 验证：语法检查、可复现构建、macOS Zotero 截图检查，以及 Windows/macOS CI。

## 实施记录

- 2026-08-25 18:18：建立分支 `fix/macos-compose-controls`。
- 为输入区设置不可压缩的 flex 尺寸，增加左右/底部安全内边距，并允许工具栏边缘可见。
- 为 `.zcc-button` 关闭 macOS 原生按钮 appearance，使边框和圆角严格绘制在 CSS box 内；工具栏按钮禁止收缩。
- 版本更新为 v0.6.2，并更新 changelog 与 Zotero 更新元数据。

## 总结

- 自动验证：6 个 bridge 生命周期测试、JavaScript/Python/shell 语法检查、双次可复现 XPI 构建和 update hash 检查全部通过。
- macOS Zotero 实机验证：重新安装 XPI 并完整重启后，“备份笔记”“附件”按钮四边边框和圆角完整可见，按钮底部与面板边缘间距正常；状态和“发送”按钮布局未回归。
- XPI SHA-256：`cbe8fcb28030996f7d9a6ad80ff0ea241287a5e8220cf5f3e3ad04731557bf00`。
