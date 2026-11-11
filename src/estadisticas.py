import pandas as pd
import numpy as np
import os

def calcular_estadisticas(input_path="datos/procesados/dataset_limpio.csv", output_path="resultados/estadisticas.csv"):
    df = pd.read_csv(input_path)
    num_cols = df.select_dtypes(include=[np.number]).columns
    
    stats_list = []
    for col in num_cols:
        s = df[col]
        stats_list.append({
            'variable': col,
            'cantidad_registros': s.count(),
            'media': s.mean(),
            'mediana': s.median(),
            'minimo': s.min(),
            'maximo': s.max(),
            'rango': s.max() - s.min(),
            'desviacion_estandar': s.std(),
            'q25': s.quantile(0.25),
            'q50': s.quantile(0.50),
            'q75': s.quantile(0.75)
        })
        
    df_stats = pd.DataFrame(stats_list)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_stats.to_csv(output_path, index=False)
    print(f"[Estadísticas] Estadísticas descriptivas exportadas a {output_path}")
    return df_stats

if __name__ == "__main__":
    calcular_estadisticas()
