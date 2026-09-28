# ACID 与事务隔离级别（含 ANSI 四级与快照隔离）

来源：[本地]（未联网确证）· 用途：一致性风险判定。

## ACID

- **原子性**：事务内操作全做或全不做（undo 日志）。
- **一致性**：约束/触发器/业务不变量在事务前后成立（唯一由应用负责的部分最易漏）。
- **隔离性**：并发事务互不可见中间态；代价 = 吞吐下降。
- **持久性**：提交后掉电不丢（WAL fsync + 复制）。

## ANSI 四级与异常

| 级别 | 脏读 | 不可重复读 | 幻读 |
|---|---|---|---|
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 否 | 可能 | 可能 |
| REPEATABLE READ | 否 | 否 | 可能（标准定义） |
| SERIALIZABLE | 否 | 否 | 否 |

- 引擎实际：PG `REPEATABLE READ` = 快照隔离（SI），可避免幻读但存在**写偏斜**；
  PG 9.1+ 的 `SERIALIZABLE` = SSI（谓词依赖环检测，报 `40001` 需重试）。
  MySQL InnoDB `REPEATABLE READ` 用 next-key lock 抑制幻读。
- 副作用：隔离级别越低越易出现 lost update / write skew → 需显式 `SELECT ... FOR UPDATE`
  或乐观锁版本号。

## 用法

1. 默认级别先查引擎文档再写业务；关键写路径显式声明级别与锁策略。
2. 事务内禁止外部 IO（HTTP/文件/消息）——长事务放大锁等待与回滚段。
3. 重试逻辑只针对可重试错误码（序列化冲突/死锁），死锁须回滚整事务。

- 返回 [references](../references.md) · [连接池与锁等待](../性能与索引/连接池与锁等待.md)
