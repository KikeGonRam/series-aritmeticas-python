# Progresion Aritmetica con Pandas

Proyecto en Python para analizar si una serie numerica cumple una Progresion Aritmetica (PA).

## Requisitos

- Python 3.14
- Pandas

## Instalacion

```powershell
python -m pip install -r requirements.txt
```

## Ejecucion rapida (todo en uno)

Opcion 1 (doble clic o CMD):

```bat
run_all.bat
```

Opcion 1b (silenciosa, salida minima):

```bat
run_all_silent.bat
```

Opcion 2 (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all.ps1
```

Este atajo ejecuta:

1. `main.py`
2. Pruebas unitarias `unittest`

`run_all.bat` muestra el detalle completo; `run_all_silent.bat` solo imprime `OK` o `FALLIDO`.

Y devuelve codigo de salida `0` si todo termina bien.

## Ejecucion

```powershell
python main.py
```

## Pruebas unitarias

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Funcionalidades principales

- Validacion robusta de entrada (None, tipos no numericos, lista vacia).
- Deteccion de progresion aritmetica y razon comun.
- Reporte tabular con `posicion`, `valor` y `diferencia_con_anterior`.
- Estadisticas descriptivas con Pandas (`min`, `max`, `media`, `desviacion_estandar`).
- Prediccion de los siguientes terminos si la serie es PA.
- Calculo de un termino en posicion especifica con la formula:

  `a_n = a_1 + (n - 1) * d`

- Redondeo de salida configurable en `mostrar_analisis(redondeo=4)`.
- Exportacion de reporte a CSV con `exportar_reporte_csv(...)`.

## Reportes CSV

Al ejecutar `main.py`, para cada caso que si es PA se genera un CSV en la carpeta `reportes/`.

Ejemplos de archivos:

- `reportes/pa_pa_creciente.csv`
- `reportes/pa_pa_decreciente.csv`
- `reportes/pa_pa_decimal.csv`

## Casos de prueba incluidos

`main.py` incluye casos PA y no PA, con decimales, negativos, un solo numero, `None` y texto mezclado para validar manejo de errores.
