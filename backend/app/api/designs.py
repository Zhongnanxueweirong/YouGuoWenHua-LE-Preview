from flask import Blueprint, request
from ..schemas.design import DesignCreate
from ..services import design_service
from ..utils.responses import ok

bp = Blueprint("designs", __name__, url_prefix="/designs")


@bp.post("")
def create_design():
    payload = DesignCreate(**(request.get_json(silent=True) or {}))
    design = design_service.create_design(payload.model_dump())
    return ok({"id": design.id, "public_token": design.public_token})


@bp.get("/<token>")
def get_design(token):
    design = design_service.get_by_token(token)
    return ok(design.to_dict())
