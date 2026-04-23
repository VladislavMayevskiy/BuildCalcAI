from pydantic import BaseModel, Field


class CalculationInput(BaseModel):
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    windows_area: float = Field(..., ge=0)
    doors_area: float = Field(..., ge=0)


class CalculationResponse(BaseModel):
    floor_area: float
    ceiling_area: float
    wall_area: float
    wall_area_with_reserve: float
    paint_liters: float
    tile_required_sqm: float