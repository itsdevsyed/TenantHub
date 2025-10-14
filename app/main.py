from fastapi import FastAPI

app = FastAPI(title="TenantHub")

@app.get("/")
async def root():
    return {"message": "TenantHub API is running!"}
