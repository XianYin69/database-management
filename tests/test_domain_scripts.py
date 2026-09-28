"""test_domain_scripts.py — 领域脚本冒烟测试（sql_lint / schema_migrate / backup_verify）。"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(os.path.dirname(HERE), "scripts")


def run(name, *args):
    return subprocess.run([sys.executable, "-B", os.path.join(S, name), *args],
                          capture_output=True, text=True)


class Domain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_sql_lint_flags_bad_ddl(self):
        p = os.path.join(self.tmp, "V0001__bad.sql")
        open(p, "w", encoding="utf-8").write("DROP TABLE t;\nUPDATE t SET a=1;\n")
        r = run("sql_lint.py", p)
        self.assertEqual(r.returncode, 1)
        self.assertIn("破坏性 DDL", r.stdout)

    def test_schema_migrate_dry_run(self):
        m = os.path.join(self.tmp, "m"); os.makedirs(m)
        f = os.path.join(m, "V0001__init.sql")
        open(f, "w", encoding="utf-8").write("CREATE TABLE t(id int PRIMARY KEY);")
        st = os.path.join(self.tmp, "state.json")
        r = run("schema_migrate.py", "--migrations", m, "--state", st)
        self.assertEqual(r.returncode, 0)
        self.assertIn("待应用 = 1", r.stdout)
        self.assertFalse(os.path.exists(st))

    def test_backup_verify_detects_empty(self):
        b = os.path.join(self.tmp, "b"); os.makedirs(b)
        open(os.path.join(b, "full.dump"), "wb").close()
        r = run("backup_verify.py", "--dir", b)
        self.assertEqual(r.returncode, 1)
        self.assertIn("空文件", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
