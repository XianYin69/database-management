"""slow_query_check.py — 慢日志/EXPLAIN 剖面：解析耗时与行数，按总耗时排序给治理优先级。"""
import argparse, re, sys

Q = re.compile(r"query_time:\s*([\d.]+).*?rows_examined:\s*(\d+).*?rows_sent:\s*(\d+)", re.S | re.I)
SQL = re.compile(r"^\s*(SELECT|UPDATE|DELETE|INSERT)", re.I)
PLAN = re.compile(r"(Seq Scan|Full scan|type=ALL|Using filesort|Using temporary|rows=(\d+))", re.I)


def digest(text):
    """按语句指纹聚合（数字/字符串归一）→ 总耗时、次数、扫描/返回比。"""
    agg = {}
    for block in text.split(";"):
        m = Q.search(block)
        if not m:
            continue
        stmt = " ".join(l for l in block.splitlines() if SQL.match(l))
        if not stmt:
            continue
        key = re.sub(r"\d+", "?", re.sub(r"'[^']*'", "?", stmt.lower()))[:120]
        t, ex, sent = float(m.group(1)), int(m.group(2)), int(m.group(3))
        a = agg.setdefault(key, {"t": 0.0, "n": 0, "ex": 0, "sent": 0})
        a["t"] += t; a["n"] += 1; a["ex"] += ex; a["sent"] += sent
    return agg


def main():
    p = argparse.ArgumentParser(description="慢查询剖面")
    p.add_argument("--log", help="慢日志文件"); p.add_argument("--explain", help="EXPLAIN 文本")
    p.add_argument("--top", type=int, default=10); a = p.parse_args()
    if a.explain:
        txt = open(a.explain, encoding="utf-8").read()
        hits = PLAN.findall(txt)
        print("计划风险信号 =", len(hits), "| 示例:", [h[0] for h in hits[:5]])
        if not hits:
            print("未发现典型退化信号")
    if not a.log:
        print("未提供 --log，仅执行 EXPLAIN 检查"); return
    agg = digest(open(a.log, encoding="utf-8", errors="ignore").read())
    rows = sorted(agg.items(), key=lambda kv: -kv[1]["t"])[:a.top]
    for k, v in rows:
        ratio = v["ex"] / max(v["sent"], 1)
        print("总耗时=%.3fs 次数=%d 扫描/返回=%.1f | %s" % (v["t"], v["n"], ratio, k[:80]))
    print("指纹数 =", len(agg), "| 优先治理前", len(rows), "项（扫描/返回高者先建索引或改写）")


main()
