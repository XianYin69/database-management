# PostgreSQL 官方文档要点（docs.postgresql.org）

来源：[本地]（未联网确证·引用前须以当前版本官方页确证）· 用途：PG 特性与运维基线。

## 结构

- 实例 → 数据库 → schema → 对象；角色与权限分层（`GRANT`/`RLS`）。
- MVCC：元组多版本 + `xmin/xmax`；`VACUUM`/autovacuum 回收死元组，防事务 ID 回卷。
- WAL：`wal_level`（replica/logical）、归档、流复制、逻辑复制、时间点恢复（PITR）。

## 常用能力

| 能力 | 说明 |
|---|---|
| 索引类型 | B-tree / hash / GIN / GiST / BRIN / SP-GiST；表达式与部分索引 |
| 数据类型 | `jsonb`（+GIN）、数组、范围、`uuid`、生成列 |
| 约束 | 主外键（含延迟约束）、唯一、检查、排除约束（`EXCLUDE USING gist`） |
| 并发 | 快照隔离、SSI、`SELECT FOR UPDATE/SHARE`、`SKIP LOCKED`（队列模式） |
| DDL | `CREATE INDEX CONCURRENTLY`、`SET NOT NULL` 分步、常量默认值在线加列 |
| 运维 | `pg_stat_activity`、`pg_stat_statements`、`EXPLAIN (ANALYZE, BUFFERS)`、`pg_dump`/`pg_basebackup` |

## 用法

1. 迁移脚本优先使用可并发的 DDL 形式，避免长时锁表。
2. 任何「PG 某版本行为」须派 file_ops 抓官方 Release Notes 确证后改写为 `[联网]`。
3. 执行计划以 `EXPLAIN (ANALYZE, BUFFERS)` 判读；估算与实际行数偏差 >10× 视为统计过期。

- 返回 [references](../references.md) · [迁移与版本化schema](../可用性与演进/迁移与版本化schema.md)
