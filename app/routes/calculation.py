from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.calculation import CalculationResponse, CalculationInput
from app.services.calculation_service import calculate_room, perimeter
from app.database import get_db
from app.models.calculation_history import Calculation
from app.models.users import Users
from app import oauth2
router = APIRouter(tags=["Calculation"])


@router.post("/calculate", response_model=CalculationResponse)
def calculate(data: CalculationInput, db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)  ):
    wall_area_before_openings = perimeter(data.length, data.width) * data.height

    if data.doors_area + data.windows_area > wall_area_before_openings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Windows and doors area cannot exceed total wall area",
        )

    response = calculate_room(data)
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