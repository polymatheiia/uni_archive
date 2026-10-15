"""
VAR Model for Poland and Ukraine Temperature Data
Student: [Your Name]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import grangercausalitytests
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('/mnt/user-data/uploads/temperatures_clean.csv')

# Get Poland and Ukraine data
poland = df[df['Country'] == 'Poland'].sort_values(['year', 'month']).reset_index(drop=True)
ukraine = df[df['Country'] == 'Ukraine'].sort_values(['year', 'month']).reset_index(drop=True)

# VAR needs equal length series - use Poland's length (shorter)
poland_temps = poland['AverageTemperatureCelsius'].values
ukraine_temps = ukraine['AverageTemperatureCelsius'].values[:len(poland_temps)]

print("Data loaded:")
print(f"Poland: {len(poland_temps)} observations")
print(f"Ukraine: {len(ukraine_temps)} observations")

# Create dataframe with both series
data = pd.DataFrame({
    'Poland': poland_temps,
    'Ukraine': ukraine_temps
})

print(f"\nCombined dataset shape: {data.shape}")

# Split train/test (80/20)
train_size = int(len(data) * 0.8)
train = data[:train_size]
test = data[train_size:]

print(f"Train size: {len(train)}")
print(f"Test size: {len(test)}")

# =============================================================================
# FIT VAR MODEL
# =============================================================================
print("\n" + "="*70)
print("VAR MODEL")
print("="*70)

# Try different lags and find best AIC
print("\nFinding best lag order...")
model = VAR(train)
results = []
for lag in range(1, 13):
    try:
        fit = model.fit(lag)
        results.append({'lag': lag, 'AIC': fit.aic, 'BIC': fit.bic})
    except:
        pass

results_df = pd.DataFrame(results)
best_lag = results_df.loc[results_df['AIC'].idxmin(), 'lag']
print(f"\nBest lag by AIC: {int(best_lag)}")
print(results_df.to_string(index=False))

# Fit final model with best lag
print(f"\nFitting VAR({int(best_lag)})...")
var_model = model.fit(int(best_lag))

print("\nModel Summary:")
print(f"AIC: {var_model.aic:.2f}")
print(f"BIC: {var_model.bic:.2f}")

# Forecast
forecast = var_model.forecast(train.values[-int(best_lag):], steps=len(test))
forecast_df = pd.DataFrame(forecast, columns=['Poland', 'Ukraine'])

# Calculate RMSE for each country
poland_rmse = np.sqrt(np.mean((test['Poland'].values - forecast_df['Poland'].values)**2))
ukraine_rmse = np.sqrt(np.mean((test['Ukraine'].values - forecast_df['Ukraine'].values)**2))

print(f"\nForecast Performance:")
print(f"Poland RMSE: {poland_rmse:.4f}")
print(f"Ukraine RMSE: {ukraine_rmse:.4f}")

# =============================================================================
# GRANGER CAUSALITY TEST
# =============================================================================
print("\n" + "="*70)
print("GRANGER CAUSALITY TEST")
print("="*70)
print("Testing if one country's temperatures help predict the other's")

print("\nDoes Ukraine -> Poland?")
try:
    gc_result = grangercausalitytests(data[['Poland', 'Ukraine']], maxlag=4, verbose=False)
    p_val = gc_result[1][0]['ssr_ftest'][1]
    print(f"  p-value (lag 1): {p_val:.4f}")
    if p_val < 0.05:
        print("  Result: YES, Ukraine helps predict Poland (p < 0.05)")
    else:
        print("  Result: NO, Ukraine does not help predict Poland")
except Exception as e:
    print(f"  Could not compute: {e}")

print("\nDoes Poland -> Ukraine?")
try:
    gc_result = grangercausalitytests(data[['Ukraine', 'Poland']], maxlag=4, verbose=False)
    p_val = gc_result[1][0]['ssr_ftest'][1]
    print(f"  p-value (lag 1): {p_val:.4f}")
    if p_val < 0.05:
        print("  Result: YES, Poland helps predict Ukraine (p < 0.05)")
    else:
        print("  Result: NO, Poland does not help predict Ukraine")
except Exception as e:
    print(f"  Could not compute: {e}")

# =============================================================================
# PLOTS
# =============================================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Poland
ax1.plot(range(len(test)), test['Poland'].values, label='Actual', linewidth=2)
ax1.plot(range(len(forecast_df)), forecast_df['Poland'].values,
         label=f'VAR({int(best_lag)}) Forecast - RMSE={poland_rmse:.3f}',
         linewidth=2, linestyle='--')
ax1.set_title('Poland - VAR Model Forecast', fontsize=12, fontweight='bold')
ax1.set_xlabel('Time (months in test period)')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Ukraine
ax2.plot(range(len(test)), test['Ukraine'].values, label='Actual', linewidth=2)
ax2.plot(range(len(forecast_df)), forecast_df['Ukraine'].values,
         label=f'VAR({int(best_lag)}) Forecast - RMSE={ukraine_rmse:.3f}',
         linewidth=2, linestyle='--')
ax2.set_title('Ukraine - VAR Model Forecast', fontsize=12, fontweight='bold')
ax2.set_xlabel('Time (months in test period)')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/var_model.png', dpi=150)
print("\nSaved var_model.png")
plt.close()

# Save results
results_summary = pd.DataFrame({
    'Country': ['Poland', 'Ukraine'],
    'Model': [f'VAR({int(best_lag)})', f'VAR({int(best_lag)})'],
    'RMSE': [poland_rmse, ukraine_rmse],
    'AIC': [var_model.aic, var_model.aic],
    'BIC': [var_model.bic, var_model.bic]
})

results_summary.to_csv('/mnt/user-data/outputs/var_results.csv', index=False)
results_df.to_csv('/mnt/user-data/outputs/var_lag_selection.csv', index=False)
print("Saved var_results.csv")
print("Saved var_lag_selection.csv")

print("\n" + "="*70)
print("DONE!")
print("="*70)
