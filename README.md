# Suicide Rate Analysis

A comprehensive Python data analysis pipeline for global suicide rates, focusing on time series analysis, correlation with socio-economic factors (GDP per capita, population), and forecasting.

## Features
- Cleans and prepares diverse datasets (wide/long format, robust column handling)
- Generates clear visualizations:
  - Time series plots by age, gender, and country
  - Correlation heatmap (suicide rate, GDP per capita, population)
  - Forecast plots (moving average, linear regression)
- All outputs saved as PNGs in the `visualization/` folder
- Modular, reproducible, and well-documented code

## How to Use
1. Place your suicide rate and `gdp_population.csv` data files in the project folder.
2. Run `python suicide_rate_analysis.py`.
3. View results and insights in the `visualization/` folder and `INSIGHTS.md`.

## Requirements
- Python 3.7+
- pandas, numpy, matplotlib, seaborn, scikit-learn, statsmodels

## Author
MoAJ-ML

---

*For questions or improvements, open an issue or pull request!*
