"""sql_lint.py — SQL/迁移静态体检：SELECT *、无 WHERE 的 UPDATE/DELETE、隐式转换、缺约束、破坏性 DDL 无回滚。"""
import argparse, os, re, sys

RULES = [
    (r"\bselect\s+\*", "SELECT * 显式列化", "warn"),
    (r"\bupdate\s+\w+[^;]*\bset\b(?![^;]*\bwhere\b)", "UPDATE 无 WHERE", "err"),
    (r"\bdelete\s+from\s+\w+\s*;?(?![^;]*\bwhere\b)", "DELETE 无 WHERE", "err"),
    (r"\bdrop\s+(table|database|schema)\b", "破坏性 DDL：须审批+回滚预案", "err"),
    (r"\btruncate\b", "TRUNCATE：不可 PITR 到点，须备份点", "err"),
    (r"\badd\s+(column\s+)?\w+\s+.*(not\s+null)(?!.+default)", "NOT NULL 无默认值", "err"),
    (r"\bvarchar\s*\(\s*255\s*\)", "varchar(255) 默认长度：按域取值定", "warn"),
    (r"\bfloat\b|\bdouble\b", "金额/精度敏感量禁用浮点", "err"),
    (r"\bcreate\s+table\b(?![^;]*\bprimary\s+key\b)", "建表缺主键", "err"),
    (r"\breferences\b(?![^,]*\bon\s+delete\b)", "外键缺 ON DELETE 语义", "warn"),
    (r"\bcreate\s+index\b(?!\s+concurrently)", "大表建索引建议 CONCURRENTLY/LOCK=NONE", "warn"),
]


def lint(path):
    txt = open(path, encoding="utf-8").read()
    low = re.sub(r"--.*|/\*.*?\*/", " ", txt.lower())
    hits = []
    for pat, msg, lvl in RULES:
        for m in re.finditer(pat, low, re.S):
            hits.append((lvl, msg, txt[:m.start()].count("\n") + 1))
    return hits


def main():
    p = argparse.ArgumentParser(description="SQL 静态体检")
    p.add_argument("target"); a = p.parse_args()
    files = [a.target] if os.path.isfile(a.target) else [
        os.path.join(d, f) for d, _, fs in os.walk(a.target)
        for f in fs if f.endswith((".sql", ".ddl"))]
    err = warn = 0
    for f in files:
        for lvl, msg, line in lint(f):
            print("%s:%d [%s] %s" % (f, line, lvl, msg))
            err += lvl == "err"; warn += lvl == "warn"
    print("文件=%d 错误=%d 警告=%d" % (len(files), err, warn))
    sys.exit(1 if err else 0)


main()
