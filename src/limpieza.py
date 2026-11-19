import pandas as pd

def limpiar_datos(df):
    """Limpia el dataset de ventas: normaliza columnas, trata nulos y valores negativos."""
    df_limpio = df.copy()
    
    # 1. Normalizar nombres de columnas a español (como indicaba tu informe 1)
    df_limpio.columns = ['entity', 'code', 'year', 'electric_cars_sold']
    
    # 2. Eliminar filas duplicadas
    duplicados_antes = df_limpio.duplicated().sum()
    df_limpio = df_limpio.drop_duplicates()
    print(f"[Limpieza] Se eliminaron {duplicados_antes} filas duplicadas.")
    
    # 3. Tratamiento de nulos en 'code' (pertenecen a agregados como 'Rest of World')
    df_limpio['code'] = df_limpio['code'].fillna('DESC')
    
    # 4. Filtrar valores negativos o fuera de rango en ventas (ej. registros residuales de Rest of World)
    df_limpio = df_limpio[df_limpio['electric_cars_sold'] >= 0]
    
    print(f"[Limpieza] Filas tras la limpieza: {len(df_limpio)}")
    return df_limpio