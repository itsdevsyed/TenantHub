from fastapi import FastAPI

from app.auth.routes import router as auth_router

app = FastAPI(
    title="TenantHub API",
    version="1.0.0"
)

# ---------- ROUTES ----------
app.include_router(auth_router)


# ---------- ROOT ----------
@app.get("/")
async def root():
    return {"message": "TenantHub API running"}
