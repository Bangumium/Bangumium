
# Bangumium

Bangumium 是一个 [bgm.tv](https://bgm.tv/) 的桌面客户端，支持 Windows、Linux 和 macOS 平台。

目前实现的功能还比较初级，如有不足之处望多多包涵（

## 架构

Pywebview + Vue.js

## 特点

* 多平台支持（Windows/macOS/Linux）
* 桌面通知集成（目前仅支持好友时间线）

## 目前实现的功能

* 好友时间线（使用`bs4`解析html实现，部分情况下可能会出错）
* 好友有新动态时发送桌面通知
* 动画收视进度管理、书籍阅读进度管理
* 条目搜索（但目前还不支持筛选条件）
* 条目详情（但目前还不支持评论、讨论版、吐槽箱功能）
* 修改收藏
* 用户主页（目前只支持基本信息和收藏条目的简单显示）

## 软件下载

在 [GitHub Releases](https://github.com/Bangumium/Bangumium/releases) 下载编译完成的软件。

**Windows 用户可能需要自行前往 [此处](https://developer.microsoft.com/en-us/microsoft-edge/webview2) 下载 Microsoft Edge Webview2 运行时才可以正常运行。**

如果你使用 Arch Linux，可以使用 AUR 中的 `bangumium-bin` 包直接安装本软件。

## 参与开发

### 安装 NPM 和 PIP 依赖

在项目根目录执行 `pip install -r requirements.txt` 或 `pip install -r requirements_linux.txt` 以安装 Python 依赖。

在`frontend/`执行`npm install`安装 npm 依赖。

### 启动开发环境

```
./dev.sh
```

### 生成可执行文件

在 Linux & macOS 下使用`./build.sh`，在 Windows 下使用 `./build_win.sh`.

注：在 Windows 下需要使用 bash 作为脚本解释环境，可选项包括 Git Bash. 同时在 Windows 下构建时需要保证 CWD (Current Working Dir) 为项目根目录。

## 参与贡献

欢迎提出 PR / Issues.

在 PR 被接受之后，你的名字会被添加到下个版本中的软件“设置-关于”界面中（如果不需要的话告知即可）。

## 许可证

本软件的源代码使用 MIT 协议开源。本程序不含任何担保。

`icon.png` 修改自 `https://bgm.tv/img/ico/ico_ios.png`，这个图标的版权归 `bgm.tv` 所有。
