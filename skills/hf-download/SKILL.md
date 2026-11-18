---
name: hf-download
description: 在 Windows 本地可见 PowerShell 或 CMD 窗口中下载 Hugging Face 模型或数据集。处理 Python/HF 环境、按需认证、HF_ENDPOINT 镜像与网络代理、文件筛选和中断后继续下载；适用于提供 HF 链接、仓库 ID 或要求排查 HF 下载失败的请求。
---

# HF Download

将用户的 HF 下载需求转换为当前环境可执行的下载任务，在可见终端中展示原生进度。默认 PowerShell；用户指定 CMD 时使用 CMD。仅分析或准备命令的请求不启动下载。

## 确定目标与环境

- 解析仓库 ID、仓库类型（默认 model）、revision、仓库内完整文件路径或 include/exclude、保存目录。文件链接中的 revision 和路径分别传递，不把整条网页链接当 repo_id。revision 含斜杠或链接含义不清时查仓库确认。
- 根据本次请求、已有目录和上下文补足参数；只有存在影响下载范围的歧义时询问。用户指定单文件时不扩大为全仓库。量化版本不自行替换；Diffusers 目录依据真实仓库结构选择，不固定套用 unet 或 transformer 清单。
- 优先复用工作目录已有 venv。检查 `Get-Command hf -All`、对应 Python 的 huggingface_hub 版本和所选 HF 的 `download --help`。后续使用 HF 可执行文件的绝对路径，避免误用 Hermes 等其他应用的环境。仅在缺依赖时使用所选环境的 `python -m pip install huggingface_hub`，不无条件升级。
- 没有合适环境时在下载工作目录创建 venv。激活不是必要条件，使用解释器和 HF 的绝对路径即可。不要把用户机器路径写入 skill 的默认常量。

## 认证与网络

- 公开仓库不强制登录。私有/gated 仓库优先复用已有登录或继承的 `HF_TOKEN`；需要新登录时，让用户在可见终端使用对应 HF 的 `auth login` 输入凭据。不要读取或展示 token 文件、输出环境变量全集，也不要将真实 token 放进配置、脚本、命令参数或日志。
- gated 模型可能需用户在官网接受协议或申请权限。`auth whoami` 只验证身份，不能证明目标仓库权限或大文件链路正常。手写 token 文件不是默认认证流程；如需定位凭据位置，应遵循 `HF_HOME`/`HF_TOKEN_PATH`。
- `HF_ENDPOINT` 控制 Hub API/镜像地址，`HTTP_PROXY`/`HTTPS_PROXY` 控制代理线路，分别处理。优先本次明确设置，其次继承当前配置；未配置时使用官方默认地址。用户要求镜像但未给地址时可使用 `https://hf-mirror.com`，说明这是第三方服务；不自行把已有凭据切换到未指定的新站点。
- 环境变量在启动 HF/Python 子进程前设置，仅作用于下载进程；不修改系统、用户全局变量或终端 profile。需回到官方时显式指定 `https://huggingface.co`，避免继承镜像。

## 预览与可见执行

1. 使用选定的 HF、相同网络设置和目标参数执行 `hf download ... --dry-run`。核实匹配文件、仓库相对路径、预计下载量以及目标磁盘可用空间。预览会访问网络，但不下载模型正文。零匹配不能作为成功；先修正筛选。用户已明确要求下载且范围清楚时，不再要求重复确认。
2. 为该任务在工作目录外的临时目录创建 JSON 配置，使用 UTF-8。配置键见下方。然后用任意可用 Python 执行本 skill 的 `scripts/visible_download.py`；依赖由配置中指定的 HF 环境提供。
3. 启动器创建独立可见窗口：PowerShell 使用 `-NoExit`，CMD 使用 `/K`。下载继承终端标准输入输出，不重定向、不套日志管道、不隐藏窗口，从而保留原生进度条和 Ctrl+C。普通后台 exec 的输出不满足可见终端要求。
4. 报告运行目录和状态文件。若尚在下载，可向用户交接可见窗口，并明确“已启动，尚未确认完成”；不要为等待大文件而无限阻塞，也不要另起重复下载。用户要求等待完成时，每次有界等待并继续读取状态。
5. `status.json` 的 `completed` 仅表示 HF 退出码为 0。再根据预览清单核对预期文件和可取得的大小；区分实际下载、已有文件复用、失败、取消和未知。存在目录、窗口退出或少数缓存文件都不能证明完整。

配置示例（路径和仓库均由本次任务填写）：

```json
{
  "hf_executable": "D:/downloads/venv/Scripts/hf.exe",
  "repo_id": "owner/repository",
  "repo_type": "model",
  "revision": "main",
  "local_dir": "D:/models/repository",
  "include": ["diffusion_models/example.safetensors"],
  "exclude": [],
  "endpoint": "https://hf-mirror.com",
  "dry_run": false
}
```

必填：`hf_executable`、`repo_id`、`local_dir`，两个本地路径必须为绝对路径。可选：`repo_type`、`revision`、`include`、`exclude`、`endpoint`、`http_proxy`、`https_proxy`、`dry_run`。网络键省略时继承当前环境；代理值为空字符串时清除对应代理。配置不支持 token 或任意附加命令。

```powershell
# 路径均替换为本次任务的绝对路径；使用参数数组/工具结构化参数避免拼接 shell 命令。
& 'D:/downloads/venv/Scripts/python.exe' '<skill-dir>/scripts/visible_download.py' --config '<job.json>' --shell powershell
# 用户指定 CMD 时将 --shell 改为 cmd。
```

启动器打印 `pid`、`run_dir`、`status_file`。窗口下载结束后仍保留；用户可查看结果或关闭。Ctrl+C 尽量记录 cancelled；强制关闭窗口可能留下 running，需结合进程和文件核实，不能直接判成功。Windows 状态文件替换期间偶发读取占用时，短暂重读，不据此判定下载失败。

## 中断和排障

保留已下载文件、`.cache/huggingface` 和未完成数据，以相同目标参数继续。不要默认 force-download、删除目录或自动无限重试。不要加入旧版 `resume_download`、`local_dir_use_symlinks` 参数；根据实际安装版本帮助信息判断兼容性。

发生权限、路径、TLS、Xet、镜像或环境错误时，按需阅读 [references/troubleshooting.md](references/troubleshooting.md)。不要通过关闭 TLS 校验解决下载问题。
