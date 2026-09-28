---
name: database-management
description: >
  数据库管理技能：接收数据任务→澄清需求→回忆经验→规划大纲→分析分支/引擎→写脚本/迁移→构建测试→
  知识库构建→浏览器学习→审查→交付；薄技能（能力经 dependence/ 声明），遇不明处强制派 file_ops 联网学习并沉淀知识链。
license: MIT
metadata:
  category: development
---

# database-management

使用 `database-management` skill 来完成用户请求。

## 工作原则

1. **按流程执行**：不跳步、不静默越权；决策节点留逻辑链。
2. **双链辩论**：审查节点运行正反双链（logic_chain.py debate）。
3. **返回机制**：审查失败记中断（process_chain.py interrupt），修复后 resume；任一路径完成＝收口返回调度方整合续排。
4. **惩罚熔断**：重试达 10 次即熔断，强制回退或求助用户。
5. **垃圾回收**：tmp 收尾后释放到目标 skill 并删除；未指定目录时固定路径沙盒作业。
6. **薄技能**：本体不内嵌他技能内容，能力经 [dependence/](dependence/dependence.md) 声明。

## 执行路径

**创建路径**：初始化→需求确认→经验查询→大纲构建→分支分析→脚本构建→构建测试→知识库构建→浏览器学习→约束编写→整体审查→收尾→**完成**
**修改路径**：初始化→修改流程→**完成**

> 浏览器学习为横切节点：任一步遇到不明 API/引擎/报错即触发，学完沉淀知识链再回原节点。

## 可用工具（scripts/）

check_links / logic_chain / process_chain / garbage_collect / context_compress / penalty / sandbox /
deps_check / run_tests / lint_check / browser_learn / knowledge_fetch / knowledge_convert /
scaffold_project / self_update / flowchart_helper + 领域：schema_migrate / sql_lint / slow_query_check / backup_verify

## 红线

- 不得跳过初始化（含 MIT `LICENSE`，已有不覆盖）；不得静默写盘（默认 `--dry-run`）；不得删除 resistance/ 约束。
- 悬空链接必须为 0；所有 .md / 脚本 ≤ 50 行；缓存文件不得写入 skill 目录（落用户缓存目录）。
- 文件夹名=流程名；脚本英文名称；SKILL.md 必含 YAML frontmatter；agent/ 四格式提示词一句话。
- 遇不明必派 file_ops 联网学习（见 [浏览器学习约束](resistance/浏览器学习约束/浏览器学习约束.md)），禁止臆造 SQL/引擎行为。
- 破坏性 DDL（DROP/TRUNCATE/无默认值加 NOT NULL/改类型）须审批 + 回滚预案，见 [迁移安全约束](resistance/迁移安全约束/迁移安全约束.md)。
- 数据完整性（主外键/唯一/检查/非空）不得为省事而放宽，见 [数据完整性约束](resistance/数据完整性约束/数据完整性约束.md)。
- Git 工作流：每步功能分支提交→审核通过合 dev→整体审查通过 dev 合 main（推送前须用户确认）。

## 详细流程

- 流程节点：[branch/流程/](branch/流程/流程.md)；约束兜底：[resistance/](resistance/resistance.md)
