# main.py
from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()

# Include routes
app.include_router(auth_router)

# Optional root
@app.get("/")
async def root():
    return {"message": "TenantHub API running"}
