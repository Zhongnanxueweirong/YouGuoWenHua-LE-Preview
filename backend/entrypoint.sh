#!/usr/bin/env sh
set -e

echo "[entrypoint] 等待数据库就绪..."
python - <<'PY'
import os, time, sqlalchemy
url = os.environ.get("DATABASE_URL", "")
if url.startswith("mysql"):
    eng = sqlalchemy.create_engine(url)
    for i in range(60):
        try:
            eng.connect().close()
            print("[entrypoint] 数据库已就绪")
            break
        except Exception:
            print(f"[entrypoint] 数据库未就绪，重试 {i+1}/60")
            time.sleep(2)
    else:
        raise SystemExit("[entrypoint] 数据库连接超时")
PY

echo "[entrypoint] 执行数据库迁移..."
flask db upgrade

echo "[entrypoint] 首启检查初始数据..."
python - <<'PY'
from app import create_app
from app.models import Product
app = create_app()
with app.app_context():
    if Product.query.count() == 0:
        from scripts.seed import run_seed
        run_seed()
        print("[entrypoint] 已灌入初始数据")
    else:
        print("[entrypoint] 已存在数据，跳过 seed")
PY

echo "[entrypoint] 启动 Gunicorn..."
exec gunicorn -w "${GUNICORN_WORKERS:-3}" -b 0.0.0.0:8000 --access-logfile - wsgi:app
