import pandas as pd
import os

def calcular_indicadores(input_path="datos/procesados/dataset_limpio.csv", output_path="resultados/indicadores.csv"):
    df = pd.read_csv(input_path)
    
    # Filter only countries for specific analysis if needed, or overall
    df_paises = df[df['tipo_entidad'] == 'pais']
    
    total_registros = len(df)
    promedio_ventas = df['ventas'].mean()
    
    # Percentage of cases with high/very high adoption or meeting condition
    pct_crecimiento_positivo = (df['variacion_anual_pct'] > 0).sum() / df['variacion_anual_pct'].count() * 100
    
    # Category most frequent
    cat_frecuente = df['categoria_mercado'].mode()[0] if not df['categoria_mercado'].mode().empty else 'N/A'
    
    # Max sales and associated record
    max_idx = df['ventas'].idxmax()
    max_row = df.loc[max_idx]
    max_val = max_row['ventas']
    max_info = f"{max_row['pais']} ({max_row['anio']})"
    
    indicadores = [
        {
            'Indicador': 'Total de registros válidos',
            'Metodo_de_calculo': 'len(df)',
            'Resultado': total_registros,
            'Interpretacion': 'Cantidad total de observaciones procesadas en el dataset.'
        },
        {
            'Indicador': 'Promedio de ventas de EVs',
            'Metodo_de_calculo': 'df["ventas"].mean()',
            'Resultado': round(promedio_ventas, 2),
            'Interpretacion': 'Venta media general de autos eléctricos por observación.'
        },
        {
            'Indicador': 'Porcentaje con variación anual positiva',
            'Metodo_de_calculo': '(variacion_anual_pct > 0) / Total * 100',
            'Resultado': f"{round(pct_crecimiento_positivo, 2)}%",
            'Interpretacion': 'Proporción de observaciones que muestran aceleración o crecimiento respecto al año anterior.'
        },
        {
            'Indicador': 'Categoría de mercado más frecuente',
            'Metodo_de_calculo': 'df["categoria_mercado"].mode()[0]',
            'Resultado': cat_frecuente,
            'Interpretacion': 'El rango de volumen de ventas predominante a nivel global y nacional.'
        },
        {
            'Indicador': 'Valor máximo de ventas y registro',
            'Metodo_de_calculo': 'df["ventas"].max() y registro asociado',
            'Resultado': f"{max_val} ({max_info})",
            'Interpretacion': 'Identifica el pico histórico de ventas registrado en la serie.'
        }
    ]
    
    df_ind = pd.DataFrame(indicadores)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_ind.to_csv(output_path, index=False)
    print(f"[Indicadores] Indicadores exportados a {output_path}")
    return df_ind

if __name__ == "__main__":
    calcular_indicadores()
