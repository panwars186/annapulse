from fastapi import FastAPI
from app.api.user import router as user_router
from app.db.database import Base, engine
import app.models.user
import app.models.otp
import app.models.subscription
import app.models.meal_schedule
import app.models.wallet
import app.models.wallet_transaction
import app.models.notification
import app.models.feedback
import app.models.menu

from app.api.auth import router as auth_router
import app.models.subscription_plan
from app.api.subscription_plan import router as plan_router
from app.api.subscription import router as subscription_router
from app.api.meal import   router as meal_router
from app.api.wallet import router as wallet_router
from app.api.billing import router as billing_router
from app.services.scheduler import scheduler
from app.api.calendar import router as calendar_router
from app.api.payment import router as payment_router
from app.api.admin import router as admin_router
from app.api.delivery import router as delivery_router
from app.api.menu import router as menu_router
from app.api.feedback import router as feedback_router
from app.api.notification import router as notification_router


app = FastAPI(title="AnnaPulse Api")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(plan_router)
app.include_router(subscription_router)
app.include_router(meal_router)
app.include_router(wallet_router)
app.include_router(billing_router)
app.include_router(calendar_router)
app.include_router(payment_router)
app.include_router(admin_router)
app.include_router(delivery_router)
app.include_router(menu_router)
app.include_router(feedback_router)
app.include_router(notification_router)


scheduler.start()


@app.get("/")
def root():
    return {"message": "Welcome to AnnaPulse !"}