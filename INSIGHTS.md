# Suicide Rate Analysis Insights

## 1. Time Series Trends
- The generated plot `suicide_by_age_gender_country.png` visualizes suicide rates over time, grouped by age, gender, and country (top 5 countries shown for clarity).
- Key Observations:
  - Suicide rates vary significantly by gender, with males generally exhibiting higher rates than females across most countries.
  - Certain countries show marked changes over the years, indicating socio-economic or policy shifts.

## 2. Correlation Analysis
- The `correlation_heatmap.png` shows the correlation between suicide rates, GDP per capita, and population (where available).
- Key Observations:
  - The strength and direction of correlation can highlight whether economic prosperity or population size has any association with suicide rates.
  - In this dataset, the correlation between suicide rate and GDP per capita/population is weak to moderate, suggesting other factors may play a more significant role.

## 3. Forecasting
- The `forecast_plot.png` shows actual suicide rates, a 3-year moving average, and a linear regression trendline.
- Key Observations:
  - Moving averages smooth out year-to-year fluctuations and help reveal underlying trends.
  - The regression line can be used for basic forecasting, showing the general direction (increase/decrease) in suicide rates over time.

## 4. Data Quality & Recommendations
- Data is aggregated and some files are wide-format (years as columns), requiring transformation for time series analysis.
- Some countries/years have missing data, which may affect trend accuracy.
- For deeper insights, consider integrating more granular data (e.g., by region, age group, or mental health policy changes).

---

All visual outputs are saved in the `visualization/` directory. For further analysis or custom plots, modify `suicide_rate_analysis.py` as needed.
