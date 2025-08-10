from fastapi import FastAPI
from app.routers import user as user_router
from app.routers import prediction as prediction_router
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user_router.router)
app.include_router(prediction_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Lucky City API!"}
