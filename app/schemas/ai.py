from pydantic import BaseModel


class AIExplanationResponse(BaseModel):
    calculation_id: int
    explanation: str