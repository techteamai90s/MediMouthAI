from fastapi import FastAPI
from app.routes.prescription import router  # import router correctly

app = FastAPI(title="Prescription Analyzer")

app.include_router(router)  # include it here

@app.get("/")
async def root():
    return {"message": "Welcome to Prescription Analyzer API"}