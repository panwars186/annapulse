from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.notification import Notification

router = APIRouter(prefix = "/notifications",tags= ["Notiifications"])

@router.get("/")
def get_notifications(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    notification = db.query(Notification).filter(Notification.user_id == current.user_id).all()
    return notification


def mark_as_read_notification(
    notification_id:int,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    notification = db.query(Notification).filter(
Notification.id == notification_id,
    Notification.user_id == current_user.id).first()
    notification.is_read = True
    db.commit()
    return {"message":"Notification marked as read"}



