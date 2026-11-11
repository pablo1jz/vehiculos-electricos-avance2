import os
from src.carga import cargar_datos
from src.limpieza import limpiar_datos
from src.transformacion import aplicar_transformaciones
from src.validaciones import validar_dataset
from src.estadisticas import calcular_estadisticas
from src.indicadores import calcular_indicadores
from src.visualizaciones import generar_graficos

def main():
    print("=== INICIANDO PIPELINE COMPLETO - AVANCE 2 Y AVANCE 3 ===")
    
    ruta_original = os.path.join("datos", "electric-car-sales.csv")
    if not os.path.exists(ruta_original):
        # Fallback to root
        ruta_original = "electric-car-sales.csv"
        
    ruta_salida = os.path.join("datos", "procesados", "dataset_limpio.csv")
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # 1. Pipeline de carga, limpieza, transformación y validación (Avance 2)
    df = cargar_datos(ruta_original)
    df_limpio = limpiar_datos(df)
    df_trans = aplicar_transformaciones(df_limpio)
    validar_dataset(df_trans)
    
    df_trans.to_csv(ruta_salida, index=False)
    print(f"[Exportación] Dataset limpio guardado en: {ruta_salida}")
    
    # 2. Pipeline de análisis, indicadores y visualizaciones (Avance 3)
    print("\n[Avance 3] Calculando estadísticas descriptivas...")
    calcular_estadisticas()
    
    print("[Avance 3] Calculando indicadores automatizados...")
    calcular_indicadores()
    
    print("[Avance 3] Generando gráficos con Pyplot...")
    generar_graficos()
    
    print("=== PROCESO COMPLETADO EXITOSAMENTE ===")

if __name__ == "__main__":
    main()
