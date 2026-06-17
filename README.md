# 友国文化 · 南岳木刻定制平台

以微信为主入口、移动端优先的「商品展示 + 定制体验 + 留资下单 + 自传播」平台。
3D 激光木刻定制器是平台上的第一个商品模块；架构按多商品平台设计，便于后续扩展。

> 详细规划与架构见 [`docs/PROJECT-PLAN.md`](docs/PROJECT-PLAN.md)。

## 技术栈
- 后端：Flask（应用工厂 + Blueprint 分层）+ SQLAlchemy + Flask-Migrate
- 数据库：MySQL 8（容器化，可移植；ORM 隔离，将来可换库）
- 存储：本地卷（默认）/ S3 兼容（第1期）
- 反代/HTTPS：Caddy（自动签证书）
- 部署：docker-compose（caddy + backend + mysql），**服务器无关**，换机=拷 `data/` 卷

## 一键启动（本地）
前提：已装 Docker 与 Docker Compose。

```bash
cp .env.example .env        # 然后修改其中的密码等
make up                     # 构建并启动；首次会自动建表 + 灌入初始数据
```

启动后：
- 平台首页 / 定制器： http://localhost/
- 店家后台： http://localhost/admin/ （密码 = .env 里的 ADMIN_PASSWORD）
- 健康检查： http://localhost/api/health

常用命令：`make logs`（日志）、`make down`（停止）、`make seed`（重灌数据）、`make backup`（导出数据库）。

## 验证留资接口（示例）
```bash
curl -X POST http://localhost/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"contact_name":"张三","phone":"13800001111","message":"想做一块平安喜乐","quantity":2}'
```
随后在 `/admin/` 即可看到该留言，并可一键拨号、改状态。

## 目录结构
```
backend/          Flask 应用（api 路由 / services 业务 / models 数据 / storage 存储抽象）
  app/api/        路由层（薄）：解析请求→调 service→返回
  app/services/   业务逻辑层（唯一操作模型处）
  app/models/     数据模型
  app/storage/    存储抽象（local + s3 占位）
  app/product_types/  商品类型注册表（扩展新商品类型只动这里 + 前端模块）
  migrations/     数据库迁移（禁手改表，一律走迁移）
frontend/public/  前端静态（落地页 / 定制器模块 / 后台页）
caddy/            反向代理 + HTTPS 配置
data/             运行时卷（mysql + uploads，已 gitignore）
docs/             项目规划与规范
```

## 上线要点
1. **ICP 备案**：大陆服务器解析 + 微信服务号配置「业务域名」都要求已备案域名，**请尽早办**。
2. 上线时把 `.env` 的 `SITE_ADDRESS` 改为你的域名、`PUBLIC_BASE_URL` 改为 `https://你的域名`，Caddy 会自动签发 HTTPS。
3. 把网站地址挂到微信**服务号自定义菜单**即可（MVP 阶段微信只作入口）。

## 路线图（摘要）
- **第0期(本骨架)**：留资/下单、商品/素材入库、极简后台、Docker 部署。
- **第1期**：分享海报合成、微信 JS-SDK 自定义转发、服务号新订单提醒、设计链接找回、(可)迁 S3+CDN。
- **第2期**：上线更多商品类型、多语言等。

## 已实现的接口（v1）
公开：`GET /categories`、`GET /products`、`GET /products/{id}`、`GET /patterns`、
`POST /uploads`、`POST /designs`、`GET /designs/{token}`、`POST /orders`、`GET /content/{key}`、
`POST /share/poster`（骨架，海报合成下一步实现）。
后台（需登录）：`POST /admin/login|logout`、`GET /admin/orders`、`PATCH /admin/orders/{id}`、`GET /admin/stats`。
