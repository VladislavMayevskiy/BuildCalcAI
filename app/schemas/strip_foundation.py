from pydantic import BaseModel

#Стрічковий фундамент

class StripFoundationInput(BaseModel):
    length: float
    width: float
    foundation_width: float
    foundation_depth: float
    reserve_percent: float = 10

class StripFoundationResponse(BaseModel):
    perimeter: float
    concrete_volume: float
    concrete_volume_with_reserve: float

    