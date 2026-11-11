import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generar_graficos(input_path="datos/procesados/dataset_limpio.csv", output_dir="resultados/graficos"):
    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    
    # Gráfico 01: Histograma de Ventas
    plt.figure(figsize=(9, 5))
    df_paises = df[df['tipo_entidad'] == 'pais']
    sns.histplot(df_paises['ventas'].dropna(), kde=True, color='#2B6CB0', bins=30)
    plt.title('Distribución de Ventas Anuales de Autos Eléctricos (Países)', fontsize=12, fontweight='bold')
    plt.xlabel('Ventas Anuales (Unidades)', fontsize=10)
    plt.ylabel('Frecuencia (Cantidad de observaciones)', fontsize=10)
    plt.tight_layout()
    path1 = os.path.join(output_dir, 'grafico_01.png')
    plt.savefig(path1, dpi=300)
    plt.close()
    
    # Gráfico 02: Evolución Temporal Mundial (Línea)
    plt.figure(figsize=(9, 5))
    df_world = df[df['pais'] == 'World']
    sns.lineplot(x='anio', y='ventas', data=df_world, marker='o', color='#319795', linewidth=2.5)
    plt.title('Evolución Temporal de las Ventas Mundiales de EVs (2010-2025)', fontsize=12, fontweight='bold')
    plt.xlabel('Año', fontsize=10)
    plt.ylabel('Ventas Mundiales (Unidades)', fontsize=10)
    plt.tight_layout()
    path2 = os.path.join(output_dir, 'grafico_02.png')
    plt.savefig(path2, dpi=300)
    plt.close()
    
    # Gráfico 03: Diagrama de Caja (Boxplot) usando matplotlib puro
    plt.figure(figsize=(9, 5))
    categorias = ['muy bajo', 'bajo', 'medio', 'alto', 'muy alto']
    datos_cat = [df[df['categoria_mercado'] == cat]['ventas'].dropna() for cat in categorias]
    plt.boxplot(datos_cat, labels=categorias, patch_artist=True, boxprops=dict(facecolor='#63B3ED', color='#2B6CB0'))
    plt.title('Distribución de Ventas por Categoría de Mercado', fontsize=12, fontweight='bold')
    plt.xlabel('Categoría de Mercado', fontsize=10)
    plt.ylabel('Ventas (Unidades)', fontsize=10)
    plt.yscale('log')
    plt.tight_layout()
    path3 = os.path.join(output_dir, 'grafico_03.png')
    plt.savefig(path3, dpi=300)
    plt.close()
    
    print(f"[Visualizaciones] Gráficos exportados exitosamente en {output_dir}")

if __name__ == "__main__":
    generar_graficos()
