import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import predict, teams, elo, simulate

app = FastAPI(title="World Cup Predictor API")
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"], allow_headers=["*"])
app.include_router(predict.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(elo.router, prefix="/api")
app.include_router(simulate.router, prefix="/api")

@app.get("/")
def root(): return {"status": "ok"}