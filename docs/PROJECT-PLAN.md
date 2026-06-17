# 友国文化 · 展示与定制平台 — 项目规划与架构规范

> 文档目的：项目"地基文档"。任何人(含接手开发、或把本文贴给 Claude 的人)读完应能理解系统定位、技术选型、目录规范、数据结构与扩展边界。
>
> 状态：**v0.3 初稿** · 待评审
> 变更要点(相对 v0.1)：① 改为"服务器无关"可移植架构，去除云厂商绑定；② 从单一木刻定制器升级为**多商品展示平台**；③ 数据库定为 **MySQL**；④ 存储改为本地卷 + S3 兼容；⑤ 新增"面向年长用户的后台易用性"。
> v0.3 变更：**微信确定用「服务号」，且仅作入口(把微信当浏览器，菜单跳转到网站即可)**；JS-SDK 自定义转发卡片、服务号消息通知等深度集成移至第 1 期。第 0 期不碰 AppSecret/签名。

---

## 1. 产品定位

一句话：**一个以微信为主入口、移动端优先的"商品展示 + 体验/定制 + 留资下单 + 自传播"平台；3D 木刻激光定制器是平台上的第一个商品模块。背后配一个极简后台供店家运营。**

- 核心商业目标：为线下店(湖南衡阳南岳区)与品牌"友国文化"**获客、引流、宣传**。
- 主入口：**微信公众号/服务号**(菜单挂链接、推文引流)；网站为可独立访问的次入口。
- 核心用户：南岳大庙的香客与游客，手机在手(且多在微信里)，无耐心注册。
- 转化链路：用户在微信里打开 → 玩定制器/看商品 → **留联系方式 / 提交下单意向** → 店家后台跟进 → 线下或微信成交。
- 传播链路：用户设计/浏览后 → **微信转发卡片 + 分享海报(带店铺二维码)** → 朋友圈/微信群扩散；线下店张贴引流二维码，线上线下打通。

### 设计原则(优先级从高到低)
1. **服务器无关 / 可移植**：不绑定任何云厂商托管服务；全部组件容器化，换服务器=搬数据卷。
2. **规范与扩展性优先于功能数量**：目录、分层、接口约定一开始就立住。
3. **平台化**：核心是"多商品 + 多模块"的底座，木刻定制器只是其中一个模块。
4. **微信友好(当入口)**：站点在微信内与独立浏览器中都正常工作；微信只作入口，深度集成留待后续。
5. **游客零登录**：体验对所有人开放，绝不设注册墙。
6. **后台为年长者设计**：店家后台极简、大字、大按钮、无术语。
7. **不做线上支付**：下单只产生意向，成交走线下/微信；数据为支付预留口子但不实现。

---

## 2. 角色与核心流程

| 角色 | 能做什么 |
|------|----------|
| 游客(匿名) | 浏览商品、玩定制器、保存/分享设计、提交留资或下单意向、上传自定义图 |
| 店家/运营(单一管理员，年长者) | 登录极简后台、查看与跟进留资/订单、管理商品与素材、编辑文案、看简单统计 |

### 关键流程
```
微信公众号菜单/推文链接  ──┐
                          ├──▶ 平台 H5（也可浏览器直接访问）
线下店二维码 / 网址 ───────┘        │
                                   ├─ 浏览商品（木刻定制器 / 其他商品模块）
                                   ├─ 体验定制 → 保存设计 → 分享卡片 + 海报
                                   └─ 提交「定制/下单意向」（联系方式 + 关联商品/设计）
                                            └─▶ 后台「订单/线索」（状态：新）
                                                     └─ 店家联系 → 成交 → 状态流转
                                                     └─（将来）服务号消息推送提醒店家
```

---

## 3. 系统架构（服务器无关 · 全容器化）

### 总览
```
            ┌─────────────────────────────────────────┐
  用户(多在 │  Caddy（反向代理 + 自动HTTPS）            │
  微信内)──▶│  托管前端静态资源，代理 /api 到后端       │
            └───────────────┬─────────────────────────┘
                            ▼
                   ┌──────────────────┐
                   │ Flask API        │  应用工厂 + Blueprint 分层
                   │ (Gunicorn)       │  /api/v1/...
                   └───────┬──────────┘
            ┌──────────────┼───────────────┬─────────────────┐
            ▼              ▼               ▼                 ▼
     ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌──────────────┐
     │ MySQL 8    │  │ 存储(本地卷)│  │ 海报/缩略图   │  │ (第1期)微信   │
     │（容器+卷） │  │ 可换S3兼容  │  │（Pillow）     │  │ JS-SDK签名    │
     └────────────┘  └────────────┘  └──────────────┘  └──────────────┘
```
> 全部跑在一台服务器的 docker-compose 里。换服务器：拷 `data/` 卷 + 起容器即可，不依赖华为云任何专属服务。

### 技术选型与可移植性

| 关注点 | 选型 | 为什么 / 移植口子 |
|--------|------|-------------------|
| 后端框架 | **Flask**（应用工厂 + Blueprint） | 模块化：新功能=新增 Blueprint，不动旧码 |
| ORM / 迁移 | **SQLAlchemy + Flask-Migrate** | 数据库可换；迁移全程用 migration，禁手写 DDL |
| 数据库 | **MySQL 8**（容器 + 数据卷） | 团队**已熟悉**；容器化=换服务器照搬；ORM 隔离，将来换库改配置即可 |
| 请求校验/序列化 | **Pydantic v2** | 校验集中在 schemas/，与路由解耦 |
| 图片/文件存储 | **本地卷(默认)** | 最省、最可移植(拷文件夹)；接口抽象见 §8 |
| 对象存储(升级) | **S3 兼容**(MinIO 自建 / 任意云) | OBS·OSS·COS·R2 皆支持 S3 协议，**不绑定一家** |
| 海报/缩略图 | **Pillow** 服务端生成 | 量大可异步化(见 tasks/ 口子) |
| 微信集成 | **MVP 仅作入口**(菜单/推文跳转网址) | JS-SDK 分享、消息通知为第1期，见 §9 |
| WSGI | **Gunicorn** | 调 worker 数横向扩 |
| 反代/TLS | **Caddy**（自动签证书） | 也可换 Nginx |
| 编排 | **docker-compose** | 单机起全栈；上量可迁 K8s |
| 异步任务(预留) | MVP 同步处理 | 将来接 RQ/Celery + Redis，目录已留 |

> ⚠️ **ICP 备案是双重硬前提**：(1) 大陆服务器需备案才能解析域名；(2) **微信公众号配置安全域名也要求已备案域名**。流程约 2–3 周，**请立刻在所用服务器对应的云开始备案**(备案绑服务器，换服务器需变更备案，选服务器时留意)。

---

## 4. 平台化数据模型核心：商品与模块

这是支撑"未来不止一个定制器、还要放其他商品"的关键抽象。

- **商品(product)** 是平台的中心实体。每个商品有一个**类型(type)**，决定它用哪个前端模块来展示/交互。
- 类型专属的参数放在商品的 **`config`(JSON)** 字段里，不为每种新商品加新表。
- 当前 3D 木刻定制器 = 商品类型 `laser_customizer`。
- 将来新增"其他商品展示" = 新增一个类型(如 `image_gallery`、`simple_product`、`spec_table`…) + 一个对应前端模块；**留资、订单、后台、文案等公共底座完全复用**。

```
categories（分类）──< products（商品, 带 type + config）
                              │
            designs（定制快照, 仅定制类商品产生）
                              │
        leads/orders（留资/下单意向）── 引用 product，(可选)引用 design
site_contents（站点文案/店铺信息，全局）
```

---

## 5. 数据表设计

> 命名：表名复数 snake_case；所有表含 `id`、`created_at`、`updated_at`。设计后端无关(MySQL 优先，可移植)。

### 5.1 categories — 商品分类
| 字段 | 类型 | 说明 |
|------|------|------|
| id / name / slug | | 分类名、URL 别名 |
| sort_order / is_active | int / bool | 排序、是否显示 |

### 5.2 products — 商品（平台中心）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int PK | |
| category_id | FK→categories | |
| type | str | **模块类型**：laser_customizer / image_gallery / … |
| name / subtitle | str | 商品名、副标题 |
| cover_key | str | 封面图(存储层 key) |
| config | json | 类型专属配置(如定制器的可选木料/形制/默认素材集) |
| sort_order / is_active | int / bool | 排序、是否上架 |

### 5.3 patterns — 祈福图样素材库（定制器用）
把现写死在 JS 里的图样搬进库，店家可自助增删改、排序、上下架。
| 字段 | 类型 | 说明 |
|------|------|------|
| id / key / name / description | | 标识、显示名、简介 |
| image_key | str | 图样文件(存储层) |
| product_id | FK→products | 可空：归属某定制商品(或全局共享) |
| sort_order / is_active | int / bool | |

### 5.4 uploads — 用户上传图
| 字段 | 类型 | 说明 |
|------|------|------|
| id / storage_key / mime / size | | 文件信息 |
| ip_hash | str | 来源粗略哈希(隐私友好) |

### 5.5 designs — 设计快照（定制类商品产生）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int PK | |
| product_id | FK→products | 来自哪个定制商品 |
| public_token | str 唯一 | 不可猜的分享/找回令牌 |
| params | json | 形制/尺寸/木料/激光/摆放等全部参数(整合存 JSON) |
| pattern_id / upload_id | FK | 选用素材 或 自定义图(二选一) |
| thumbnail_key | str | 渲染缩略图 |

### 5.6 orders — 订单 / 定制意向（核心获客实体）
统一承载"留资咨询"与"下单意向"：轻咨询=未填数量的订单。
| 字段 | 类型 | 说明 |
|------|------|------|
| id / order_no | | 主键、人类可读单号(如 YG20260617-0007) |
| contact_name / phone / wechat | str | 联系人、电话、微信 |
| message / quantity | str / int | 留言、数量(咨询可空) |
| product_id | FK→products | 关于哪个商品 |
| design_id | FK→designs | 关联设计快照(可空) |
| status | enum | new / contacted / confirmed / producing / completed / cancelled |
| source | str | 渠道：wechat_oa / web / poster / qr_store |
| payment_status | enum | **预留**：unpaid(默认)；将来扩 paid_offline/paid_online |
| operator_note | str | 店家内部备注 |

> 取舍：MVP 提交即落 `orders`(留资=最小订单)。将来区分"轻咨询 vs 正式订单"加 `type` 字段即可，不拆表。

### 5.7 site_contents — 站点文案/店铺信息
让店家不改代码就能改地址、电话、品牌缘起文案。
| 字段 | 类型 | 说明 |
|------|------|------|
| id / key / value | | key 如 store_address、culture_intro；value 为 json/text |

### 5.8 admin（鉴权，非数据表）
MVP **不建用户表**：后台用 `.env` 单一密码 + 服务端 session。`admin_users` 作为将来口子，文档记录、不实现。

---

## 6. 项目目录结构

```
youguo-platform/
├── docker-compose.yml            # 默认编排（caddy + backend + mysql）
├── docker-compose.prod.yml       # 生产覆盖（端口/日志/重启/worker）
├── .env.example                  # 环境变量样例（真实 .env 不入库）
├── .gitignore  ·  README.md  ·  Makefile   # 一键命令: up/down/migrate/lint/test
│
├── docs/
│   ├── PROJECT-PLAN.md           # 本文件
│   ├── API.md                    # 接口清单（随开发更新）
│   └── CONVENTIONS.md            # 开发规范
│
├── caddy/Caddyfile               # 反代 + HTTPS
│
├── backend/                      # Flask 应用
│   ├── Dockerfile · pyproject.toml · wsgi.py
│   ├── app/
│   │   ├── __init__.py           # ★ create_app() 应用工厂
│   │   ├── config.py             # Base/Dev/Prod 配置类
│   │   ├── extensions.py         # db / migrate / cors 单例
│   │   ├── errors.py             # 全局错误处理 + 统一错误结构
│   │   ├── models/               # categories/products/patterns/designs/orders/...
│   │   ├── schemas/              # Pydantic 校验/序列化
│   │   ├── api/                  # ★ 路由层(薄)，按资源拆 Blueprint
│   │   │   ├── __init__.py        #   注册全部蓝图到 /api/v1
│   │   │   ├── products.py · categories.py
│   │   │   ├── designs.py · patterns.py · uploads.py
│   │   │   ├── orders.py · content.py
│   │   │   ├── share.py · wechat.py        # 海报 / 微信JS-SDK签名
│   │   │   └── admin.py                     # 后台(鉴权)
│   │   ├── services/             # ★ 业务逻辑层
│   │   ├── product_types/        # ★ 商品类型注册表(各类型的校验/展示规则)
│   │   ├── storage/              # ★ 存储抽象: base + local + (s3)
│   │   ├── tasks/                # 预留：异步任务
│   │   └── utils/                # 响应封装/分页/token
│   ├── migrations/  ·  tests/
│
├── frontend/                     # 前端
│   ├── Dockerfile
│   ├── public/
│   │   └── modules/
│   │       └── laser_customizer/  # 现有 3D 定制器(先原样保留为模块)
│   ├── pages/                    # 首页/分类/商品/缘起/店铺/成品图集
│   ├── admin/                    # ★ 极简后台页(面向年长者)
│   └── assets/
│
└── data/                         # ★ 运行时数据卷(.gitignore，仅服务器)
    ├── mysql/                    # MySQL 数据
    └── uploads/                  # 上传图 + 海报/缩略图
```

### 分层铁律
- **api/(路由)** 只做：解析请求 → 调 service → 返回响应；不写业务、不拼 SQL。
- **services/(业务)** 是唯一操作模型、组织规则的地方。
- **product_types/** 用"类型注册表"承载每种商品的差异(校验规则、展示数据装配)，新增商品类型只在此与前端 modules/ 各加一处。
- **models/(数据)** 只定义表与关系。
- 结果：加"其他商品类型""在线支付""会员"都是新增模块，旧代码基本不动。

---

## 7. API 设计

### 约定
- 前缀与版本：`/api/v1/`，新版本另开 `/api/v2/`，老版本不破坏。
- 资源命名：复数名词、kebab URL、标准 REST 动词。
- 统一响应：`{ "code":0, "message":"ok", "data":{...} }`(code=0 成功)，并配恰当 HTTP 状态码。
- 分页：`?page=1&page_size=20` → `{ items,total,page,page_size }`。

### 公开接口（无需登录）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/categories | 分类列表 |
| GET | /api/v1/products | 商品列表(可按分类筛) |
| GET | /api/v1/products/{id} | 商品详情(含 type + config) |
| GET | /api/v1/patterns | 上架素材(可按商品筛) |
| POST | /api/v1/uploads | 上传自定义图 |
| POST | /api/v1/designs | 保存设计，返回 id + public_token |
| GET | /api/v1/designs/{token} | 凭令牌找回设计 |
| POST | /api/v1/orders | 提交留资/下单意向 |
| GET | /api/v1/content/{key} | 取站点文案 |
| POST | /api/v1/share/poster | 由设计/商品生成分享海报 |
| GET | /api/v1/wechat/jssdk-config | (第1期)微信 JS-SDK 签名配置，见 §9 |

### 后台接口（需登录，/api/v1/admin）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /admin/login · /admin/logout | 密码登录/登出 |
| GET / PATCH | /admin/orders (/{id}) | 订单看板：筛选/分页 / 改状态/加备注 |
| CRUD | /admin/products · /admin/categories · /admin/patterns | 商品/分类/素材管理 |
| PUT | /admin/content/{key} | 编辑文案 |
| GET | /admin/stats | 简单统计 |

> 细化到 `docs/API.md`，本文只定骨架与约定。

---

## 8. 存储抽象（可移植关键）

```python
# app/storage/base.py —— 所有后端实现同一接口
class Storage:
    def save(self, file, key: str) -> str: ...   # 返回可访问 url/key
    def url(self, key: str) -> str: ...
    def delete(self, key: str) -> None: ...
```
- **MVP 默认 `LocalStorage`**：写 `data/uploads/`，Caddy 静态对外。最省、搬服务器=拷文件夹。
- **升级 `S3Storage`(S3 兼容)**：用 boto3 一套代码对接 **MinIO(自建) / 华为OBS / 阿里OSS / 腾讯COS / Cloudflare R2** —— 只改 `.env` 的 endpoint 与密钥，**不绑定任何一家云**，业务代码零改。
- 图片：上传压缩限尺寸；缩略图/海报用 Pillow；原图与生成物分目录。

---

## 9. 微信（仅作入口）

**已定**：使用**服务号**；MVP 阶段微信只当作"入口/浏览器"，菜单/推文跳转到平台网站即可，**不做深度集成**。平台 H5 在微信内与独立浏览器都正常工作。

### MVP 接入方式（轻）
- **服务号自定义菜单** → 链接到平台网址(如"在线定制""商品展示""联系我们")。
- **图文推文** 内嵌网址做内容引流。
- **网站/线下二维码** 作补充入口。

### 微信内传播（MVP 的现实手段）
- 第 0 期**不做** JS-SDK，所以用户点微信"…→分享"出现的是默认卡片(无法自定义)。
- 因此**分享海报是 MVP 阶段微信里最主要的传播方式**：服务端 Pillow 合成竖图(设计渲染图 + 祝福语 + 品牌 + **店铺二维码**)，用户长按保存/转发朋友圈。海报**保留在 MVP**。

### MVP 硬前提
- 服务号菜单跳转的域名需配为**业务域名**，而配业务域名要求**已备案域名**；叠加大陆服务器解析也要备案。→ **ICP 备案仍是必须，请尽早办。**
- MVP **不需要** AppSecret、不需要 JS-SDK 签名服务、不需要安全域名 JS 授权。

### 第 1 期再做的深度集成（口子已留）
- **JS-SDK 自定义转发卡片**：后端 `GET /api/v1/wechat/jssdk-config` 签名，前端 `wx.config + wx.updateAppMessageShareData` 自定义标题/缩略图。需 AppID/AppSecret、配 JS 接口安全域名、后端缓存 `jsapi_ticket`(约2小时)。与海报叠加，传播更顺。
- **服务号模板/订阅消息**：新订单推送"您有 1 条新定制留言"给店家(对年长操作者极友好)，或给客户发进度。
- **网页授权 OAuth**：静默拿 openid，用于线索归因或消息触达。

---

## 10. 后台易用性（面向年长操作者）

操作者与使用者多为年长者，后台按"长辈也能用"设计：

- **一屏为主**：进入即是"订单/留言"列表，今日新单醒目高亮，无需翻找。
- **大字、大按钮、高对比**；每条订单用大号卡片展示联系人、电话(可一键拨号/复制)、需求、关联设计缩略图。
- **状态操作做成大按钮**："已联系""已成交""取消"，点一下即变，带二次确认防误触。
- **零术语**：界面全中文白话，不出现"字段""枚举""API"等词。
- **理想形态**：后台也做成微信 H5，店家在微信里点公众号菜单"管理后台"就能看；配合服务号消息提醒，几乎不需要"打开网站、登录"这类门槛。
- 商品/素材/文案管理同样走"大按钮 + 表单极简 + 预览"路线，能不让长辈输入的就不让输入(多用选择、上传)。

---

## 11. Docker 部署

`docker-compose.yml` 起：

| 服务 | 角色 | 卷 |
|------|------|-----|
| caddy | 反代 + 自动 HTTPS + 托管前端静态 | 证书卷、前端产物 |
| backend | Flask + Gunicorn | 读 `data/uploads`、连 mysql |
| mysql | MySQL 8 | `./data/mysql` |
| (minio) | **可选**，将来需 S3 存储时启用 | `./data/minio` |

- **换服务器**：拷 `data/`(mysql + uploads) + 起容器即可，不依赖原云任何专属服务。
- 升级到对象存储+CDN：启用 S3 存储后端，配 `.env`，去掉 uploads 卷依赖。
- 密钥全走 `.env`，**不入库**；生产用 `docker-compose.prod.yml` 覆盖。
- 备份：`mysqldump` 定时 + 同步 uploads 目录(脚本入 `Makefile`)。

---

## 12. 配置与环境变量（.env.example 雏形）

```
FLASK_ENV=production
SECRET_KEY=please-change-me
# 数据库（MySQL，容器内）
DATABASE_URL=mysql+pymysql://app:password@mysql:3306/youguo
# 存储
STORAGE_BACKEND=local            # local | s3
UPLOAD_DIR=/app/data/uploads
# S3 兼容(将来启用，兼容 MinIO/OBS/OSS/COS/R2)
# S3_ENDPOINT= / S3_BUCKET= / S3_ACCESS_KEY= / S3_SECRET_KEY=
# 站点 & 后台
PUBLIC_BASE_URL=https://your-domain.com
ADMIN_PASSWORD=please-change-me
# 微信服务号（第1期深度集成时再填；MVP 不需要）
# WECHAT_APPID=
# WECHAT_APPSECRET=
```

---

## 13. 安全与合规

- 上传：限图片类型、限大小、校验真实 MIME，防恶意文件。
- 提交接口：限流 + 防刷(蜜罐/频率限制)，防垃圾留资。
- 后台：密码 + session、强制 HTTPS；将来多用户再上正式鉴权。
- 隐私：联系方式属个人信息，最小化收集、不公开展示；来源仅存哈希。
- 微信密钥：AppSecret 严禁入库与下发前端；签名在后端完成。
- 版权：保留"友国文化"水印与"盗图必究"声明，素材原创。
- 备案：域名 ICP 备案为大陆部署 + 微信集成双重前提(见 §3)。

---

## 14. 开发规范（CONVENTIONS 摘要）

- **Python 风格**：black + ruff + isort，pre-commit 钩子统一执行。
- **命名**：Python snake_case；URL 复数/kebab；常量大写。
- **分支**：main(可部署) / dev(集成) / feat-*、fix-*。
- **提交信息**：Conventional Commits，如 `feat(orders): 新增下单意向提交接口`。
- **数据库变更**：一律 `flask db migrate` 生成迁移并入库，**禁手改表**。
- **测试**：pytest，重点 service 层。
- **文档同步**：接口变更同步 `docs/API.md`。

---

## 15. 路线图

| 阶段 | 目标 | 范围 |
|------|------|------|
| **第 0 期**(先搭起来) | 跑通获客闭环 + 立住平台底座 | 平台骨架与规范、商品/分类/素材入库、木刻定制器作为首个模块、设计保存、留资/下单接口、**极简后台**、**分享海报**(微信内主要传播手段)、服务号菜单挂网址、Docker 一键部署(caddy+backend+mysql) |
| **第 1 期**(增长) | 放大传播与运营 | **微信深度集成**(JS-SDK 自定义转发卡片、服务号新订单消息提醒)、设计链接找回、成品图集、后台统计看板、(可)迁 S3+CDN |
| **第 2 期**(平台扩张) | 多商品类型上线 | 新增其他商品展示模块(image_gallery 等)、多语言、网页授权 OAuth；会员/复购仅在确有需求时再加；线上支付按你的决定**不做** |

---

## 16. 待你确认

> 已定：微信用**服务号**、MVP 仅作入口；数据库 **MySQL**；服务器无关容器化；后台为年长者设计。

1. **平台/仓库命名**：用 `youguo-platform`？(影响目录与镜像名)
2. **海报二维码指向**：站点首页 / 服务号关注页 / 微信客服？(决定海报怎么画)
3. **现有定制器**先作为独立模块嵌入、第 1 期再与展示页统一框架——是否认可此节奏？
4. **后台形态**：第 0 期做"网页极简后台"(微信内 H5 后台 + 消息提醒按你意思放第 1 期)——确认？
5. **服务器**：暂用华为云，是否需要我在备份/迁移脚本上特别照顾"将来搬到便宜 VPS"的步骤？

---

*© 友国文化 · 本文档为项目内部规划资料*
