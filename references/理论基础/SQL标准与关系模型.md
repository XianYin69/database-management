# SQL 标准与关系模型（ISO/IEC 9075 · SQL:1999→SQL:2016/2023）

来源：[本地]（未联网确证）· 用途：方言差异判定基线。

## 关系模型要点

- 关系 = 元组集合（无序、无重复）；域上的属性；候选键 → 主键 → 外键引用完整性。
- 关系代数五基元：选择、投影、并、差、笛卡尔积；SQL 是其可表达语言的实现。
- 三值逻辑：TRUE/FALSE/**UNKNOWN**；NULL ≠ NULL，`=` 与 `<>` 均得 UNKNOWN，须 `IS [NOT] NULL`。

## 标准与方言

| 主题 | 标准做法 | 常见方言差异 |
|---|---|---|
| 分页 | `ORDER BY` + `FETCH FIRST n ROWS ONLY` | MySQL/PG 用 `LIMIT/OFFSET` |
| 引号 | 双引号=标识符，单引号=字符串 | MySQL 允许反引号/双引号字符串 |
| 自增 | `GENERATED ... AS IDENTITY`（SQL:2003） | MySQL `AUTO_INCREMENT`、PG `SERIAL/IDENTITY` |
| 日期 | `DATE '...'` 字面量 | 各引擎格式与隐式转换不同 |
| UPSERT | `MERGE`（SQL:2003/2016） | PG `ON CONFLICT`、MySQL `ON DUPLICATE KEY` |

## 用法规则

1. 写 SQL 前先声明目标引擎与版本；跨引擎 SQL 只依赖标准子集。
2. 依赖隐式转换/排序稳定性（无 `ORDER BY` 的返回顺序）视为缺陷，`sql_lint.py` 报警。
3. 方言行为不明 → 派 file_ops 查该引擎官方文档，禁止以他引擎经验类推。

- 返回 [references](../references.md) · [索引进阶](../性能与索引/索引进阶.md)
