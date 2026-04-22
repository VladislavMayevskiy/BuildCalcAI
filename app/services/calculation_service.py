from app.schemas.calculation import CalculationInput, CalculationResponse


def floor(length: float, width: float ) -> float:
    return length * width


def ceiling(length: float, width: float ) -> float:
    return length * width

def perimeter(length: float, width: float ) -> float:
    return 2 * (length + width)

def walls(perimeter_value: float, height: float, windows_area: float, doors_area: float) -> float:
    return perimeter_value * height - windows_area - doors_area


def calculate_room(data: CalculationInput) -> CalculationResponse:
    floor_area = floor(data.length, data.width)
    ceiling_area = ceiling(data.length, data.width)
    perimeter_value = perimeter(data.length, data.width)
    wall_area = walls(perimeter_value, data.height, data.windows_area, data.doors_area)
    wall_area_with_reserve=round(wall_area * 1.1, 2)
    paint_liters = wall_area_with_reserve / 9
    return CalculationResponse( 
        floor_area=floor_area,
        ceiling_area=ceiling_area,
        wall_area=wall_area,
        wall_area_with_reserve=wall_area_with_reserve,
        paint_liters=paint_liters
)