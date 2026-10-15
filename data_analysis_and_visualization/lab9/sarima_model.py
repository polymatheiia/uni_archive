"""
SARIMA Model for Poland and Ukraine Temperature Data
Student: [Your Name]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('./temperatures_clean.csv')

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
# OPTION 1: Manual SARIMA
# =============================================================================
print("\n" + "="*70)
print("MANUAL SARIMA MODEL")
print("="*70)

# Poland SARIMA(1,1,1)(1,1,1,12)
print("\nFitting Poland SARIMA(1,1,1)(1,1,1,12)...")
poland_sarima = SARIMAX(poland_train, 
                        order=(1,1,1), 
                        seasonal_order=(1,1,1,12),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
poland_sarima_fit = poland_sarima.fit(disp=False)

poland_forecast = poland_sarima_fit.forecast(steps=len(poland_test))
poland_rmse = np.sqrt(np.mean((poland_test - poland_forecast)**2))

print(f"Poland RMSE: {poland_rmse:.4f}")
print(f"AIC: {poland_sarima_fit.aic:.2f}, BIC: {poland_sarima_fit.bic:.2f}")

# Ukraine SARIMA(1,1,1)(1,1,1,12)
print("\nFitting Ukraine SARIMA(1,1,1)(1,1,1,12)...")
ukraine_sarima = SARIMAX(ukraine_train,
                         order=(1,1,1),
                         seasonal_order=(1,1,1,12),
                         enforce_stationarity=False,
                         enforce_invertibility=False)
ukraine_sarima_fit = ukraine_sarima.fit(disp=False)

ukraine_forecast = ukraine_sarima_fit.forecast(steps=len(ukraine_test))
ukraine_rmse = np.sqrt(np.mean((ukraine_test - ukraine_forecast)**2))

print(f"Ukraine RMSE: {ukraine_rmse:.4f}")
print(f"AIC: {ukraine_sarima_fit.aic:.2f}, BIC: {ukraine_sarima_fit.bic:.2f}")

# =============================================================================
# OPTION 2: AUTO SARIMA (like auto.arima in R)
# =============================================================================
print("\n" + "="*70)
print("AUTO SARIMA MODEL (automatic parameter selection)")
print("="*70)

try:
    from pmdarima import auto_arima
except:
    print("Installing pmdarima...")
    import subprocess
    subprocess.run(['pip', 'install', 'pmdarima', '--break-system-packages', '-q'])
    from pmdarima import auto_arima

# Poland auto SARIMA
print("\nFinding best SARIMA for Poland (this takes a minute)...")
poland_auto = auto_arima(poland_train,
                         seasonal=True,
                         m=12,  # monthly seasonality
                         max_p=3, max_q=3,
                         max_P=2, max_Q=2,
                         max_d=2, max_D=1,
                         trace=False,
                         stepwise=True,
                         suppress_warnings=True)

print(f"Best model for Poland: {poland_auto.order} x {poland_auto.seasonal_order}")
poland_auto_forecast = poland_auto.predict(n_periods=len(poland_test))
poland_auto_rmse = np.sqrt(np.mean((poland_test - poland_auto_forecast)**2))
print(f"RMSE: {poland_auto_rmse:.4f}")

# Ukraine auto SARIMA
print("\nFinding best SARIMA for Ukraine (this takes a minute)...")
ukraine_auto = auto_arima(ukraine_train,
                          seasonal=True,
                          m=12,
                          max_p=3, max_q=3,
                          max_P=2, max_Q=2,
                          max_d=2, max_D=1,
                          trace=False,
                          stepwise=True,
                          suppress_warnings=True)

print(f"Best model for Ukraine: {ukraine_auto.order} x {ukraine_auto.seasonal_order}")
ukraine_auto_forecast = ukraine_auto.predict(n_periods=len(ukraine_test))
ukraine_auto_rmse = np.sqrt(np.mean((ukraine_test - ukraine_auto_forecast)**2))
print(f"RMSE: {ukraine_auto_rmse:.4f}")

# =============================================================================
# PLOTS
# =============================================================================

# Poland plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Manual SARIMA
ax1.plot(range(len(poland_test)), poland_test, label='Actual', linewidth=2)
ax1.plot(range(len(poland_forecast)), poland_forecast, 
         label=f'Manual SARIMA(1,1,1)(1,1,1,12) - RMSE={poland_rmse:.3f}', 
         linewidth=2, linestyle='--')
ax1.set_title('Poland - Manual SARIMA', fontsize=12, fontweight='bold')
ax1.set_xlabel('Time (months in test period)')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Auto SARIMA
ax2.plot(range(len(poland_test)), poland_test, label='Actual', linewidth=2)
ax2.plot(range(len(poland_auto_forecast)), poland_auto_forecast,
         label=f'Auto SARIMA{poland_auto.order}x{poland_auto.seasonal_order} - RMSE={poland_auto_rmse:.3f}',
         linewidth=2, linestyle='--', color='green')
ax2.set_title('Poland - Auto SARIMA', fontsize=12, fontweight='bold')
ax2.set_xlabel('Time (months in test period)')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./poland_sarima.png', dpi=150)
print("\nSaved poland_sarima.png")
plt.close()

# Ukraine plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Manual SARIMA
ax1.plot(range(len(ukraine_test)), ukraine_test, label='Actual', linewidth=2)
ax1.plot(range(len(ukraine_forecast)), ukraine_forecast,
         label=f'Manual SARIMA(1,1,1)(1,1,1,12) - RMSE={ukraine_rmse:.3f}',
         linewidth=2, linestyle='--')
ax1.set_title('Ukraine - Manual SARIMA', fontsize=12, fontweight='bold')
ax1.set_xlabel('Time (months in test period)')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Auto SARIMA
ax2.plot(range(len(ukraine_test)), ukraine_test, label='Actual', linewidth=2)
ax2.plot(range(len(ukraine_auto_forecast)), ukraine_auto_forecast,
         label=f'Auto SARIMA{ukraine_auto.order}x{ukraine_auto.seasonal_order} - RMSE={ukraine_auto_rmse:.3f}',
         linewidth=2, linestyle='--', color='green')
ax2.set_title('Ukraine - Auto SARIMA', fontsize=12, fontweight='bold')
ax2.set_xlabel('Time (months in test period)')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./ukraine_sarima.png', dpi=150)
print("Saved ukraine_sarima.png")
plt.close()

# Save results
results = pd.DataFrame({
    'Country': ['Poland', 'Poland', 'Ukraine', 'Ukraine'],
    'Model': ['Manual SARIMA(1,1,1)(1,1,1,12)',
              f'Auto SARIMA{poland_auto.order}x{poland_auto.seasonal_order}',
              'Manual SARIMA(1,1,1)(1,1,1,12)',
              f'Auto SARIMA{ukraine_auto.order}x{ukraine_auto.seasonal_order}'],
    'RMSE': [poland_rmse, poland_auto_rmse, ukraine_rmse, ukraine_auto_rmse]
})

results.to_csv('./sarima_results.csv', index=False)
print("\nSaved sarima_results.csv")

print("\n" + "="*70)
print("DONE!")
print("="*70)
