from fastapi import FastAPI
from app.routers import user_routes, account_routes,transaction_routes
from app.database import Base,engine

Base.metadata.create_all(bind=engine)

app=FastAPI(title="FinTrack API",version="1.0")

app.include_router(user_routes.router,prefix="/users",tags=["Users"])
app.include_router(account_routes.router,prefix="/accounts",tags=["Accounts"])
app.include_router(transaction_routes.router,prefix="/transactions",tags=["Transactions"])

@app.get("/")
def root():
    return {"message":"Bienvenue sur l'API FinTrack"}