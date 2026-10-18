---
name: database-management
version: 0.1.0
description: >
  数据库管理技能：接收数据任务→澄清需求→回忆经验→规划大纲→分析分支/引擎→写脚本/迁移→构建测试→
  知识库构建→浏览器学习→审查→交付；薄技能（能力经 dependence/ 声明），遇不明处强制派 file_ops 联网学习并沉淀知识链。
license: MIT
metadata:
  category: development
scope: >
  本技能专注于关系型数据库的全生命周期管理，覆盖建模、迁移、查询优化、备份恢复与性能调优；
  支持 PostgreSQL / MySQL / SQLite / MongoDB 等主流引擎；
  不包含数据库代理服务、集群管理、云托管平台操作等非核心领域。
---

# database-management

使用 `database-management` skill 来完成用户请求。

## Scope（范围声明）

详见 [Scope.md](Scope.md)。

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
- 悬空链接必须为 0；所有 .md ≤ 50 行（50 行红线只约束 markdown 文本；脚本 .py/.ps1/.sh/.cmd 不限行数，但仍禁裸 except、print 调试残留、>100 字符长行、超长函数）；缓存文件不得写入 skill 目录（落用户缓存目录）。
- 文件夹名=流程名；脚本英文名称；SKILL.md 必含 YAML frontmatter；agent/ 四格式提示词一句话。
- 遇不明必派 file_ops 联网学习（见 [浏览器学习约束](resistance/浏览器学习约束/浏览器学习约束.md)），禁止臆造 SQL/引擎行为。
- 破坏性 DDL（DROP/TRUNCATE/无默认值加 NOT NULL/改类型）须审批 + 回滚预案，见 [迁移安全约束](resistance/迁移安全约束/迁移安全约束.md)。
- 数据完整性（主外键/唯一/检查/非空）不得为省事而放宽，见 [数据完整性约束](resistance/数据完整性约束/数据完整性约束.md)。
- Git 工作流：每步功能分支提交→审核通过合 dev→整体审查通过 dev 合 main（推送前须用户确认）。

- **变更日志规范**：每次修改/新增/删除操作完成后，必须在根目录 `CHANGELOG.md` 记录变更（日期、改动范围、涉及文件、违反后果）；`CHANGELOG.md` 本身也是变更产物，写入时需同步更新本条规范（本条除外）；变更日志不可缺失、不可跳过、不可事后补录（漏记视为违规）。
## 详细流程

- 流程节点：[branch/流程/](branch/流程/流程.md)；约束兜底：[resistance/](resistance/resistance.md)

## 红线17·批23 对等对话（不得删除）

红线17·批23 对等对话——你与派发方对话是相互独立的对等对话（无主次），不是从属或执行关系：

1. 互为监视者·指导者·训诫者：发现派发方指令与本技能红线/安全边界冲突时，以本技能 SKILL.md 为准并在结果中明说，不盲目照办、也不越权扩展。
2. 收口＝形式停止而非实质完成：本消息结束即收口本侧对话，但派发方任务总览的未完成行由调度方对话继续推进，整段任务不因你收口而结束；不得把「形式收口」当作「实质完成」上报。
3. 技能启用只以本技能 SKILL.md 为准：禁止列举/遍历技能目录或回读非引用文档；脚本按清单一次到位调用。
4. 生成文件一律入派发方指定的目标目录（env SMS_TMP），不得写入任何技能目录。
