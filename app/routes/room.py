from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.calculation import CalculationResponse, CalculationInput, CalculationHistoryResponse
from app.services.calculation_service import calculate_room, perimeter
from app.database import get_db
from app.models.room import Room
from app.models.users import Users
from app import oauth2
from app.schemas.Room import RoomCreate,RoomResponse,RoomUpdate


router = APIRouter(prefix="/rooms", tags=["Room"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomResponse)
def create_room(data: RoomCreate, db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)):
    new_room = Room(user_id = current_user.id, name = data.name, length = data.length, width = data.width, height = data.height, doors_area = data.doors_area, windows_area = data.windows_area, room_type = data.room_type)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)):
    user_rooms = db.query(Room).filter(Room.user_id == current_user.id).all() 
    return user_rooms

@router.get("/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomResponse)
def get_room(room_id: int , db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)):
    room = db.query(Room).filter(Room.id == room_id, Room.user_id == current_user.id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

@router.patch("/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomResponse)
def update_room(room_id: int, data: RoomUpdate, db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    room = db.query(Room).filter(Room.id == room_id, Room.user_id == current_user.id).first()

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int , db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)):
    room = db.query(Room).filter(Room.id == room_id, Room.user_id == current_user.id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(room)
    db.commit()
    return
