# 按失败阶段排查

| 现象 | 先检查 | 处理边界 |
| --- | --- | --- |
| hf 不存在、导入失败、参数不支持 | HF 的完整路径、配套 Python、包版本、命令帮助 | 修复选定环境；不向另一个 Python 随意装包 |
| 401/403、Repository not found | ID、repo_type、身份及目标仓库权限 | 404 也可能隐藏私有仓库；不要直接判仓库不存在。网页接受协议/申请权限由用户完成 |
| No files matched、预览零匹配 | 远端真实文件树、revision、完整相对路径 | 不猜路径、不下载全仓库绕过筛选 |
| TLS EOF、连接超时 | 镜像 API 与文件重定向目的地、代理是否适用于该进程 | 首页 200 不能证明大文件传输；保留错误类型但避免输出带签名的下载 URL |
| Xet/CAS 传输失败 | 实际 hub/hf-xet 版本、代理/证书/目标主机链路 | `HF_HUB_DISABLE_XET=1` 是版本相关的诊断选项，不是通用默认；先核对实际版本官方文档。若需设置，在启动器父进程中设置，使新窗口继承 |
| 下载读取超时 | 下载链路与当前超时配置 | 可按证据增大 `HF_HUB_DOWNLOAD_TIMEOUT`；重试一次观察，不无限循环 |
| Local entry not found、Incomplete snapshot | 前面的网络/权限错误、未完成缓存 | 不能仅凭该消息判远端文件不存在；保留已有数据继续 |
| 磁盘不足 | 目标盘和 HF/Xet 缓存盘可用空间 | 报告需求与余量，不自动删除用户文件 |
| 窗口消失或状态长期 running | 启动 PID、状态时间、任务文件和原终端 | 强制关闭可能来不及写状态；记为未知/中断，确认无活动下载后再继续 |

认证故障时不把 token 明文写进临时文件以绕过问题。网络配置变化只在本次下载进程生效。修改已记录任务的 endpoint、代理或文件范围前，说明变化；没有新证据不反复更换线路。

官方参考（命令语法仍以当前安装版本为准）：

- [CLI 和认证](https://huggingface.co/docs/huggingface_hub/en/guides/cli)
- [下载、筛选、本地目录与 dry-run](https://huggingface.co/docs/huggingface_hub/en/guides/download)
- [环境变量](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables)
- [Gated 模型访问](https://huggingface.co/docs/hub/models-gated)
