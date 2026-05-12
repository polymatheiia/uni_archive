import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import warnings

warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('./temperatures_clean.csv')

# Extract Poland and Ukraine data
poland_data = df[df['Country'] == 'Poland'].copy()
ukraine_data = df[df['Country'] == 'Ukraine'].copy()

# Sort by year and month
poland_data = poland_data.sort_values(['year', 'month']).reset_index(drop=True)
ukraine_data = ukraine_data.sort_values(['year', 'month']).reset_index(drop=True)

# Create time series
poland_ts = poland_data['AverageTemperatureCelsius'].values
ukraine_ts = ukraine_data['AverageTemperatureCelsius'].values

# Create datetime index for better plotting
poland_data['date'] = pd.to_datetime(poland_data[['year', 'month']].assign(day=1))
ukraine_data['date'] = pd.to_datetime(ukraine_data[['year', 'month']].assign(day=1))

# Save time series data
poland_df = poland_data[['date', 'year', 'month', 'AverageTemperatureCelsius']].copy()
ukraine_df = ukraine_data[['date', 'year', 'month', 'AverageTemperatureCelsius']].copy()

poland_df.to_csv('./poland_timeseries.csv', index=False)
ukraine_df.to_csv('./ukraine_timeseries.csv', index=False)

print("=" * 80)
print("TIME SERIES DATA PREPARATION")
print("=" * 80)
print(f"\nPoland time series: {len(poland_ts)} observations")
print(f"  Period: {poland_data['year'].min()} - {poland_data['year'].max()}")
print(f"  Mean temperature: {poland_ts.mean():.2f}°C")
print(f"  Std deviation: {poland_ts.std():.2f}°C")

print(f"\nUkraine time series: {len(ukraine_ts)} observations")
print(f"  Period: {ukraine_data['year'].min()} - {ukraine_data['year'].max()}")
print(f"  Mean temperature: {ukraine_ts.mean():.2f}°C")
print(f"  Std deviation: {ukraine_ts.std():.2f}°C")


# Stationarity test
def adf_test(series, name):
    result = adfuller(series, autolag='AIC')
    print(f"\n{name} - Augmented Dickey-Fuller Test:")
    print(f"  ADF Statistic: {result[0]:.4f}")
    print(f"  p-value: {result[1]:.4f}")
    print(f"  Critical Values:")
    for key, value in result[4].items():
        print(f"    {key}: {value:.4f}")
    if result[1] <= 0.05:
        print(f"  => Series is STATIONARY (reject H0)")
    else:
        print(f"  => Series is NON-STATIONARY (fail to reject H0)")
    return result[1] <= 0.05


print("\n" + "=" * 80)
print("STATIONARITY TESTS")
print("=" * 80)
poland_stationary = adf_test(poland_ts, "Poland")
ukraine_stationary = adf_test(ukraine_ts, "Ukraine")

# ============================================================================
# AR MODELS
# ============================================================================
print("\n" + "=" * 80)
print("AUTOREGRESSIVE (AR) MODELS")
print("=" * 80)


def fit_ar_model(data, dates, country_name, p_order=12):
    """Fit AR model with specified order"""
    print(f"\n{country_name} - AR({p_order}) Model")
    print("-" * 60)

    # Split data: train on first 80%, test on last 20%
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]

    # Fit AR model
    model = AutoReg(train_data, lags=p_order, trend='c')
    model_fit = model.fit()

    print(f"  Training samples: {len(train_data)}")
    print(f"  Test samples: {len(test_data)}")
    print(f"\n  Model Parameters:")
    print(f"    Constant: {model_fit.params[0]:.4f}")
    for i in range(1, min(6, len(model_fit.params))):  # Show first 5 AR coefficients
        print(f"    AR({i}): {model_fit.params[i]:.4f}")
    if len(model_fit.params) > 6:
        print(f"    ... (and {len(model_fit.params) - 6} more coefficients)")

    print(f"\n  Model Fit:")
    print(f"    AIC: {model_fit.aic:.2f}")
    print(f"    BIC: {model_fit.bic:.2f}")

    # Forecast
    forecast = model_fit.forecast(steps=len(test_data))

    # Calculate errors
    mse = np.mean((test_data - forecast) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(test_data - forecast))

    print(f"\n  Forecast Performance:")
    print(f"    MSE: {mse:.4f}")
    print(f"    RMSE: {rmse:.4f}")
    print(f"    MAE: {mae:.4f}")

    return model_fit, train_data, test_data, forecast, train_size


# Fit AR models
poland_ar_fit, poland_train, poland_test, poland_ar_forecast, poland_train_size = \
    fit_ar_model(poland_ts, poland_data['date'], "Poland", p_order=12)

ukraine_ar_fit, ukraine_train, ukraine_test, ukraine_ar_forecast, ukraine_train_size = \
    fit_ar_model(ukraine_ts, ukraine_data['date'], "Ukraine", p_order=12)

# ============================================================================
# MA MODELS
# ============================================================================
print("\n" + "=" * 80)
print("MOVING AVERAGE (MA) MODELS")
print("=" * 80)


def fit_ma_model(data, dates, country_name, q_order=12):
    """Fit MA model (using ARIMA with p=0, d=0, q=q_order)"""
    print(f"\n{country_name} - MA({q_order}) Model")
    print("-" * 60)

    # Split data: train on first 80%, test on last 20%
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]

    # Fit MA model (ARIMA(0,0,q))
    model = ARIMA(train_data, order=(0, 0, q_order), trend='c')
    model_fit = model.fit()

    print(f"  Training samples: {len(train_data)}")
    print(f"  Test samples: {len(test_data)}")
    print(f"\n  Model Parameters:")

    # Get parameter names and values
    params = model_fit.params
    print(f"    Constant: {params[0]:.4f}")
    for i in range(1, min(6, len(params))):  # Show first 5 MA coefficients
        print(f"    MA({i}): {params[i]:.4f}")
    if len(params) > 6:
        print(f"    ... (and {len(params) - 6} more coefficients)")

    print(f"\n  Model Fit:")
    print(f"    AIC: {model_fit.aic:.2f}")
    print(f"    BIC: {model_fit.bic:.2f}")

    # Forecast
    forecast = model_fit.forecast(steps=len(test_data))

    # Calculate errors
    mse = np.mean((test_data - forecast) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(test_data - forecast))

    print(f"\n  Forecast Performance:")
    print(f"    MSE: {mse:.4f}")
    print(f"    RMSE: {rmse:.4f}")
    print(f"    MAE: {mae:.4f}")

    return model_fit, train_data, test_data, forecast, train_size


# Fit MA models
poland_ma_fit, poland_train_ma, poland_test_ma, poland_ma_forecast, poland_train_size_ma = \
    fit_ma_model(poland_ts, poland_data['date'], "Poland", q_order=12)

ukraine_ma_fit, ukraine_train_ma, ukraine_test_ma, ukraine_ma_forecast, ukraine_train_size_ma = \
    fit_ma_model(ukraine_ts, ukraine_data['date'], "Ukraine", q_order=12)

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n" + "=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)

# Poland AR Model Visualization
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Plot 1: AR Model - Full series with train/test split and forecast
ax = axes[0]
train_dates = poland_data['date'].iloc[:poland_train_size]
test_dates = poland_data['date'].iloc[poland_train_size:poland_train_size + len(poland_test)]

ax.plot(poland_data['date'], poland_ts, label='Actual', alpha=0.7, linewidth=1)
ax.plot(test_dates, poland_ar_forecast, label='AR Forecast',
        color='red', linewidth=2, linestyle='--')
ax.axvline(x=train_dates.iloc[-1], color='green', linestyle=':',
           linewidth=2, label='Train/Test Split')
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Poland - AR(12) Model: Actual vs Forecast', fontsize=13, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Plot 2: ACF
plot_acf(poland_ts, lags=40, ax=axes[1], title='Poland - Autocorrelation Function (ACF)')
axes[1].set_xlabel('Lag', fontsize=11)

# Plot 3: PACF
plot_pacf(poland_ts, lags=40, ax=axes[2], title='Poland - Partial Autocorrelation Function (PACF)')
axes[2].set_xlabel('Lag', fontsize=11)

plt.tight_layout()
plt.savefig('./poland_ar_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Created poland_ar_model.png")

# Poland MA Model Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Plot 1: MA Model
ax = axes[0]
test_dates = poland_data['date'].iloc[poland_train_size_ma:poland_train_size_ma + len(poland_test_ma)]

ax.plot(poland_data['date'], poland_ts, label='Actual', alpha=0.7, linewidth=1)
ax.plot(test_dates, poland_ma_forecast, label='MA Forecast',
        color='purple', linewidth=2, linestyle='--')
ax.axvline(x=train_dates.iloc[-1], color='green', linestyle=':',
           linewidth=2, label='Train/Test Split')
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Poland - MA(12) Model: Actual vs Forecast', fontsize=13, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Plot 2: Comparison of AR vs MA
ax = axes[1]
ax.plot(test_dates, poland_test, label='Actual', color='black', linewidth=2)
ax.plot(test_dates, poland_ar_forecast, label='AR Forecast',
        color='red', linewidth=2, linestyle='--', alpha=0.7)
ax.plot(test_dates, poland_ma_forecast, label='MA Forecast',
        color='purple', linewidth=2, linestyle='-.', alpha=0.7)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Poland - AR vs MA Model Comparison (Test Period)', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./poland_ma_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Created poland_ma_model.png")

# Ukraine AR Model Visualization
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Plot 1: AR Model
ax = axes[0]
train_dates_ukr = ukraine_data['date'].iloc[:ukraine_train_size]
test_dates_ukr = ukraine_data['date'].iloc[ukraine_train_size:ukraine_train_size + len(ukraine_test)]

ax.plot(ukraine_data['date'], ukraine_ts, label='Actual', alpha=0.7, linewidth=1)
ax.plot(test_dates_ukr, ukraine_ar_forecast, label='AR Forecast',
        color='red', linewidth=2, linestyle='--')
ax.axvline(x=train_dates_ukr.iloc[-1], color='green', linestyle=':',
           linewidth=2, label='Train/Test Split')
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Ukraine - AR(12) Model: Actual vs Forecast', fontsize=13, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Plot 2: ACF
plot_acf(ukraine_ts, lags=40, ax=axes[1], title='Ukraine - Autocorrelation Function (ACF)')
axes[1].set_xlabel('Lag', fontsize=11)

# Plot 3: PACF
plot_pacf(ukraine_ts, lags=40, ax=axes[2], title='Ukraine - Partial Autocorrelation Function (PACF)')
axes[2].set_xlabel('Lag', fontsize=11)

plt.tight_layout()
plt.savefig('./ukraine_ar_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Created ukraine_ar_model.png")

# Ukraine MA Model Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Plot 1: MA Model
ax = axes[0]
test_dates_ukr_ma = ukraine_data['date'].iloc[ukraine_train_size_ma:ukraine_train_size_ma + len(ukraine_test_ma)]

ax.plot(ukraine_data['date'], ukraine_ts, label='Actual', alpha=0.7, linewidth=1)
ax.plot(test_dates_ukr_ma, ukraine_ma_forecast, label='MA Forecast',
        color='purple', linewidth=2, linestyle='--')
ax.axvline(x=train_dates_ukr.iloc[-1], color='green', linestyle=':',
           linewidth=2, label='Train/Test Split')
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Ukraine - MA(12) Model: Actual vs Forecast', fontsize=13, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Plot 2: Comparison of AR vs MA
ax = axes[1]
ax.plot(test_dates_ukr_ma, ukraine_test_ma, label='Actual', color='black', linewidth=2)
ax.plot(test_dates_ukr_ma, ukraine_ar_forecast, label='AR Forecast',
        color='red', linewidth=2, linestyle='--', alpha=0.7)
ax.plot(test_dates_ukr_ma, ukraine_ma_forecast, label='MA Forecast',
        color='purple', linewidth=2, linestyle='-.', alpha=0.7)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Ukraine - AR vs MA Model Comparison (Test Period)', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./ukraine_ma_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Created ukraine_ma_model.png")

# ============================================================================
# SUMMARY COMPARISON
# ============================================================================
print("\n" + "=" * 80)
print("MODEL COMPARISON SUMMARY")
print("=" * 80)

# Calculate metrics for comparison
poland_ar_rmse = np.sqrt(np.mean((poland_test - poland_ar_forecast) ** 2))
poland_ma_rmse = np.sqrt(np.mean((poland_test_ma - poland_ma_forecast) ** 2))
ukraine_ar_rmse = np.sqrt(np.mean((ukraine_test - ukraine_ar_forecast) ** 2))
ukraine_ma_rmse = np.sqrt(np.mean((ukraine_test_ma - ukraine_ma_forecast) ** 2))

print("\nPoland:")
print(f"  AR(12) RMSE: {poland_ar_rmse:.4f}")
print(f"  MA(12) RMSE: {poland_ma_rmse:.4f}")
print(f"  Better model: {'AR' if poland_ar_rmse < poland_ma_rmse else 'MA'}")

print("\nUkraine:")
print(f"  AR(12) RMSE: {ukraine_ar_rmse:.4f}")
print(f"  MA(12) RMSE: {ukraine_ma_rmse:.4f}")
print(f"  Better model: {'AR' if ukraine_ar_rmse < ukraine_ma_rmse else 'MA'}")

# Save summary
summary = pd.DataFrame({
    'Country': ['Poland', 'Poland', 'Ukraine', 'Ukraine'],
    'Model': ['AR(12)', 'MA(12)', 'AR(12)', 'MA(12)'],
    'RMSE': [poland_ar_rmse, poland_ma_rmse, ukraine_ar_rmse, ukraine_ma_rmse],
    'AIC': [poland_ar_fit.aic, poland_ma_fit.aic, ukraine_ar_fit.aic, ukraine_ma_fit.aic],
    'BIC': [poland_ar_fit.bic, poland_ma_fit.bic, ukraine_ar_fit.bic, ukraine_ma_fit.bic]
})

summary.to_csv('./model_comparison.csv', index=False)
print("\n✓ Model comparison saved to model_comparison.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)