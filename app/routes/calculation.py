from fastapi import APIRouter, HTTPException, status
from app.schemas.calculation import CalculationResponse, CalculationInput
from app.services.calculation_service import calculate_room, perimeter

router = APIRouter(tags=["Calculation"])


@router.post("/calculate", response_model=CalculationResponse)
def calculate(data: CalculationInput):
    wall_area_before_openings = perimeter(data.length, data.width) * data.height

    if data.doors_area + data.windows_area > wall_area_before_openings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Windows and doors area cannot exceed total wall area",
        )

    response = calculate_room(data)
    return response