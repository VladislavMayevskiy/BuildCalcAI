from fastapi import FastAPI
from app.routes import calculation, user, auth, room
from app.database import Base, engine
app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(calculation.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(room.router)