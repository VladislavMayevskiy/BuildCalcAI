from fastapi import FastAPI
from app.routes import calculation, user, auth, room, ai, foundation
app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(calculation.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(room.router)
app.include_router(ai.router)
app.include_router(foundation.router)