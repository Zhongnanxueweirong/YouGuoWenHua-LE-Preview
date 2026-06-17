"""商品类型注册表：未来新增商品类型只在此登记，公共底座不变。
每种类型可声明默认 config、校验函数、展示装配等（MVP 先放最简）。"""

REGISTRY = {
    "laser_customizer": {
        "label": "激光木刻定制",
        "frontend_module": "laser_customizer",
        "default_config": {},
    },
    # 将来：
    # "image_gallery": {"label": "图集展示", "frontend_module": "image_gallery", "default_config": {}},
    # "simple_product": {"label": "普通商品", "frontend_module": "simple_product", "default_config": {}},
}


def is_valid_type(t: str) -> bool:
    return t in REGISTRY
