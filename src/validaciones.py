"""Validaciones de calidad para el dataset de ventas de vehículos eléctricos."""
import pandas as pd


def validar_dataset(df: pd.DataFrame) -> bool:
    """Ejecuta controles de integridad sobre el dataset procesado."""
    if df is None or df.empty:
        raise ValueError("El dataset procesado está vacío.")

    columnas_requeridas = {"entity", "code", "year", "electric_cars_sold"}
    faltantes = columnas_requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {sorted(faltantes)}")

    if (df["electric_cars_sold"] < 0).any():
        raise ValueError("Se detectaron valores negativos en electric_cars_sold.")

    if df["year"].isna().any() or df["electric_cars_sold"].isna().any():
        raise ValueError("Se detectaron valores nulos en year o electric_cars_sold.")

    print(f"[Validación] Dataset validado correctamente ({len(df)} registros, {df['entity'].nunique()} entidades).")
    return True
