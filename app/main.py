from fastapi import FastAPI
from app.routes import calculation

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(calculation.router)