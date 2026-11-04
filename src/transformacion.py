import pandas as pd

def aplicar_transformaciones(df):
    """Aplica transformaciones analíticas a las ventas de vehículos eléctricos."""
    df_trans = df.copy()
    
    # Transformación 1: Asegurar tipo numérico entero en ventas
    df_trans['electric_cars_sold'] = pd.to_numeric(df_trans['electric_cars_sold'], errors='coerce')
    
    # Transformación 2: Separar países de agregados regionales (World, Europe, etc.)
    agregados = ['World', 'Europe', 'European Union (27)', 'Rest of World']
    df_trans['tipo_entidad'] = df_trans['entity'].apply(lambda x: 'Agregado' if x in agregados else 'País')
    
    # Transformación 3: Clasificar el volumen de ventas por rangos (ej. escala de adopción)
    df_trans['nivel_adopcion'] = pd.qcut(
        df_trans['electric_cars_sold'], 
        q=3, 
        labels=['Bajo', 'Medio', 'Alto'], 
        duplicates='drop'
    )
    
    print("[Transformaciones] Transformaciones aplicadas correctamente (incluyendo datos de China y otros países).")
    return df_trans