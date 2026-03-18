import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.menu import Menu
from app.schemas.menu import MenuCreate

router = APIRouter(prefix="/menus", tags=["Menus"])
logger = logging.getLogger(__name__)


@router.post("/menu")
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    new_menu = Menu(**menu.model_dump())
    try:
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
    except Exception:  # noqa: BLE001
        logger.exception("Failed to create menu")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create menu")

    return new_menu


@router.get("/menu")
def get_menu(db: Session = Depends(get_db)):
    try:
        menu = db.query(Menu).all()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to fetch menu")
        raise HTTPException(status_code=500, detail="Failed to fetch menu")

    return menu
