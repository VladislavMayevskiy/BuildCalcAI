
from typing import Any, Dict


def build_calculation_explanation_prompt(input_data: Dict[str, Any],result_data: Dict[str, Any]) -> str:
    prompt = f"""
You are a renovation calculation assistant.

Explain this room material calculation to the user in simple language.
Do not change the numbers.
Do not invent extra measurements.
Explain where each result comes from.
Respond in Ukrainian.

Input room data:
{input_data}

Calculation result:
{result_data}
"""
    return prompt