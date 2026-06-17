.PHONY: up down logs migrate seed shell backup lint

up:        ## 构建并启动全部服务
	docker compose up -d --build

down:      ## 停止并移除容器
	docker compose down

logs:      ## 查看实时日志
	docker compose logs -f

migrate:   ## 在容器内执行数据库迁移
	docker compose exec backend flask db upgrade

seed:      ## 灌入初始数据
	docker compose exec backend flask seed

shell:     ## 进入后端容器
	docker compose exec backend sh

backup:    ## 导出数据库到 backup_时间戳.sql
	docker compose exec mysql sh -c 'exec mysqldump -uroot -p"$$MYSQL_ROOT_PASSWORD" "$$MYSQL_DATABASE"' > backup_$$(date +%Y%m%d_%H%M%S).sql

lint:      ## 代码检查
	cd backend && ruff check app && black --check app
