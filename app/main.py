from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user as user_router
from app.routers import prediction as prediction_router
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specify allowed methods
    allow_headers=["Content-Type", "Authorization", "Accept"],  # Specify allowed headers
)

app.include_router(user_router.router)
app.include_router(prediction_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Lucky City API!"}
