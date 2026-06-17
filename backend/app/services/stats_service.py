from datetime import datetime, timedelta
from sqlalchemy import func
from ..extensions import db
from ..models import Order


def summary():
    week_ago = datetime.utcnow() - timedelta(days=7)
    total = Order.query.count()
    recent = Order.query.filter(Order.created_at >= week_ago).count()
    by_status = dict(
        db.session.query(Order.status, func.count(Order.id))
        .group_by(Order.status).all()
    )
    return {"total_orders": total, "orders_last_7d": recent, "by_status": by_status}
