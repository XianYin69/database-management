# 备份恢复与 PITR（未演练的备份等于没有备份）

来源：[本地]（未联网确证）· 用途：持久性与灾备验收。

## 三件套

- **全量**：物理（`pg_basebackup`、XtraBackup）或逻辑（`pg_dump`、`mysqldump`）。
- **增量/日志**：WAL 归档、binlog（ROW 格式 + `sync_binlog`/`innodb_flush_log_at_trx_commit`）。
- **副本**：流复制/异步复制 ≠ 备份（误删会同步传播）。

## RPO / RTO

| 指标 | 定义 | 决定因素 |
|---|---|---|
| RPO | 可容忍丢失数据量 | 日志归档频率、复制模式 |
| RTO | 可容忍恢复时长 | 备份体积、恢复流程自动化程度 |

## PITR 流程（概念）

1. 取最近全量 → 2. 恢复基线 → 3. 顺序重放 WAL/binlog 至目标时间点/事务位点 → 4. 校验 → 5. 切流。
- 目标点选择：误操作前一刻；须能按时间戳或位点定位（`pg_waldump`、`mysqlbinlog --stop-position`）。

## 验收规则（强制）

1. **恢复演练**：定期在隔离环境做全量+PITR 演练，记录耗时与数据校验结果；`backup_verify.py` 出报告。
2. **备份可用性校验**：校验和/大小/时间戳/可解密；异地与不可变副本（防勒索）。
3. **破坏性变更前先备份**：DDL、批量 UPDATE/DELETE、迁移切换前必须有可回滚点。
4. 备份失败告警不得静默吞掉；连续失败即熔断发布（见 [惩罚机制](../../resistance/惩罚机制/惩罚机制.md)）。

- 返回 [references](../references.md) · [迁移与版本化schema](迁移与版本化schema.md)
