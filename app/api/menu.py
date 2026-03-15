from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.menu import Menu
from app.schemas.menu import MenuCreate

router = APIRouter(prefix="/menus",tags=["Menus"])

@router.post("/menu")
def create_menu(menu:MenuCreate,db:Session = Depends(get_db)):
    new_menu = Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

@router.get("/menu")
def get_menu(db:Session = Depends(get_db)):
    menu =  db.query(Menu).all()
    return menu


