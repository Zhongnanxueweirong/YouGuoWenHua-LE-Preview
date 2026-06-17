"""初始数据：分类、示例定制商品、祈福图样素材、店铺文案。
重复执行安全(按 key/slug 去重)。"""
from app.extensions import db
from app.models import Category, Product, Pattern, SiteContent

PATTERNS = [
    ("xinxiang", "心想事成"), ("coin", "招财进宝"), ("fu", "福满乾坤"),
    ("shou", "寿比南山"), ("pingan", "平安喜乐"), ("zhurong", "祝融赐福"),
    ("youqiu", "有求必应"), ("hengshan", "南岳进香"),
]

CONTENTS = {
    "store_brand": "友国文化 · 南岳木刻",
    "store_address": "湖南省衡阳市南岳区祝融路344号2栋10号",
    "store_business": "零售 · 批发 · 来图定制",
    "store_contact": "1XX-XXXX-XXXX（电话 / 微信同号）",
    "culture_intro": "南岳衡山，古称寿岳……（品牌缘起文案，可在后台编辑）",
}


def _get_or_create(model, defaults=None, **kw):
    obj = model.query.filter_by(**kw).first()
    if obj:
        return obj, False
    obj = model(**kw, **(defaults or {}))
    db.session.add(obj)
    return obj, True


def run_seed():
    cat, _ = _get_or_create(Category, slug="keepsake",
                            defaults={"name": "祈福木刻", "sort_order": 0})
    db.session.flush()

    prod, _ = _get_or_create(
        Product, name="南岳祈福木刻定制",
        defaults={"category_id": cat.id, "type": "laser_customizer",
                  "subtitle": "激光雕刻 · 来图定制", "sort_order": 0,
                  "config": {"module": "laser_customizer"}},
    )
    db.session.flush()

    for i, (key, name) in enumerate(PATTERNS):
        _get_or_create(Pattern, key=key,
                       defaults={"name": name, "product_id": prod.id, "sort_order": i})

    for k, v in CONTENTS.items():
        obj = SiteContent.query.filter_by(key=k).first()
        if not obj:
            db.session.add(SiteContent(key=k, value=v))

    db.session.commit()
