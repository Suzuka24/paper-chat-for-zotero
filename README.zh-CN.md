# Paper Chat for Zotero

[English](README.md) · [安装指南](docs/installation.md) · [使用指南](docs/usage.md) · [最新版本](https://github.com/Suzuka24/paper-chat-for-zotero/releases/latest)

在 Zotero 原生右侧边栏中，使用本机 Codex 与当前论文对话。插件复用本机 Codex 登录，不需要 OpenAI API key 或 API 余额。

> **首次安装提示：** 仅安装 XPI 无法使用。请先下载源码包并运行 Windows 或 macOS 安装器以安装本地 bridge，再在 Zotero 中安装生成的 XPI。详见[快速安装](#快速安装)。

![Zotero PDF 阅读器中的 Paper Chat for Zotero](docs/assets/paper-chat-for-zotero.png)

## 主要功能

- 将当前 PDF、选区、标注、Zotero 条目笔记和本地附件作为上下文。
- 支持账号可用模型、推理强度、流式回答和持久化多对话。
- 支持检索论文之外的实时网页资料，并可在设置中改为缓存检索或完全关闭。
- 回答完成后自动归档插件管理的 Codex 任务，在保留续聊上下文的同时避免占满“最近”列表。
- 渲染 Markdown、表格、代码和 KaTeX 公式，页码引用可跳转到 PDF。
- 单条消息和完整对话可复制或保存到 Zotero 笔记。
- 界面跟随 Zotero 自动切换中文或英文。

## 快速安装

需要 Windows 10/11 或 macOS、Zotero 9.0.x、Python 3.10+，并在同一系统账户中登录过官方 Codex 客户端或 Codex CLI。

1. 下载并解压[最新版本源码](https://github.com/Suzuka24/paper-chat-for-zotero/releases/latest)，或克隆本仓库。
2. 根据系统运行安装器。

   Windows PowerShell：

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\Install.ps1
   ```

   macOS 终端：

   ```bash
   python3 Install-macOS.py
   ```

3. 在 Zotero 中选择 `工具 → 插件 → 齿轮 → 从文件安装插件`，安装 `dist/paper-chat-for-zotero.xpi`。
4. 完整重启 Zotero，并打开一篇本地 PDF。

完成登录后，Codex 客户端不需要保持运行。实际使用仍受用户自己的 ChatGPT/Codex 方案、工作区策略和限额约束。

## 文档

- [详细安装、升级与故障排查](docs/installation.md)
- [完整使用指南](docs/usage.md)
- [隐私与本地数据存储](PRIVACY.md)
- [问题反馈](SUPPORT.md)
- [版本记录](CHANGELOG.md)
- [贡献与发布流程](CONTRIBUTING.md)

## 许可

本项目采用 [MIT License](LICENSE)，与 OpenAI、Zotero 无隶属或背书关系。OpenAI、ChatGPT、Codex 与 Zotero 均为其各自权利人的商标。
