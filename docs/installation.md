# 安装、升级与故障排查

## 1. 前置条件

1. 在 Windows 10/11 或 macOS 上安装 Zotero 9.0.x 和 Python 3.10+。
2. 使用同一系统用户登录官方 Codex 桌面客户端，或安装 Codex CLI 后运行 `codex login`。
3. 确认该 ChatGPT 账号或工作区可以使用 Codex。插件不会提供额外权限，也不使用 API key。

Codex 客户端只需完成一次登录，不需要在使用插件时保持打开。登录过并不代表永久有效：退出账号、凭证过期或组织策略变化后，需要重新登录。

## 2. 安装

解压 Release 源码包并进入项目目录，然后根据系统运行安装器。

### Windows

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install.ps1
```

### macOS

```bash
python3 Install-macOS.py
```

安装器会：

- 下载固定且经过测试的 OpenAI 官方 Codex App Server 版本；
- 强制校验 GitHub Release 提供的 SHA-256；
- 将桥接服务安装到 Windows 的 `%LOCALAPPDATA%\PaperChatForZotero` 或 macOS 的 `~/Library/Application Support/PaperChatForZotero`；
- 生成独立的 256-bit 随机本地令牌；
- 创建 Windows 登录自启动快捷方式或 macOS 用户级 `launchd` 服务；
- 构建 `dist/paper-chat-for-zotero.xpi`。

在 Zotero 中选择 `工具 → 插件 → 齿轮 → 从文件安装插件`，选择上述 XPI，然后完全退出并重新打开 Zotero。

不希望桥接服务登录后自动启动时，Windows 使用：

```powershell
.\Install.ps1 -NoAutoStart
```

macOS 使用：

```bash
python3 Install-macOS.py --no-auto-start
```

## 3. 升级

1. 关闭 Zotero。
2. 用新版源码重新运行 `Install.ps1` 或 `python3 Install-macOS.py`。
3. 在 Zotero 插件管理器中从文件安装新的 XPI，确认覆盖升级。
4. 完整重启 Zotero。

`0.4.x` 开发版的插件 ID 与公开版不同。首次升级到 `0.5.0` 时，请先在插件管理器移除旧开发版，再安装新 XPI。原有偏好键和对话数据目录仍保留，可继续读取；新的 Codex 对话项目目录名为 `Paper Chat for Zotero`。

## 4. 手动控制桥接

```powershell
& "$env:LOCALAPPDATA\PaperChatForZotero\Start-Bridge.ps1"
& "$env:LOCALAPPDATA\PaperChatForZotero\Stop-Bridge.ps1"
& "$env:LOCALAPPDATA\PaperChatForZotero\Start-Bridge.ps1" -Foreground
```

前台模式会把诊断信息显示在终端。日志位于：

```text
%LOCALAPPDATA%\PaperChatForZotero\bridge.log
```

macOS：

```bash
"$HOME/Library/Application Support/PaperChatForZotero/Start-Bridge.sh"
"$HOME/Library/Application Support/PaperChatForZotero/Stop-Bridge.sh"
"$HOME/Library/Application Support/PaperChatForZotero/Start-Bridge.sh" --foreground
```

macOS 日志位于 `~/Library/Application Support/PaperChatForZotero/bridge.log`。

## 5. 常见问题

### 显示“Codex 未连接”

- 运行当前系统对应的 `Start-Bridge.ps1` 或 `Start-Bridge.sh`。
- 检查 `bridge.log`。
- 确认本机 `127.0.0.1:23120` 没有被其他程序占用。
- 重新运行 `Install.ps1`，确保插件读取到与桥接一致的本地令牌。

### 账号或模型列表为空

打开官方 Codex 客户端重新登录，或运行 `codex login`。插件不能使用普通 ChatGPT 网页 Cookie，也不能代替用户开通 Codex 权限。

### PDF 回答缺少正文信息

确认 PDF 已下载到本地并包含可提取文本层。扫描件先在 Zotero 或其他工具中执行 OCR。

### 插件没有出现在侧栏

确认 Zotero 版本为 9.0.x，插件已启用，并在安装/升级后完整重启 Zotero。仍有问题时，从 `帮助 → 调试输出记录` 获取错误并按 [SUPPORT.md](../SUPPORT.md) 提交。

## 6. 卸载

在 Zotero 插件管理器中移除插件，然后运行：

```powershell
.\Uninstall-Bridge.ps1
```

macOS 运行：

```bash
./Uninstall-Bridge.sh
```

该脚本删除新旧桥接安装目录和自启动快捷方式，不删除 Zotero 条目、笔记或插件保存的历史对话。历史数据位置见 [PRIVACY.md](../PRIVACY.md)。
