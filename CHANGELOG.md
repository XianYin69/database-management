# CHANGELOG

## 0.1.0 — 初版（database-management）

- 结构复刻 general-programming / ui-design：创建路径 12 节点 + 修改路径。
- 新增机制约束：垃圾回收 / 上下文压缩 / 逻辑链 / 过程链存取 / 惩罚 / 沙盒。
- 新增领域约束：`resistance/数据完整性约束/`（主外键、唯一、检查、精度、UTC 时间）、
  `resistance/迁移安全约束/`（破坏性 DDL 须备份点 + 回滚预案 + 影响评估 + 审批）。
- 新增薄技能依赖声明：file_ops / code-guidelines / pavedpath-code / python / git（见 `dependence/`）。
- 新增知识库 5 域 12 条目：理论基础、经典书目、数据建模、性能与索引、可用性与演进。
  本次构建环境外网不可达（urlopen 10060），条目如实标注 `[本地]`，未伪造 URL。
- 新增脚本：`schema_migrate.py`（迁移台账/校验和，默认 dry-run）、`sql_lint.py`（SQL 静态体检）、
  `slow_query_check.py`（慢日志指纹 + EXPLAIN 信号）、`backup_verify.py`（备份可用性核验）。
- 新增 `tests/test_domain_scripts.py`：三脚本冒烟测试。
- 违规后果：放宽完整性 → 脏数据不可逆；跳过迁移审批 → 不可回滚的线上事故。
- 兜底：无网络 → `[本地]` 标注并说明缺口；无临时库 → 降级静态校验并声明「未做真库验证」。
