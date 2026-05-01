from app.schemas.strip_foundation import StripFoundationInput
from app.services.strip_foundation_service import calculate_strip_foundation


def test_calculate_strip_foundation_returns_correct_values():
    data = StripFoundationInput(
        length=10,
        width=8,
        foundation_width=0.4,
        foundation_depth=0.6,
        reserve_percent=10,
    )

    result = calculate_strip_foundation(data)

    assert result.perimeter == 36
    assert result.concrete_volume == 8.64
    assert result.concrete_volume_with_reserve == 9.5


def test_calculate_strip_foundation_with_zero_reserve():
    data = StripFoundationInput(
        length=10,
        width=8,
        foundation_width=0.4,
        foundation_depth=0.6,
        reserve_percent=0,
    )

    result = calculate_strip_foundation(data)

    assert result.perimeter == 36
    assert result.concrete_volume == 8.64
    assert result.concrete_volume_with_reserve == 8.64