import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user as user_router
from app.routers import prediction as prediction_router
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configure CORS - support both local and production frontends
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://127.0.0.1:3000",  # Alternative local
]

# Add production frontend URL from environment variable if provided
production_frontend = os.getenv("FRONTEND_URL")
if production_frontend:
    allowed_origins.append(production_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

app.include_router(user_router.router)
app.include_router(prediction_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Lucky City API!"}
