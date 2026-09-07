import runpy
from pathlib import Path
p=Path(__file__).with_name('test_hardening.py')
ns=runpy.run_path(str(p))
passed=failed=0
for name, fn in sorted(ns.items()):
    if name.startswith('test_'):
        try: fn(); passed += 1; print('PASS',name)
        except Exception as e: failed += 1; print('FAIL',name,repr(e))
print(f'RESULT passed={passed} failed={failed}')
raise SystemExit(1 if failed else 0)
