# 迁移与版本化 schema（可重复、可回滚、可灰度）

来源：[本地]（未联网确证）· 用途：schema 变更工程规范。

## 版本化原则

- 每次变更 = 一个带序号的迁移文件（`V0001__init.sql` / 时间戳前缀），含 up 与 down。
- 迁移表（`schema_version`/`flyway_schema_history`）记录已应用版本与校验和；禁止手改线上结构。
- 迁移文件一经合入不可编辑；修正用新迁移（append-only）。

## 安全变更模式（Expand / Migrate / Contract）

1. **Expand**：先加新列/新表/新索引（兼容旧代码）。
2. **Migrate**：双写 + 回填（分批、限速、可中断续跑）+ 对账。
3. **Contract**：切读新路径、观察期后再删旧结构（删除属破坏性，须审批）。

## 大表 DDL 注意

- 加列：常量默认值多数引擎可在线；带易失默认/生成值可能全表重写（须确证版本行为）。
- 加索引：`CREATE INDEX CONCURRENTLY`（PG）/ `ALGORITHM=INPLACE, LOCK=NONE`（MySQL）；
  失败会残留 `INVALID` 索引需清理。
- 改类型/重命名：多为重写或长锁 → 走影子表 + 触发器/CDC 同步 + 原子改名切换。
- 任何 DDL 前设 `lock_timeout`/`statement_timeout`，避免 MDL 排队雪崩。

## 验收

1. 迁移必须在预发环境跑 up→down→up 全链，记录耗时。
2. 回填任务须幂等、可断点续跑、有进度与差异计数。
3. 破坏性步骤须附回滚预案，见 [迁移安全约束](../../resistance/迁移安全约束/迁移安全约束.md)。

- 返回 [references](../references.md) · [备份恢复与PITR](备份恢复与PITR.md)
