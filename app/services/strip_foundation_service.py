from app.schemas.strip_foundation import StripFoundationResponse, StripFoundationInput


def calculate_strip_foundation(data: StripFoundationInput) -> StripFoundationResponse:
    perimeter = 2 * (data.width + data.length)
    concrete_volume = perimeter * data.foundation_depth * data.foundation_width
    concrete_volume_with_reserve = concrete_volume * (1 + data.reserve_percent / 100)

    return StripFoundationResponse(
        perimeter=round(perimeter, 2),
        concrete_volume=round(concrete_volume, 2),
        concrete_volume_with_reserve=round(concrete_volume_with_reserve, 2)
    )