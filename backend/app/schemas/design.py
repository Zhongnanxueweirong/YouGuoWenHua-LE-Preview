from typing import Optional, Any, Dict
from pydantic import BaseModel


class DesignCreate(BaseModel):
    product_id: Optional[int] = None
    params: Optional[Dict[str, Any]] = None
    pattern_id: Optional[int] = None
    upload_id: Optional[int] = None
