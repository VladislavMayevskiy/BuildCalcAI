from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import oauth2
from app.models.users import Users
from app.models.calculation_history import Calculation
from app.schemas.ai import AIExplanationResponse
from app.services.openai_service import generate_ai_response

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/explain-calculation/{calculation_id}", response_model=AIExplanationResponse)
def explain_calculation(calculation_id: int , db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    calculation = db.query(Calculation).filter(calculation_id == Calculation.id, current_user.id == Calculation.user_id).first()
    if not calculation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    prompt = f"""
You are a renovation calculation assistant.

Explain this room material calculation to the user in simple language.
Do not change the numbers.
Do not invent extra measurements.
Explain where each result comes from.
Respond in Ukrainian.

Input room data:
{calculation.input_data}

Calculation result:
{calculation.result_data}
"""
    explanation = generate_ai_response(prompt)
    return {
        "calculation_id": calculation.id,
        "explanation": explanation
    }