
from sqlalchemy import Integer, Column, String

from app.db.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer,primary_key = True,index=True)
    user_id = Column(Integer)
    meal_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(String)



