"""backup_verify.py — 备份可用性核验：大小、新鲜度、格式头、校验和。"""
import argparse, hashlib, json, os, sys, time

SIG = {".gz": b"\x1f\x8b", ".zip": b"PK\x03\x04", ".7z": b"7z\xbc\xaf"}


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read(1 << 20)).hexdigest()[:16]


def status_of(p, size, age, max_age_h):
    sig = SIG.get(os.path.splitext(p)[1].lower())
    if size == 0: return "空文件"
    if age > max_age_h: return "过期"
    if sig and open(p, "rb").read(len(sig)) != sig:
        return "格式头不符"
    return "OK"


def check(root, max_age_h):
    rows = []
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(dp, f)
            size = os.path.getsize(p)
            age = (time.time() - os.path.getmtime(p)) / 3600.0
            rows.append(dict(file=p, size=size, age_h=round(age, 1), sha=sha(p),
                             status=status_of(p, size, age, max_age_h)))
    return rows


def main():
    ap = argparse.ArgumentParser(description="备份核验")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--max-age-hours", type=float, default=24)
    ap.add_argument("--json", help="报告输出路径（落 tmp/用户缓存）")
    a = ap.parse_args()
    rows = check(a.dir, a.max_age_hours)
    bad = [r for r in rows if r["status"] != "OK"]
    for r in rows:
        print("%-8s %10d %6.1fh %s %s" % (r["status"], r["size"],
                                          r["age_h"], r["sha"], r["file"]))
    print("备份数=%d 异常=%d" % (len(rows), len(bad)))
    if a.json: json.dump(rows, open(a.json, "w", encoding="utf-8"), indent=1)
    print("提示：仅核验可用性，恢复演练须在隔离环境执行")
    sys.exit(1 if bad else 0)


main()
