"""分享海报：MVP 阶段微信里最主要的传播手段。
此处先给出接口骨架；海报合成(Pillow + 服务号关注二维码)在下一步实现。"""
from flask import Blueprint, request
from ..utils.responses import ok

bp = Blueprint("share", __name__, url_prefix="/share")


@bp.post("/poster")
def poster():
    data = request.get_json(silent=True) or {}
    # TODO(下一步): 用 Pillow 合成竖版海报：
    #   设计渲染图 + 祝福语 + 品牌「友国文化·南岳木刻」+ 服务号关注小二维码
    #   生成后存入 uploads 卷，返回图片 url
    return ok({"status": "todo", "received": data,
               "note": "海报合成将于下一步实现"})
