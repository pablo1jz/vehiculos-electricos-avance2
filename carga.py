"""Carga e inspección del conjunto de datos de ventas de EVs (Avance 2)."""
import pandas as pd
import os

def cargar_datos(ruta="datos/electric-car-sales.csv"):
    """Carga el dataset original de ventas de vehículos eléctricos."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo en: {ruta}")
    
    df = pd.read_csv(ruta)
    print(f"[Carga] Dataset cargado exitosamente. Dimensiones iniciales: {df.shape}")
    return df