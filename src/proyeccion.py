"""Modelos matemáticos de proyección para ventas de vehículos eléctricos."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def calcular_metricas_serie(df_serie: pd.DataFrame) -> dict:
    """Calcula indicadores clave sobre una serie anual ordenada por 'year'."""
    serie = df_serie.sort_values("year").copy()
    total_ventas = float(serie["electric_cars_sold"].sum()) if len(serie) > 0 else 0.0
    promedio_ventas = float(serie["electric_cars_sold"].mean()) if len(serie) > 0 else 0.0
    max_ventas = float(serie["electric_cars_sold"].max()) if len(serie) > 0 else 0.0
    min_ventas = float(serie["electric_cars_sold"].min()) if len(serie) > 0 else 0.0
    registros = int(len(serie))

    variacion_global_pct = np.nan
    if len(serie) >= 2 and serie["electric_cars_sold"].iloc[0] > 0:
        variacion_global_pct = (
            (serie["electric_cars_sold"].iloc[-1] - serie["electric_cars_sold"].iloc[0])
            / serie["electric_cars_sold"].iloc[0]
        ) * 100.0

    return {
        "total_ventas": total_ventas,
        "promedio_ventas": promedio_ventas,
        "max_ventas": max_ventas,
        "min_ventas": min_ventas,
        "registros": registros,
        "variacion_global_pct": variacion_global_pct,
    }


def proyectar_ventas(
    df_serie: pd.DataFrame,
    modelo: str = "Regresión Lineal",
    horizonte: int = 5,
) -> pd.DataFrame:
    """Genera proyección anual de ventas para una serie con columnas ['year', 'electric_cars_sold']."""
    serie = (
        df_serie.groupby("year", as_index=False)["electric_cars_sold"]
        .sum()
        .sort_values("year")
        .reset_index(drop=True)
    )
    if len(serie) < 2 or horizonte < 1:
        return pd.DataFrame(columns=["year", "electric_cars_sold", "tipo", "modelo"])

    ultimo_anio = int(serie["year"].max())
    anios_futuros = np.arange(ultimo_anio + 1, ultimo_anio + horizonte + 1, dtype=int)

    if modelo == "Regresión Lineal":
        X = serie["year"].to_numpy(dtype=float).reshape(-1, 1)
        y = serie["electric_cars_sold"].to_numpy(dtype=float)
        reg = LinearRegression()
        reg.fit(X, y)
        preds = np.maximum(reg.predict(anios_futuros.astype(float).reshape(-1, 1)), 0.0)
    elif modelo == "Promedio Móvil (3 Años)":
        ventana = min(3, len(serie))
        valor_base = float(serie["electric_cars_sold"].tail(ventana).mean())
        preds = np.full(horizonte, max(valor_base, 0.0), dtype=float)
    elif modelo == "Tasa de Crecimiento Promedio":
        tasas = serie["electric_cars_sold"].pct_change().replace([np.inf, -np.inf], np.nan).dropna()
        tasa_prom = float(tasas.clip(lower=-0.5, upper=1.5).mean()) if len(tasas) > 0 else 0.05
        actual = float(serie["electric_cars_sold"].iloc[-1])
        preds_list = []
        for _ in range(horizonte):
            actual = max(actual * (1.0 + tasa_prom), 0.0)
            preds_list.append(actual)
        preds = np.array(preds_list, dtype=float)
    else:
        raise ValueError(f"Modelo no soportado: {modelo}")

    return pd.DataFrame({
        "year": anios_futuros,
        "electric_cars_sold": preds,
        "tipo": "Proyectado",
        "modelo": modelo,
    })
