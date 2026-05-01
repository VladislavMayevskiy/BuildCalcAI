from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.calculation_result import CalculationResult
from app.schemas.calculation import CalculationResponse, CalculationInput, CalculationHistoryResponse
from app.services.calculation_service import calculate_room, calculate_room_v2
from app.database import get_db
from app.models.calculation_history import Calculation
from app.models.users import Users
from app import oauth2




router = APIRouter(tags=["Calculation"])


@router.get("/calculations/history", response_model=list[CalculationHistoryResponse])
def get_calculation_history(db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    history = (
        db.query(Calculation).filter(Calculation.user_id == current_user.id).all()
        )

    return history

@router.post("/calculate", response_model=CalculationResponse)
def calculate(data: CalculationInput, db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)  ):
    try:
        response = calculate_room(data)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    calculation = Calculation(
    user_id=current_user.id,
    room_project_id=None,
    calculation_type="room_calculation",
    input_data=data.model_dump(),
    result_data=response.model_dump(),
)
    db.add(calculation)
    db.commit()
    return response


@router.post("/calculate/v2", response_model=CalculationResult)
def calculate_v2(data: CalculationInput,db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    try:
        response = calculate_room_v2(data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    calculation = Calculation(
        user_id=current_user.id,
        room_project_id=None,
        calculation_type="room_calculation_v2",
        input_data=data.model_dump(),
        result_data=response.model_dump(),
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return response