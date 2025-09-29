from fastapi import FastAPI
from app.routes import prescription, speech

app = FastAPI(title="MediMouth API")

app.include_router(prescription.router)
app.include_router(speech.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Prescription Analyzer API"}