"""schema_migrate.py — 迁移台账：校验命名/校验和，列待应用（默认 dry-run，--yes 登记）。"""
import argparse, hashlib, json, os, re, sys

NAME = re.compile(r"^(V\d{4}|[0-9]{8,14})__([A-Za-z0-9_\-]+)\.sql$")


def load(root):
    out = []
    if not os.path.isdir(root): return out
    for f in sorted(os.listdir(root)):
        m = NAME.match(f)
        if not m:
            out.append({"file": f, "ok": False, "err": "命名须 V0001__topic.sql"}); continue
        txt = open(os.path.join(root, f), encoding="utf-8").read()
        ddl = txt.upper()
        out.append({"file": f, "ok": True, "ver": m.group(1),
                    "up": "-- +up" in txt or "CREATE" in ddl or "ALTER" in ddl,
                    "down": "-- +down" in txt or "DROP" in ddl,
                    "sha": hashlib.sha256(txt.encode()).hexdigest()[:12]})
    return out


def state(path):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"applied": {}}


def main():
    p = argparse.ArgumentParser(description="迁移台账/计划")
    p.add_argument("--migrations", required=True); p.add_argument("--state", required=True)
    p.add_argument("--yes", action="store_true", help="缺省仅预览")
    a = p.parse_args()
    items, st = load(a.migrations), state(a.state)
    bad = [i["file"] for i in items if not i["ok"]]
    pend = [i for i in items if i["ok"] and i["ver"] not in st["applied"]]
    for i in items:
        print("%-34s %s up=%s down=%s sha=%s" % (i["file"], "OK " if i["ok"] else "BAD",
                                                 i.get("up"), i.get("down"), i.get("sha")))
    print("待应用 =", len(pend), "| 非法 =", len(bad))
    if bad:
        print("存在非法迁移命名，中止"); return 2
    if not a.yes:
        print("[dry-run] 未登记；正式应用须 --yes"); return 0
    for i in pend:
        st["applied"][i["ver"]] = {"file": i["file"], "sha": i["sha"]}
        print("registered", i["ver"], i["file"])
    json.dump(st, open(a.state, "w", encoding="utf-8"), indent=1)
    print("台账已写入（实际执行由引擎客户端完成）", a.state); return 0


sys.exit(main())
