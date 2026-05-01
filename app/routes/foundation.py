from app.schemas.strip_foundation import StripFoundationInput, StripFoundationResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import Users
from app.database import get_db
from app import oauth2
from app.services.strip_foundation_service import calculate_strip_foundation
from app.models.calculation_history import Calculation

router = APIRouter(prefix="/foundation" ,tags=["Foundation"])


@router.post("/strip", response_model=StripFoundationResponse)
def strip_foundation(data: StripFoundationInput ,db: Session = Depends(get_db), current_user: Users = Depends(oauth2.get_current_user)):
    response = calculate_strip_foundation(data=data)
    calculation = Calculation(
        user_id = current_user.id,
        room_project_id = None,
        calculation_type = "strip_foundation",
        input_data = data.model_dump(),
        result_data = response.model_dump()
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return response


