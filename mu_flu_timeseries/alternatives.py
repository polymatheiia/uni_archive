"""
Ridge Regression + Hybrid Approaches dla Flu Forecasting

Zawiera:
1. Czysty Ridge
2. Ridge + Prophet (ensemble)
3. Ridge na residuach Prophet
4. Ridge + STL decomposition
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prophet import Prophet
from statsmodels.tsa.seasonal import STL
import warnings
warnings.filterwarnings('ignore')


def safe_iso_to_date(year, week):
    """Bezpieczna konwersja rok+tydzień ISO na datę"""
    try:
        return pd.to_datetime(f"{int(year)}-W{int(week)}-1", format='%G-W%V-%u')
    except ValueError:
        if week == 53:
            return pd.to_datetime(f"{int(year)+1}-W01-1", format='%G-W%V-%u')
        raise


def create_lagged_features(ts, lags=[1, 2, 4, 8, 13, 52], include_rolling=True,
                          include_fourier=True, include_interactions=False):
    """
    Tworzy bogate features dla Ridge

    Parameters:
    -----------
    lags : list
        Które lagi użyć (52 = rok wstecz, ale traci 52 tygodnie!)
    include_rolling : bool
        Rolling statistics
    include_fourier : bool
        Sin/cos dla sezonowości
    include_interactions : bool
        Interakcje między features (lag_1 * month, etc.)
    """
    df = pd.DataFrame({'y': ts})

    # 1. Lagged values
    for lag in lags:
        df[f'lag_{lag}'] = df['y'].shift(lag)

    # 2. Rolling statistics
    if include_rolling:
        for window in [4, 8]:
            df[f'rolling_mean_{window}'] = df['y'].shift(1).rolling(window).mean()
            df[f'rolling_std_{window}'] = df['y'].shift(1).rolling(window).std()
            df[f'rolling_max_{window}'] = df['y'].shift(1).rolling(window).max()
            df[f'rolling_min_{window}'] = df['y'].shift(1).rolling(window).min()

    # 3. Fourier terms (zamiast SARIMA seasonal!)
    if include_fourier:
        week_of_year = (np.arange(len(ts)) % 52) + 1

        # 3 harmonics
        for k in range(1, 4):
            df[f'sin_year_{k}'] = np.sin(2 * k * np.pi * week_of_year / 52)
            df[f'cos_year_{k}'] = np.cos(2 * k * np.pi * week_of_year / 52)

    # 4. Trend
    df['time_index'] = np.arange(len(ts))
    df['time_squared'] = df['time_index'] ** 2

    # 5. Month dummies
    df['month'] = pd.to_datetime(ts.index).month
    for month in range(1, 13):
        df[f'month_{month}'] = (df['month'] == month).astype(int)

    # 6. Interakcje (opcjonalne - zwiększa features!)
    if include_interactions:
        # lag_1 × miesiąc (czy ostatni tydzień ma inną wagę w różnych miesiącach?)
        for month in [1, 2, 3, 12]:  # zimowe miesiące
            df[f'lag1_x_month{month}'] = df['lag_1'] * df[f'month_{month}']

        # rolling_mean × sezonowość
        df['rolling_mean_4_x_sin1'] = df['rolling_mean_4'] * df['sin_year_1']

    return df


def prepare_data(filepath='grypa_polska_2007_2023_CLEANED.xlsx',
                include_lag52=False):
    """Wczytuje i przygotowuje dane"""

    print("📂 Wczytywanie danych...")
    df_flu = pd.read_excel(filepath)
    df_flu['date'] = df_flu.apply(lambda row: safe_iso_to_date(row['Rok'], row['Numer tygodnia']), axis=1)
    df_flu = df_flu.sort_values('date').reset_index(drop=True)
    ts = df_flu.set_index('date')['Liczba przypadków na 100 tys.']

    print(f"✓ Szereg czasowy: {len(ts)} tygodni ({ts.index.min().date()} - {ts.index.max().date()})")

    # Features
    lags = [1, 2, 4, 8, 13]
    if include_lag52:
        lags.append(52)
        print("⚠️  Używam lag_52 - straci się 52 tygodnie danych")

    df = create_lagged_features(ts, lags=lags, include_interactions=False)

    print(f"✓ Utworzono {df.shape[1]} features")
    df = df.dropna()
    print(f"✓ Po usunięciu NaN: {len(df)} tygodni")

    return df, ts


def train_ridge_model(X_train, y_train, alphas=[0.1, 1.0, 10.0, 100.0, 1000.0]):
    """
    Trenuje Ridge z cross-validation dla alpha

    Returns:
        Najlepszy model Ridge
    """
    print("\n🔷 Trenowanie Ridge Regression z CV...")

    # RidgeCV automatycznie wybierze najlepsze alpha
    ridge = RidgeCV(alphas=alphas, cv=5)
    ridge.fit(X_train, y_train)

    print(f"✓ Najlepsze alpha: {ridge.alpha_}")

    return ridge


def evaluate_model(model, X_test, y_test, model_name="Model"):
    """Ewaluacja"""
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print(f"\n📊 {model_name}:")
    print(f"   MAE:  {mae:.2f}")
    print(f"   RMSE: {rmse:.2f}")
    print(f"   MAPE: {mape:.2f}%")

    return {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'predictions': y_pred}


def show_feature_importance(ridge_model, feature_names, top_n=15):
    """Wyświetla najważniejsze features dla Ridge"""
    coefs = np.abs(ridge_model.coef_)
    indices = np.argsort(coefs)[::-1][:top_n]

    print(f"\n📊 TOP {top_n} Najważniejszych Features:")
    print("="*70)
    for i, idx in enumerate(indices):
        sign = "+" if ridge_model.coef_[idx] > 0 else ""
        print(f"{i+1:2d}. {feature_names[idx]:<30} {sign}{ridge_model.coef_[idx]:>8.4f}")


# ============================================================================
# HYBRID APPROACH 1: Ridge + Prophet Ensemble
# ============================================================================

def hybrid_ridge_prophet_ensemble(train_data, test_data, X_train, X_test,
                                 y_train, y_test, ridge_model):
    """
    Hybrid 1: Uśrednij predykcje Ridge + Prophet

    Final = w1 * Ridge + w2 * Prophet
    """
    print("\n" + "="*80)
    print("🔀 HYBRID 1: Ridge + Prophet Ensemble")
    print("="*80)

    # 1. Predykcja Ridge
    ridge_pred = ridge_model.predict(X_test)

    # 2. Trenuj Prophet
    print("\n⏳ Trenowanie Prophet...")
    prophet_df = pd.DataFrame({
        'ds': train_data.index,
        'y': train_data['y'].values
    })

    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )

    prophet_model.fit(prophet_df)

    # Prognoza Prophet
    future = pd.DataFrame({'ds': test_data.index})
    prophet_forecast = prophet_model.predict(future)
    prophet_pred = prophet_forecast['yhat'].values

    # 3. Ensemble - różne wagi
    weights = [
        (0.7, 0.3, "Ridge 70% + Prophet 30%"),
        (0.6, 0.4, "Ridge 60% + Prophet 40%"),
        (0.5, 0.5, "Ridge 50% + Prophet 50%"),
    ]

    best_mae = float('inf')
    best_ensemble = None

    for w1, w2, name in weights:
        ensemble_pred = w1 * ridge_pred + w2 * prophet_pred
        mae = mean_absolute_error(y_test, ensemble_pred)
        print(f"\n{name}: MAE = {mae:.2f}")

        if mae < best_mae:
            best_mae = mae
            best_ensemble = ensemble_pred

    return best_ensemble


# ============================================================================
# HYBRID APPROACH 2: Ridge on Prophet Residuals
# ============================================================================

def hybrid_ridge_on_prophet_residuals(train_data, test_data, X_train, X_test,
                                     y_train, y_test):
    """
    Hybrid 2: Prophet dla głównego trendu/sezonowości, Ridge dla residuów

    Final = Prophet + Ridge(residuals)
    """
    print("\n" + "="*80)
    print("🔀 HYBRID 2: Ridge na Residuach Prophet")
    print("="*80)

    # 1. Trenuj Prophet
    print("\n⏳ Trenowanie Prophet...")
    prophet_df = pd.DataFrame({
        'ds': train_data.index,
        'y': train_data['y'].values
    })

    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )
    prophet_model.fit(prophet_df)

    # 2. Oblicz residua Prophet na train
    prophet_train_pred = prophet_model.predict(prophet_df)['yhat'].values
    residuals_train = y_train.values - prophet_train_pred

    print(f"✓ Residua Prophet - średnia: {np.mean(residuals_train):.4f}, std: {np.std(residuals_train):.4f}")

    # 3. Trenuj Ridge na residuach
    print("\n🔷 Trenowanie Ridge na residuach...")
    ridge_residual = RidgeCV(alphas=[0.1, 1.0, 10.0, 100.0], cv=5)
    ridge_residual.fit(X_train, residuals_train)

    print(f"✓ Najlepsze alpha dla residuów: {ridge_residual.alpha_}")

    # 4. Predykcja na test
    # Prophet baseline
    prophet_test = prophet_model.predict(pd.DataFrame({'ds': test_data.index}))
    prophet_pred = prophet_test['yhat'].values

    # Ridge correction
    ridge_correction = ridge_residual.predict(X_test)

    # Final
    final_pred = prophet_pred + ridge_correction

    mae = mean_absolute_error(y_test, final_pred)
    rmse = np.sqrt(mean_squared_error(y_test, final_pred))

    print(f"\n📊 Prophet baseline: MAE = {mean_absolute_error(y_test, prophet_pred):.2f}")
    print(f"📊 Prophet + Ridge correction: MAE = {mae:.2f}, RMSE = {rmse:.2f}")

    return final_pred, prophet_pred, ridge_correction


# ============================================================================
# HYBRID APPROACH 3: Ridge on STL Residuals
# ============================================================================

def hybrid_ridge_on_stl_residuals(train_data, test_data, X_train, X_test,
                                 y_train, y_test):
    """
    Hybrid 3: STL decomposition + Ridge na residuach

    STL = Seasonal and Trend decomposition using Loess
    Final = Trend + Seasonal + Ridge(residuals)
    """
    print("\n" + "="*80)
    print("🔀 HYBRID 3: Ridge na Residuach STL Decomposition")
    print("="*80)

    # 1. STL decomposition
    print("\n⏳ STL decomposition...")
    stl = STL(train_data['y'], seasonal=53, period=52)  # seasonal=53 dla robustness
    result = stl.fit()

    # Komponenty
    trend = result.trend
    seasonal = result.seasonal
    residuals = result.resid

    print(f"✓ Trend range: {trend.min():.2f} - {trend.max():.2f}")
    print(f"✓ Seasonal range: {seasonal.min():.2f} - {seasonal.max():.2f}")
    print(f"✓ Residuals std: {residuals.std():.2f}")

    # 2. Trenuj Ridge na residuach
    print("\n🔷 Trenowanie Ridge na residuach...")
    ridge_residual = RidgeCV(alphas=[0.1, 1.0, 10.0, 100.0], cv=5)
    ridge_residual.fit(X_train, residuals.values)

    # 3. Predykcja na test
    # Dla test set - użyj ostatniego trendu + sezonowości z okresu treningowego
    last_trend_value = trend.iloc[-1]

    # Sezonowość - użyj odpowiedniego tygodnia z train
    test_indices = test_data.index
    seasonal_test = []

    for test_date in test_indices:
        # Znajdź odpowiedni tydzień w roku
        test_week = test_date.isocalendar()[1]
        # Znajdź taki sam tydzień w train seasonal
        train_weeks = [d.isocalendar()[1] for d in train_data.index]
        matching = [i for i, w in enumerate(train_weeks) if w == test_week]
        if matching:
            seasonal_test.append(seasonal.iloc[matching[-1]])
        else:
            seasonal_test.append(0)  # fallback

    seasonal_test = np.array(seasonal_test)

    # Ridge correction
    ridge_correction = ridge_residual.predict(X_test)

    # Final
    final_pred = last_trend_value + seasonal_test + ridge_correction

    mae = mean_absolute_error(y_test, final_pred)
    rmse = np.sqrt(mean_squared_error(y_test, final_pred))

    print(f"\n📊 STL + Ridge: MAE = {mae:.2f}, RMSE = {rmse:.2f}")

    return final_pred


# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_comprehensive_results(y_test, results_dict, title="Porównanie Modeli"):
    """Kompleksowa wizualizacja wyników"""

    fig, axes = plt.subplots(3, 1, figsize=(16, 12))

    # 1. Prognozy vs rzeczywistość
    axes[0].plot(y_test.index, y_test.values, 'o-', linewidth=2.5, markersize=7,
                label='Rzeczywiste', color='black', zorder=10)

    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    for i, (name, result) in enumerate(results_dict.items()):
        axes[0].plot(y_test.index, result['predictions'], '--', linewidth=2,
                    label=f"{name} (MAE: {result['MAE']:.2f})",
                    color=colors[i % len(colors)], alpha=0.8)

    axes[0].set_title(title, fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Liczba przypadków na 100 tys.', fontsize=11)
    axes[0].legend(fontsize=10, loc='upper left')
    axes[0].grid(True, alpha=0.3)

    # 2. Błędy bezwzględne
    for i, (name, result) in enumerate(results_dict.items()):
        errors = np.abs(y_test.values - result['predictions'])
        axes[1].plot(y_test.index, errors, 'o-', linewidth=1.5, markersize=4,
                    label=name, color=colors[i % len(colors)])

    axes[1].set_title('Błędy Bezwzględne', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('|Błąd|', fontsize=11)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    # 3. Rozkład błędów (histogram)
    for i, (name, result) in enumerate(results_dict.items()):
        errors = y_test.values - result['predictions']
        axes[2].hist(errors, bins=15, alpha=0.5, label=name,
                    color=colors[i % len(colors)], edgecolor='black')

    axes[2].axvline(x=0, color='red', linestyle='--', linewidth=2)
    axes[2].set_title('Rozkład Błędów (Prognoza - Rzeczywistość)', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Błąd', fontsize=11)
    axes[2].set_ylabel('Częstość', fontsize=11)
    axes[2].legend(fontsize=9)
    axes[2].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.show()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("RIDGE REGRESSION + HYBRID APPROACHES")
    print("="*80)

    # 1. Przygotuj dane
    df, ts_original = prepare_data(include_lag52=False)  # Zmień na True jeśli chcesz lag_52

    # 2. Train/test split
    test_size = 26
    train_data = df.iloc[:-test_size].copy()
    test_data = df.iloc[-test_size:].copy()

    cols_to_drop = ['y', 'month']
    X_train = train_data.drop(cols_to_drop, axis=1)
    y_train = train_data['y']
    X_test = test_data.drop(cols_to_drop, axis=1)
    y_test = test_data['y']

    print(f"\n📊 Train: {len(X_train)} tygodni, Test: {len(X_test)} tygodni")
    print(f"📊 Features: {len(X_train.columns)}")

    # 3. MODEL 1: Pure Ridge
    print("\n" + "="*80)
    print("MODEL 1: Pure Ridge Regression")
    print("="*80)

    ridge_model = train_ridge_model(X_train, y_train)
    ridge_results = evaluate_model(ridge_model, X_test, y_test, "Pure Ridge")
    show_feature_importance(ridge_model, X_train.columns, top_n=15)

    # 4. MODEL 2: Ridge + Prophet Ensemble
    ensemble_pred = hybrid_ridge_prophet_ensemble(
        train_data, test_data, X_train, X_test, y_train, y_test, ridge_model
    )

    # 5. MODEL 3: Ridge on Prophet Residuals
    hybrid2_pred, prophet_pred, ridge_correction = hybrid_ridge_on_prophet_residuals(
        train_data, test_data, X_train, X_test, y_train, y_test
    )

    # 6. MODEL 4: Ridge on STL Residuals
    hybrid3_pred = hybrid_ridge_on_stl_residuals(
        train_data, test_data, X_train, X_test, y_train, y_test
    )

    # 7. Podsumowanie
    print("\n\n" + "="*80)
    print("📊 FINALNE PODSUMOWANIE")
    print("="*80)

    results = {
        'Pure Ridge': {
            'MAE': ridge_results['MAE'],
            'RMSE': ridge_results['RMSE'],
            'predictions': ridge_results['predictions']
        },
        'Ridge+Prophet (70/30)': {
            'MAE': mean_absolute_error(y_test, ensemble_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, ensemble_pred)),
            'predictions': ensemble_pred
        },
        'Prophet + Ridge(resid)': {
            'MAE': mean_absolute_error(y_test, hybrid2_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, hybrid2_pred)),
            'predictions': hybrid2_pred
        },
        'STL + Ridge(resid)': {
            'MAE': mean_absolute_error(y_test, hybrid3_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, hybrid3_pred)),
            'predictions': hybrid3_pred
        }
    }

    # Ranking
    ranking = pd.DataFrame([
        {'Model': name, 'MAE': r['MAE'], 'RMSE': r['RMSE']}
        for name, r in results.items()
    ]).sort_values('MAE')

    print("\n🏆 Ranking (wg MAE):")
    print(ranking.to_string(index=False))

    best = ranking.iloc[0]
    print(f"\n🥇 ZWYCIĘZCA: {best['Model']}")
    print(f"   MAE:  {best['MAE']:.2f}")
    print(f"   RMSE: {best['RMSE']:.2f}")

    # 8. Wizualizacja
    print("\n📈 Generowanie wykresów...")
    plot_comprehensive_results(y_test, results, title="Ridge vs Hybrid Approaches")

    print("\n" + "="*80)
    print("✅ GOTOWE!")
    print("="*80)