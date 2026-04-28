from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import oauth2
from app.models.users import Users
from app.models.calculation_history import Calculation
from app.schemas.ai import AIExplanationResponse, AIRequestLogResponse
from app.services.openai_service import generate_ai_response
from app.models.ai_request_log import AIRequestLog
from app.services.ai_prompt_service import build_calculation_explanation_prompt

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/explain-calculation/{calculation_id}", response_model=AIExplanationResponse)
def explain_calculation(calculation_id: int , db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id,Calculation.user_id == current_user.id).first()   
    if not calculation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    prompt = build_calculation_explanation_prompt(input_data=calculation.input_data, result_data=calculation.result_data)
    
    try:
        explanation = generate_ai_response(prompt)
        log = AIRequestLog(
            user_id = current_user.id,
            prompt = prompt,
            calculation_id = calculation.id,
            response = explanation,
            error_message = None,
            status = "success"
        )
        db.add(log)
        db.commit()
    
    except Exception as error:
        log = AIRequestLog(
            user_id = current_user.id,
            prompt = prompt,
            calculation_id = calculation.id,
            response = None,
            error_message=str(error),
            status = "error"
        )
        db.add(log)
        db.commit()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI service is temporarily unavailable")
    return {
        "calculation_id": calculation.id,
        "explanation": explanation
    }



@router.get("/logs", response_model=list[AIRequestLogResponse])
def get_ai_logs(db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    logs = db.query(AIRequestLog).filter(AIRequestLog.user_id == current_user.id).order_by(AIRequestLog.created_at.desc()).all()   
    return logs

@router.get("/logs/{log_id}", response_model=AIRequestLogResponse)
def get_ai_log(log_id: int ,db: Session = Depends(get_db),current_user: Users = Depends(oauth2.get_current_user)):
    log = db.query(AIRequestLog).filter(AIRequestLog.user_id == current_user.id, AIRequestLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")  
    return log