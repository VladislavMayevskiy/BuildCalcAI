from fastapi import FastAPI
from app.api.routes import ai, auth, calculations, foundation, rooms, users
app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(calculations.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(ai.router)
app.include_router(foundation.router)