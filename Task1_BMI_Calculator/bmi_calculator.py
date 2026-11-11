"""Command-line BMI calculator for adults."""

from __future__ import annotations

import math


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Return BMI from kilograms and centimeters.

    Raises ValueError when either measurement is non-finite or not positive.
    """
    try:
        weight = float(weight_kg)
        height = float(height_cm)
    except (TypeError, ValueError) as exc:
        raise ValueError("Weight and height must be numbers.") from exc

    if not math.isfinite(weight) or not math.isfinite(height):
        raise ValueError("Weight and height must be finite numbers.")
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be greater than zero.")

    height_m = height / 100
    return weight / (height_m * height_m)


def bmi_category(bmi: float) -> str:
    """Return the general WHO adult BMI category for a positive BMI value."""
    try:
        value = float(bmi)
    except (TypeError, ValueError) as exc:
        raise ValueError("BMI must be a number.") from exc

    if not math.isfinite(value) or value <= 0:
        raise ValueError("BMI must be a finite number greater than zero.")
    if value < 18.5:
        return "Underweight"
    if value < 25:
        return "Normal weight"
    if value < 30:
        return "Overweight"
    return "Obesity"


def read_positive_number(prompt: str) -> float:
    """Prompt until a finite, positive number is entered."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("Please enter a number.")
            continue
        if not math.isfinite(value) or value <= 0:
            print("Please enter a finite number greater than zero.")
            continue
        return value


def main() -> None:
    print("Adult BMI Calculator")
    try:
        weight = read_positive_number("Weight in kilograms: ")
        height = read_positive_number("Height in centimeters: ")
    except (EOFError, KeyboardInterrupt):
        print("\nNo calculation made.")
        return

    bmi = calculate_bmi(weight, height)
    print(f"\nBMI: {bmi:.1f}")
    print(f"Category: {bmi_category(bmi)}")
    print("This adult screening measure is not a medical diagnosis.")


if __name__ == "__main__":
    main()
