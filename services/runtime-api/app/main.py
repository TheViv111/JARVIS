from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.phase1 import router as phase1_router
from app.routes.orb import router as orb_router

app = FastAPI(title="JARVIS Runtime API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(phase1_router)
app.include_router(orb_router)

