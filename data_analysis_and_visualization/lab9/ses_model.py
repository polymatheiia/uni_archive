"""
Exponential Smoothing Models for Poland and Ukraine Temperature Data
Student: [Your Name]

Using Holt-Winters (seasonal exponential smoothing) because data has:
- Trend (upward temperature trend)
- Seasonality (monthly patterns)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('/mnt/user-data/uploads/temperatures_clean.csv')

# Get Poland and Ukraine data
poland = df[df['Country'] == 'Poland'].sort_values(['year', 'month']).reset_index(drop=True)
ukraine = df[df['Country'] == 'Ukraine'].sort_values(['year', 'month']).reset_index(drop=True)

poland_temps = poland['AverageTemperatureCelsius'].values
ukraine_temps = ukraine['AverageTemperatureCelsius'].values

print("Data loaded:")
print(f"Poland: {len(poland_temps)} observations")
print(f"Ukraine: {len(ukraine_temps)} observations")

# Split train/test (80/20)
train_size_poland = int(len(poland_temps) * 0.8)
train_size_ukraine = int(len(ukraine_temps) * 0.8)

poland_train = poland_temps[:train_size_poland]
poland_test = poland_temps[train_size_poland:]

ukraine_train = ukraine_temps[:train_size_ukraine]
ukraine_test = ukraine_temps[train_size_ukraine:]

print(f"\nTrain size: Poland={len(poland_train)}, Ukraine={len(ukraine_train)}")
print(f"Test size: Poland={len(poland_test)}, Ukraine={len(ukraine_test)}")

# =============================================================================
# HOLT-WINTERS (TRIPLE EXPONENTIAL SMOOTHING)
# =============================================================================
print("\n" + "="*70)
print("HOLT-WINTERS EXPONENTIAL SMOOTHING")
print("="*70)
print("This is seasonal ES that handles trend + seasonality")

# Poland - Holt-Winters
print("\nFitting Poland Holt-Winters model...")
poland_hw = ExponentialSmoothing(
    poland_train,
    seasonal_periods=12,  # monthly seasonality
    trend='add',          # additive trend
    seasonal='add',       # additive seasonality
    damped_trend=False
)
poland_hw_fit = poland_hw.fit()

poland_hw_forecast = poland_hw_fit.forecast(steps=len(poland_test))
poland_hw_rmse = np.sqrt(np.mean((poland_test - poland_hw_forecast)**2))

print(f"Poland RMSE: {poland_hw_rmse:.4f}")
print(f"AIC: {poland_hw_fit.aic:.2f}")

# Ukraine - Holt-Winters
print("\nFitting Ukraine Holt-Winters model...")
ukraine_hw = ExponentialSmoothing(
    ukraine_train,
    seasonal_periods=12,
    trend='add',
    seasonal='add',
    damped_trend=False
)
ukraine_hw_fit = ukraine_hw.fit()

ukraine_hw_forecast = ukraine_hw_fit.forecast(steps=len(ukraine_test))
ukraine_hw_rmse = np.sqrt(np.mean((ukraine_test - ukraine_hw_forecast)**2))

print(f"Ukraine RMSE: {ukraine_hw_rmse:.4f}")
print(f"AIC: {ukraine_hw_fit.aic:.2f}")

# =============================================================================
# TRY DIFFERENT CONFIGURATIONS
# =============================================================================
print("\n" + "="*70)
print("TRYING DIFFERENT CONFIGURATIONS")
print("="*70)

configs = [
    ('add', 'add', False),   # additive trend, additive seasonal
    ('add', 'mul', False),   # additive trend, multiplicative seasonal
    ('add', 'add', True),    # additive trend, additive seasonal, damped
]

poland_results = []
for trend, seasonal, damped in configs:
    try:
        model = ExponentialSmoothing(
            poland_train,
            seasonal_periods=12,
            trend=trend,
            seasonal=seasonal,
            damped_trend=damped
        )
        fit = model.fit()
        forecast = fit.forecast(steps=len(poland_test))
        rmse = np.sqrt(np.mean((poland_test - forecast)**2))
        
        config_name = f"trend={trend}, seasonal={seasonal}, damped={damped}"
        print(f"\nPoland - {config_name}")
        print(f"  RMSE: {rmse:.4f}, AIC: {fit.aic:.2f}")
        
        poland_results.append({
            'config': config_name,
            'rmse': rmse,
            'aic': fit.aic,
            'forecast': forecast
        })
    except Exception as e:
        print(f"Failed for {config_name}: {e}")

# Find best configuration for Poland
best_poland = min(poland_results, key=lambda x: x['rmse'])
print(f"\nBest Poland config: {best_poland['config']}")
print(f"RMSE: {best_poland['rmse']:.4f}")

# Do same for Ukraine
ukraine_results = []
for trend, seasonal, damped in configs:
    try:
        model = ExponentialSmoothing(
            ukraine_train,
            seasonal_periods=12,
            trend=trend,
            seasonal=seasonal,
            damped_trend=damped
        )
        fit = model.fit()
        forecast = fit.forecast(steps=len(ukraine_test))
        rmse = np.sqrt(np.mean((ukraine_test - forecast)**2))
        
        config_name = f"trend={trend}, seasonal={seasonal}, damped={damped}"
        print(f"\nUkraine - {config_name}")
        print(f"  RMSE: {rmse:.4f}, AIC: {fit.aic:.2f}")
        
        ukraine_results.append({
            'config': config_name,
            'rmse': rmse,
            'aic': fit.aic,
            'forecast': forecast
        })
    except Exception as e:
        print(f"Failed for {config_name}: {e}")

best_ukraine = min(ukraine_results, key=lambda x: x['rmse'])
print(f"\nBest Ukraine config: {best_ukraine['config']}")
print(f"RMSE: {best_ukraine['rmse']:.4f}")

# =============================================================================
# PLOTS
# =============================================================================

# Poland plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Basic Holt-Winters
ax1.plot(range(len(poland_test)), poland_test, label='Actual', linewidth=2)
ax1.plot(range(len(poland_hw_forecast)), poland_hw_forecast,
         label=f'Holt-Winters (basic) - RMSE={poland_hw_rmse:.3f}',
         linewidth=2, linestyle='--')
ax1.set_title('Poland - Basic Holt-Winters', fontsize=12, fontweight='bold')
ax1.set_xlabel('Time (months in test period)')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Best configuration
ax2.plot(range(len(poland_test)), poland_test, label='Actual', linewidth=2)
ax2.plot(range(len(best_poland['forecast'])), best_poland['forecast'],
         label=f"Best config - RMSE={best_poland['rmse']:.3f}",
         linewidth=2, linestyle='--', color='green')
ax2.set_title(f"Poland - Best Config: {best_poland['config']}", fontsize=12, fontweight='bold')
ax2.set_xlabel('Time (months in test period)')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/poland_exponential_smoothing.png', dpi=150)
print("\nSaved poland_exponential_smoothing.png")
plt.close()

# Ukraine plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Basic Holt-Winters
ax1.plot(range(len(ukraine_test)), ukraine_test, label='Actual', linewidth=2)
ax1.plot(range(len(ukraine_hw_forecast)), ukraine_hw_forecast,
         label=f'Holt-Winters (basic) - RMSE={ukraine_hw_rmse:.3f}',
         linewidth=2, linestyle='--')
ax1.set_title('Ukraine - Basic Holt-Winters', fontsize=12, fontweight='bold')
ax1.set_xlabel('Time (months in test period)')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Best configuration
ax2.plot(range(len(ukraine_test)), ukraine_test, label='Actual', linewidth=2)
ax2.plot(range(len(best_ukraine['forecast'])), best_ukraine['forecast'],
         label=f"Best config - RMSE={best_ukraine['rmse']:.3f}",
         linewidth=2, linestyle='--', color='green')
ax2.set_title(f"Ukraine - Best Config: {best_ukraine['config']}", fontsize=12, fontweight='bold')
ax2.set_xlabel('Time (months in test period)')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/ukraine_exponential_smoothing.png', dpi=150)
print("Saved ukraine_exponential_smoothing.png")
plt.close()

# Save results
results = pd.DataFrame({
    'Country': ['Poland', 'Poland', 'Ukraine', 'Ukraine'],
    'Model': ['Holt-Winters (basic)', f"Holt-Winters ({best_poland['config']})",
              'Holt-Winters (basic)', f"Holt-Winters ({best_ukraine['config']})"],
    'RMSE': [poland_hw_rmse, best_poland['rmse'], ukraine_hw_rmse, best_ukraine['rmse']],
    'AIC': [poland_hw_fit.aic, best_poland['aic'], ukraine_hw_fit.aic, best_ukraine['aic']]
})

results.to_csv('/mnt/user-data/outputs/exponential_smoothing_results.csv', index=False)
print("Saved exponential_smoothing_results.csv")

print("\n" + "="*70)
print("DONE!")
print("="*70)
print("\nNote: Holt-Winters is the 'fancy' version of simple exponential smoothing")
print("that handles both trend and seasonality - perfect for temperature data!")
