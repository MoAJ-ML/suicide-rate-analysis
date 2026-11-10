# Suicide Rate Data Exploration

This repository explores historical country-level crude suicide rates and visualizes descriptive associations with GDP per capita and population. It does not forecast future rates or identify causal effects. The analyses are educational and must not be used for health decisions.

## Inputs and units

The executed pipeline reads `SDGSUICIDE.csv`, whose header states **crude suicide rates per 100,000 population** for 2000, 2005, 2010 and 2015. It may left-join `gdp_population.csv` on country and year; only the **Both sexes** rate is used for that correlation so male, female and combined rows are not treated as independent country-years. The GDP file does not state its publisher, currency basis or retrieval date in this repository. Other committed CSV/XLSX files have varying definitions and are not merged into the executed analysis. Their original publishers, revisions, licenses and units need to be recorded before combining them.

The country and gender curves are unweighted averages across available rows. They are not global population rates. The linear line in `trend_plot.png` is an **in-sample fit**, not an out-of-sample prediction. Correlations are descriptive and unadjusted for country, measurement differences and confounders.

## Reproduce

```bash
pip install -r requirements.txt
MPLBACKEND=Agg python suicide_rate_analysis.py
python -m unittest discover -s tests
```

Run from the repository root. Outputs are in `visualization/`. The previously committed `forecast_plot.png` and forecast language were misleading and have been removed. Source and license verification for the additional input files remains open.

No software license file is included. Suggested repository description: “Descriptive exploration of historical crude suicide-rate data with explicit units and provenance limits.”
