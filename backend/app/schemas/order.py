from typing import Optional
from pydantic import BaseModel, Field, field_validator


class OrderCreate(BaseModel):
    contact_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=5, max_length=50)
    wechat: Optional[str] = Field(None, max_length=100)
    message: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=1, le=99999)
    product_id: Optional[int] = None
    design_id: Optional[int] = None
    source: Optional[str] = Field("web", max_length=30)
    # 蜜罐字段：正常用户不会填，填了即视为机器人
    hp: Optional[str] = None

    @field_validator("contact_name", "phone")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v


class OrderStatusUpdate(BaseModel):
    status: Optional[str] = None
    operator_note: Optional[str] = None
