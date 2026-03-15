from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Menu(Base):
    __tablename__ = "menu"
    
    id = Column(Integer,primary_key=True,index=True)
    day_of_week = Column(String)
    meal_type = Column(String)
    dish_name = Column(String)
