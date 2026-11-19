# Crecimiento de Vehículos Eléctricos – Avance 4

Proyecto Final Integrador (Programación Avanzada) — Universidad Autónoma.

## Estructura
```text
app.py                      dashboard interactivo en Streamlit
main.py                     pipeline de carga, limpieza, transformación y validación
requirements.txt            dependencias de Python
datos/
  electric-car-sales.csv    dataset original
  procesados/
    dataset_limpio.csv      dataset limpio generado por el pipeline
src/
  carga.py
  limpieza.py
  transformacion.py
  validaciones.py
  proyeccion.py
reportes/
  avance_1.pdf
  Informe Avance 2 - Crecimiento de Vehículos Eléctricos.pdf
  avance_4.pdf
```

## Ejecución
```bash
pip install -r requirements.txt
python main.py
streamlit run app.py
```
