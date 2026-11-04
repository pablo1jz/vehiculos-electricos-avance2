import os
from src.carga import cargar_datos
from src.limpieza import limpiar_datos
from src.transformacion import aplicar_transformaciones
from src.validaciones import validar_dataset

def main():
    print("=== INICIANDO PIPELINE DE DATOS - AVANCE 2 ===")
    
    # Ruta del dataset del Avance 1
    ruta_original = os.path.join("datos", "electric-car-sales.csv")
    ruta_salida = os.path.join("datos", "procesados", "dataset_limpio.csv")
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # Ejecutar pipeline
    df = cargar_datos(ruta_original)
    df_limpio = limpiar_datos(df)
    df_trans = aplicar_transformaciones(df_limpio)
    validar_dataset(df_trans)
    
    # Exportar resultado
    df_trans.to_csv(ruta_salida, index=False)
    print(f"[Exportación] Dataset limpio guardado en: {ruta_salida}")
    print("=== PIPELINE FINALIZADO CON ÉXITO ===")

if __name__ == "__main__":
    main()