import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])
logger = logging.getLogger(__name__)


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        notifications = (
            db.query(Notification)
            .filter(Notification.user_id == current_user.id)
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to fetch notifications for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to fetch notifications")

    return notifications


@router.post("/mark-as-read/{notification_id}")
def mark_as_read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == current_user.id,
            )
            .first()
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            "Failed to load notification_id=%s for user_id=%s",
            notification_id,
            current_user.id,
        )
        raise HTTPException(status_code=500, detail="Failed to update notification")

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()

    return {"message": "Notification marked as read"}
