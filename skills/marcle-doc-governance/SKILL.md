---
name: marcle-doc-governance
description: 创建或维护按所有权分层的项目文档，按影响选择跳过、轻量维护或完整治理；提供通用task与review记录、当前上下文和历史索引规则。不负责长任务调度、返修轮次、角色派遣或提交授权。
---

# Marcle Doc Governance

## 先做最轻量的文档影响判断

- **跳过**：局部修改不改变稳定项目事实、当前交接、任务历史或后续工作时，不写文档。
- **轻量维护**：有实质里程碑但无跨层变化时，更新简短DEV_LOG和必要任务记录；只有当前优先级、约束、决定或下一步改变时才更新AI_CONTEXT。
- **完整治理**：初始化/修复文档体系，或产品、架构、交互、工程规则及长期决定改变时，先定位owner层，再做最小跨层更新。不因一个问题默认扫描全仓文档。

普通改动只读取相关task与必要索引。完整治理前读[doc-system-rules](references/doc-system-rules.md)；创建或实质修改任务时读其中Implementation Task Specification Rules，并按需使用[file-templates](references/file-templates.md)。只创建有用途的文件，不初始化空目录树。

## 文档所有权

| 层 | 内容 |
| --- | --- |
| product | 用户规模、产品目标、功能范围、业务规则 |
| architecture | 模块、数据、接口及所有权边界 |
| design | 用户交互与可见行为 |
| engineering | 开发、测试、打包、部署、运维及已知问题 |
| material | 原始/临时参考，默认不推送，稳定结论另归owner |
| ai | 任务、审查、决定、历史索引和当前交接 |

沿项目已有doc/或docs/约定。一项事实一个主要归属，其他文件引用，不重复详细报告。已有规模与约束定义直接引用，不重新询问用户；本期差异保存在task。

## 通用任务与审查记录

task保存目标、依据、范围、非目标、验收与Coder执行证据。只有并发、持久化、事务、生命周期、多写入者等实际风险才增加强化合同，不为小任务套完整大模板。

review保存审查类型(设计/实现)、受审版本、Reviewer身份、证据及原结论。必要P1/P2采用稳定ID，写触发机制、影响、依据、最小方向和来源分类：设计缺陷、执行遗漏、共同原因、待核实、既存/范围外。来源不明允许待核实，不做角色评分。

Reviewer独立结论由Reviewer维护；Planner的接受、反驳或后置写在独立裁定区，保留理由，不篡改原结论。Coder自审写task，不冒充独立review。普通任务可在task内保留简短review；需要独立多轮记录时用ai/task_review/，一子任务一文件区分设计/实现各轮即可。版本变更后的适用范围须明确，不把旧Approved套到新事实。

## 与执行skill的边界

本skill不启动子agent、不指定审查顺序、不决定返修轮次或阶段推进、不自动提交/推送。长任务执行语义及execution-loop模板由[marcle-goal-excution](../marcle-goal-excution/SKILL.md)拥有；只有用户请求该工作流或明确请求台账时才读取其相关内容。仅加载本文档skill不自动调用执行skill。

execution-loop作为AI工作流记录默认位于ai/tasks/，链接父任务、当前task和review。命名可沿用YYYY-MM-DD_nn_execution-loop.md，编号规则沿项目。本文只管理存放、引用与精简原则，不重复控制字段和调度政策。历史台账无需为skill迁移而批量改名。

## 收敛与交接

- AI_CONTEXT是短小的当前缓存：替换过时状态，保留来源链接，不持续堆积执行流水。
- DEV_LOG是里程碑索引：一次实质结果一段摘要和链接，不复制task/review。
- 详细实施证据在task，独立发现与复审在review，执行控制状态在台账；稳定事实更新对应owner。
- Context Delta只在持久约束、职责或后续工作改变时添加；长期决定写decisions，不仅埋在日志。
- 实现、自动验证、独立审查、人工验收、提交、部署分别表达；未验不写成通过，提案不写成现状。
- UTF-8写入并核对编码与链接。保护无关改动；不为文档整洁擅自删历史、改授权或改产品代码。
