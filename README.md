# Paper Chat for Zotero

[English](README.en.md) · [安装指南](docs/installation.md) · [隐私说明](PRIVACY.md) · [发布记录](CHANGELOG.md)

在 Zotero 阅读器的右侧边栏中，使用本机 Codex 与当前论文对话。插件复用官方 Codex 的 ChatGPT 登录状态，不要求 OpenAI API key，也不消耗 API 账户余额。

> 本项目不是 OpenAI 或 Zotero 的官方产品。它不会授予 Codex 使用资格，也不会绕过订阅限额；请求仍受用户自己的 ChatGPT/Codex 方案、工作区策略和模型可用性约束。

## 使用前提

- Windows 10/11、Zotero 9.0.x、Python 3.10+。
- 用户已在同一 Windows 账户中登录过官方 Codex 桌面客户端或 Codex CLI，且登录仍有效。
- Codex 客户端不需要保持运行；插件会启动独立的官方 Codex App Server，并复用本机认证状态。
- 如果从未登录、已经退出或凭证失效，请先打开 Codex 完成登录，或在 Codex CLI 中运行 `codex login`。

## 主要功能

- 在 Zotero 原生右侧边栏中聊天，界面随 Zotero 的中英文语言自动切换。
- 自动读取当前 PDF，并支持 PDF 选区、标注、条目笔记和本地附件作为上下文。
- 支持粘贴剪贴板图片、PDF、Word、表格、文本及资源管理器中复制的其他文件。
- 动态读取当前账号可用模型，选择推理强度，流式回答并停止生成。
- 按论文保存多条对话，支持新建、切换、重命名和删除。
- 渲染 Markdown、表格、代码块和 KaTeX 公式；页码引用可跳转到 PDF。
- 单条消息或完整对话可复制、新建 Zotero 笔记、追加或更新指定笔记。
- 可拖动调整消息区高度；对长公式、表格和长链接进行侧栏宽度约束。
- 对话使用只读沙箱；本地桥接只监听 `127.0.0.1`，每次安装生成独立随机令牌。

## 安装

下载源码或 Release 源码包，在 PowerShell 中运行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install.ps1
```

脚本会下载并校验经过本项目测试的 OpenAI 官方 Codex App Server、安装本地桥接服务，并生成：

```text
dist\paper-chat-for-zotero.xpi
```

然后在 Zotero 中打开 `工具 → 插件 → 齿轮 → 从文件安装插件`，选择该 XPI，并完整重启 Zotero。升级、无自启动安装和故障排查见[安装指南](docs/installation.md)。

## 使用

1. 在 Zotero 中打开一篇本地 PDF。
2. 点击右侧导航中的 Paper Chat 图标。
3. 选择模型与推理强度，然后提问。
4. 使用“附件”、剪贴板粘贴、PDF 选区或条目笔记补充上下文。
5. 在 `编辑 → 设置 → Paper Chat for Zotero` 中设置默认语言、风格和通用 Prompt。

## 它如何复用 Codex 登录

插件本身不读取、复制或上传登录凭证。Windows 本地桥接启动 OpenAI 官方 `codex-app-server`，由 App Server 读取和刷新当前 Windows 用户已有的 Codex 认证。插件只通过 `account/read`、模型目录和对话接口与 App Server 通信。

因此，“在电脑上使用过 Codex”需要满足两个条件：使用的是同一 Windows 用户，并且登录仍有效。如果账号无 Codex 权限、已退出或组织策略禁止使用，插件也无法连接。

## 隐私与安全

- 当前 PDF 在本地用 `pypdf` 提取文本，再随问题发送给 Codex/OpenAI 处理。
- 附件只在用户主动添加后提供给 Codex；插件不运行自己的云端服务。
- 桥接绑定本机回环地址，使用每次安装独立的 256-bit 随机令牌。
- Codex 线程使用 `approvalPolicy: never` 和只读沙箱，拒绝交互式工具请求。
- 完整的数据流、存储位置和删除方式见 [PRIVACY.md](PRIVACY.md)。

## 当前限制

- 当前安装器仅支持 Windows；macOS/Linux 尚无一键安装脚本。
- 扫描版 PDF 可能需要先 OCR；页码准确度依赖 PDF 文本层。
- 插件不能接管 Codex 客户端里已经打开的任务，只复用同一账号认证和模型目录。
- 首次安装需从 OpenAI 官方 Release 下载约 230 MB 的 App Server。

## 开发与构建

```powershell
.\Build.ps1
```

构建过程可复现，输出位于 `dist/paper-chat-for-zotero.xpi`。贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)，维护者发布流程见 [RELEASING.md](RELEASING.md)。

## 卸载

先在 Zotero 插件管理器中移除插件，再运行：

```powershell
.\Uninstall-Bridge.ps1
```

## 许可与声明

本项目以 [MIT License](LICENSE) 开源。第三方组件见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。OpenAI、ChatGPT、Codex 与 Zotero 均为其各自权利人的商标；本项目与 OpenAI、Zotero 无隶属或背书关系。
