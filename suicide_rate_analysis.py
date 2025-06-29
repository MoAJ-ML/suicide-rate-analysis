import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.api import SimpleExpSmoothing

# --- CONFIG ---
DATA_FILES = {
    'by_country': 'suicide-rates-by-country.csv',
    'by_age': 'suicide_by_age.csv',
    'by_gender': 'gender_rates.csv',
    'main': 'SDGSUICIDE.csv',
}
VIS_DIR = 'visualization'

# --- UTILS ---
def ensure_vis_dir():
    if not os.path.exists(VIS_DIR):
        os.makedirs(VIS_DIR)

# --- DATA LOADING ---
def load_data():
    # Try to load the most comprehensive file, fallback to others if needed
    for key, fname in DATA_FILES.items():
        if os.path.exists(fname):
            print(f"Loaded {fname} for '{key}' analysis.")
    # Try SDGSUICIDE.csv (wide format, needs melting)
    if os.path.exists(DATA_FILES['main']):
        # SDGSUICIDE.csv has a metadata row, actual header is second row
        df = pd.read_csv(DATA_FILES['main'], skiprows=1)
        # Strip spaces from column names
        df.columns = [c.strip() for c in df.columns]
        # Check if it is wide format (years as columns)
        year_cols = [c for c in df.columns if any(str(y) in c for y in [2000,2005,2010,2015])]
        id_vars = [c for c in df.columns if c.lower() in ['country', 'sex']]
        if year_cols and id_vars:
            df_long = df.melt(id_vars=id_vars, value_vars=year_cols, var_name='year', value_name='suicide_rate')
            df_long['year'] = df_long['year'].astype(str).str.extract(r'(\d{4})').astype(int)
            df_long['suicide_rate'] = pd.to_numeric(df_long['suicide_rate'], errors='coerce')
            df_long.columns = [c.strip().lower().replace(' ', '_') for c in df_long.columns]
            return df_long
        else:
            # Already long format or unexpected format
            df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            return df
    # Fallback: try by_country (already long format)
    if os.path.exists(DATA_FILES['by_country']):
        df = pd.read_csv(DATA_FILES['by_country'])
        # Rename columns for consistency
        col_map = {}
        for c in df.columns:
            if c.lower() in ['year']:
                col_map[c] = 'year'
            if 'suicide rate' in c.lower():
                col_map[c] = 'suicide_rate'
        df = df.rename(columns=col_map)
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        return df
    raise FileNotFoundError("No suitable dataset found.")


def merge_with_gdp_population(suicide_df):
    """
    Merge suicide data with GDP and population data on country and year.
    Cleans country names and ensures correct numeric types.
    """
    gdp_pop_path = 'gdp_population.csv'
    if not os.path.exists(gdp_pop_path):
        print('GDP/Population file missing!')
        return suicide_df
    gdp_df = pd.read_csv(gdp_pop_path)
    # Clean column names
    gdp_df.columns = [c.strip().lower().replace(' ', '_') for c in gdp_df.columns]
    # Clean country names for both
    suicide_df['country'] = suicide_df['country'].str.strip().str.lower()
    gdp_df['country'] = gdp_df['country'].str.strip().str.lower()
    # Ensure year is int
    suicide_df['year'] = suicide_df['year'].astype(int)
    gdp_df['year'] = gdp_df['year'].astype(int)
    # Merge
    merged = pd.merge(suicide_df, gdp_df, on=['country', 'year'], how='left')
    if merged[['gdp_per_capita', 'population']].isnull().all(axis=None):
        print('Merge failed: No GDP/Population data matched. Check country/year alignment.')
    return merged


# --- DATA CLEANING ---
def clean_data(df):
    # Standardize column names
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    # Try to find year and suicide_rate columns
    year_col = None
    rate_col = None
    for c in df.columns:
        if 'year' in c:
            year_col = c
        if 'suicide_rate' in c or 'suicide rate' in c:
            rate_col = c
    if not year_col or not rate_col:
        raise ValueError(f"Could not find 'year' or 'suicide_rate' columns in columns: {df.columns.tolist()}")
    # Handle missing values
    df = df.dropna(subset=[year_col, rate_col])
    # Convert year to int
    df[year_col] = df[year_col].astype(int)
    df[rate_col] = pd.to_numeric(df[rate_col], errors='coerce')
    # Rename to standard
    df = df.rename(columns={year_col: 'year', rate_col: 'suicide_rate'})
    return df

# --- TIME SERIES ANALYSIS ---
def plot_suicide_trends(df):
    """
    Enhanced time series plot: shows suicide rates by gender and by top 3 countries in separate subplots.
    Uses distinct colors and clear labeling for maximum readability.
    """
    import matplotlib.cm as cm
    import matplotlib.ticker as ticker
    # Check for necessary columns
    if 'year' not in df.columns or 'suicide_rate' not in df.columns:
        print('Required columns missing for time series plot.')
        return
    # Prepare data
    top_countries = df.groupby('country')['suicide_rate'].mean().sort_values(ascending=False).head(3).index.tolist() if 'country' in df.columns else []
    sexes = df['sex'].unique() if 'sex' in df.columns else []
    # Setup subplots
    nrows = 1 + (1 if top_countries else 0)
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(13, 6*nrows), dpi=220)
    if nrows == 1:
        axes = [axes]
    # Plot by gender
    if sexes is not None and len(sexes) > 0:
        ax = axes[0]
        color_map = cm.get_cmap('Set1', len(sexes))
        for i, sex in enumerate(sexes):
            sub = df[df['sex'] == sex]
            if sub.empty:
                continue
            sub_grouped = sub.groupby('year')['suicide_rate'].mean()
            ax.plot(sub_grouped.index, sub_grouped.values, marker='o', label=str(sex), color=color_map(i))
        ax.set_title('Suicide Rates by Gender (Global Average)', fontsize=18)
        ax.set_xlabel('Year', fontsize=15)
        ax.set_ylabel('Suicide Rate', fontsize=15)
        ax.legend(title='Gender', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    # Plot by top 3 countries
    if top_countries:
        ax = axes[1]
        color_map = cm.get_cmap('tab10', len(top_countries))
        for i, country in enumerate(top_countries):
            sub = df[df['country'] == country]
            if sub.empty:
                continue
            sub_grouped = sub.groupby('year')['suicide_rate'].mean()
            ax.plot(sub_grouped.index, sub_grouped.values, marker='o', label=str(country), color=color_map(i))
        ax.set_title('Suicide Rates by Country (Top 3)', fontsize=18)
        ax.set_xlabel('Year', fontsize=15)
        ax.set_ylabel('Suicide Rate', fontsize=15)
        ax.legend(title='Country', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, 'suicide_by_age_gender_country.png'), dpi=220)
    plt.close()


# --- CORRELATION ANALYSIS ---
def plot_correlation_heatmap(df):
    """
    Enhanced heatmap with larger font, clear colorbar, and value annotations.
    Now uses merged data with GDP per capita and population.
    """
    corr_cols = ['suicide_rate']
    if 'gdp_per_capita' in df.columns:
        corr_cols.append('gdp_per_capita')
    if 'population' in df.columns:
        corr_cols.append('population')
    # Only use rows where all correlation columns are present
    corr_df = df[corr_cols].dropna()
    if len(corr_cols) < 2 or corr_df.shape[0] == 0:
        print('Not enough variables or data for correlation heatmap.')
        return
    corr = corr_df.corr()
    if corr.shape[0] < 2:
        print('Not enough variables for correlation heatmap.')
        return
    plt.figure(figsize=(7, 6), dpi=220)
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        cbar_kws={'shrink': 0.8, 'label': 'Correlation'},
        annot_kws={"size": 15}
    )
    plt.title('Correlation Heatmap: Suicide Rate, GDP per Capita, Population', fontsize=17)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, 'correlation_heatmap.png'), dpi=220)
    plt.close()



# --- FORECASTING ---
def plot_forecast(df):
    """
    Enhanced forecast plot with markers, grid, and highlighted regression line.
    """
    import matplotlib.cm as cm
    # Aggregate by year
    yearly = df.groupby('year')['suicide_rate'].mean().reset_index()
    if yearly.empty:
        print('No data for forecast plot.')
        return
    # Moving average
    yearly['ma'] = yearly['suicide_rate'].rolling(window=3, min_periods=1).mean()
    # Linear regression
    X = yearly['year'].values.reshape(-1, 1)
    y = yearly['suicide_rate'].values
    model = LinearRegression().fit(X, y)
    yearly['regression'] = model.predict(X)
    # Plot
    plt.figure(figsize=(11, 7), dpi=220)
    plt.plot(yearly['year'], yearly['suicide_rate'], marker='o', label='Actual', color='tab:blue', linewidth=2)
    plt.plot(yearly['year'], yearly['ma'], marker='s', label='Moving Avg (3yr)', color='tab:orange', linestyle='--', linewidth=2)
    plt.plot(yearly['year'], yearly['regression'], label='Linear Regression', color='tab:red', linewidth=3, linestyle='-')
    plt.title('Forecast of Suicide Rates (Global Average)', fontsize=18)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Suicide Rate', fontsize=15)
    plt.legend(fontsize=13)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, 'forecast_plot.png'), dpi=220)
    plt.close()


# --- MAIN ---
def main():
    ensure_vis_dir()
    df = load_data()
    df = clean_data(df)
    merged_df = merge_with_gdp_population(df)
    plot_suicide_trends(df)
    plot_correlation_heatmap(merged_df)
    plot_forecast(df)
    print("All plots generated in 'visualization/' directory.")


if __name__ == '__main__':
    main()
