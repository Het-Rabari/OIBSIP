# BMI Calculator

A small command-line calculator that accepts an adult's weight in kilograms and height in centimeters, computes BMI, and displays the corresponding adult category.

## Run

From this folder, run:

    python bmi_calculator.py

Enter positive numeric values when prompted. The program keeps asking after invalid input and exits cleanly on Ctrl+C.

## Calculation

BMI is weight in kilograms divided by height in meters squared. The adult category cutoffs follow the World Health Organization's general ranges: below 18.5 is underweight, 18.5 to below 25 is normal weight, 25 to below 30 is overweight, and 30 or above is obesity.

BMI is a screening measure and does not account for factors such as age, body composition, or pregnancy. It is not a diagnosis, and these categories are not intended for children or adolescents. See the [WHO overview of overweight and obesity](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight).

## Check

Run:

    python -m unittest -v

The tests cover the calculation, category boundaries, and invalid values.
