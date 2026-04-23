from fastapi import FastAPI
from app.routes import calculation
from app.database import Base, engine
app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(calculation.router)