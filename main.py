import re
from pathlib import Path

import pandas as pd


class ProgresionAritmetica:
    """Analiza una serie numerica para determinar si sigue una Progresion Aritmetica (PA)."""

    def __init__(self, numeros: list[int | float] | None):
        """
        Inicializa la clase validando la entrada.

        Parametros:
            numeros (list[int | float]): Lista de numeros de la serie.

        Lanza:
            ValueError: Si la lista es None, no es lista o contiene elementos no numericos.
        """
        self.numeros = self._validar_numeros(numeros)
        self.serie = pd.Series(self.numeros, dtype="float64")

    @staticmethod
    def _validar_numeros(numeros: list[int | float] | None) -> list[float]:
        """
        Valida que la entrada sea una lista de numeros (int o float).

        Parametros:
            numeros (list[int | float]): Datos de entrada a validar.

        Retorna:
            list[float]: Lista validada y convertida a float.

        Lanza:
            ValueError: Si los datos no cumplen el formato esperado.
        """
        if numeros is None:
            raise ValueError("La lista de numeros no puede ser None.")

        if not isinstance(numeros, list):
            raise ValueError("La entrada debe ser una lista de numeros.")

        if len(numeros) == 0:
            raise ValueError("La lista de numeros no puede estar vacia.")

        for indice, valor in enumerate(numeros, start=1):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise ValueError(
                    f"Elemento invalido en posicion {indice}: {valor!r}. "
                    "Todos los elementos deben ser int o float."
                )

        return [float(valor) for valor in numeros]

    def obtener_diferencias(self) -> pd.Series:
        """
        Calcula las diferencias entre terminos consecutivos de la serie.

        Retorna:
            pd.Series: Diferencias entre cada termino y su anterior.
        """
        return self.serie.diff().dropna()

    def es_progresion_aritmetica(self) -> bool:
        """
        Verifica si la serie corresponde a una Progresion Aritmetica.

        Retorna:
            bool: True si todas las diferencias son iguales; False en otro caso.
        """
        if len(self.numeros) < 2:
            return False

        diferencias = self.obtener_diferencias()
        primera_diferencia = diferencias.iloc[0]
        return bool((diferencias == primera_diferencia).all())

    def obtener_razon(self) -> float | None:
        """
        Obtiene la razon comun de la PA.

        Retorna:
            float | None: Diferencia constante si es PA; None si no lo es.
        """
        if self.es_progresion_aritmetica():
            return float(self.obtener_diferencias().iloc[0])
        return None

    def obtener_estadisticas(self, redondeo: int | None = None) -> pd.DataFrame:
        """
        Calcula estadisticas descriptivas basicas de la serie.

        Parametros:
            redondeo (int | None): Cantidad de decimales para presentacion.

        Retorna:
            pd.DataFrame: DataFrame con min, max, media y desviacion estandar.
        """
        estadisticas = {
            "min": [self.serie.min()],
            "max": [self.serie.max()],
            "media": [self.serie.mean()],
            "desviacion_estandar": [self.serie.std()],
        }
        df_estadisticas = pd.DataFrame(estadisticas)
        if redondeo is not None:
            df_estadisticas = df_estadisticas.round(redondeo)
        return df_estadisticas

    def predecir_siguiente(self, n: int) -> list[float]:
        """
        Predice los siguientes n terminos usando la razon comun de la PA.

        Parametros:
            n (int): Cantidad de terminos a predecir.

        Retorna:
            list[float]: Lista con los n terminos siguientes.

        Lanza:
            ValueError: Si n no es entero positivo o si la serie no es PA.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("El parametro n debe ser un entero positivo.")

        razon = self.obtener_razon()
        if razon is None:
            raise ValueError("No se pueden predecir terminos porque la serie no es PA.")

        ultimo = self.serie.iloc[-1]
        return [float(ultimo + razon * paso) for paso in range(1, n + 1)]

    def obtener_termino(self, posicion: int) -> float:
        """
        Obtiene el termino en una posicion dada (base 1) usando la formula de PA.

        Formula matematica:
            a_n = a_1 + (n - 1) * d
        donde a_1 es el primer termino y d es la razon comun.

        Parametros:
            posicion (int): Posicion del termino a consultar (base 1).

        Retorna:
            float: Valor del termino solicitado.

        Lanza:
            ValueError: Si la posicion no es valida o la serie no es PA.
        """
        if not isinstance(posicion, int) or posicion < 1:
            raise ValueError("La posicion debe ser un entero mayor o igual a 1.")

        razon = self.obtener_razon()
        if razon is None:
            raise ValueError("No se puede calcular el termino porque la serie no es PA.")

        primer_termino = self.serie.iloc[0]
        return float(primer_termino + (posicion - 1) * razon)

    def obtener_reporte(self, redondeo: int | None = None) -> pd.DataFrame:
        """
        Genera un reporte tabular de la serie.

        Parametros:
            redondeo (int | None): Cantidad de decimales para presentacion.

        Retorna:
            pd.DataFrame: DataFrame con columnas posicion, valor y diferencia_con_anterior.
        """
        reporte = pd.DataFrame(
            {
                "posicion": range(1, len(self.serie) + 1),
                "valor": self.serie,
                "diferencia_con_anterior": self.serie.diff(),
            }
        )
        if redondeo is not None:
            reporte = reporte.round(redondeo)
        return reporte

    def exportar_reporte_csv(self, ruta_archivo: str, redondeo: int = 4) -> str:
        """
        Exporta el reporte de la serie a un archivo CSV.

        Parametros:
            ruta_archivo (str): Ruta completa o relativa del archivo CSV.
            redondeo (int): Decimales para el reporte exportado.

        Retorna:
            str: Ruta final del archivo generado.
        """
        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.obtener_reporte(redondeo=redondeo).to_csv(ruta, index=False)
        return str(ruta)

    def mostrar_analisis(self, redondeo: int = 4) -> None:
        """
        Imprime un analisis completo de la serie con manejo de excepciones.

        Incluye reporte en DataFrame, validacion de PA, razon comun,
        estadisticas y ejemplos de calculo de terminos.

        Parametros:
            redondeo (int): Decimales para mostrar resultados en pantalla.
        """
        try:
            print("=" * 70)
            print("  ANALISIS DE PROGRESION ARITMETICA")
            print("=" * 70)
            print(f"Serie original: {self.numeros}")
            print("\nReporte detallado:")
            print(self.obtener_reporte(redondeo=redondeo).to_string(index=False))

            es_pa = self.es_progresion_aritmetica()
            print(f"\nEs progresion aritmetica: {es_pa}")

            if es_pa:
                razon = self.obtener_razon()
                print(f"Razon comun: {round(razon, redondeo)}")
                print(f"Termino en posicion 10: {round(self.obtener_termino(10), redondeo)}")
                siguientes = [round(valor, redondeo) for valor in self.predecir_siguiente(3)]
                print(f"Siguientes 3 terminos: {siguientes}")
            else:
                print("Razon comun: No aplica (la serie no es PA)")

            print("\nEstadisticas:")
            print(self.obtener_estadisticas(redondeo=redondeo).to_string(index=False))
            print("=" * 70)

        except ValueError as error:
            print(f"Error de validacion: {error}")
        except Exception as error:
            print(f"Error inesperado durante el analisis: {error}")


def _normalizar_nombre_archivo(texto: str) -> str:
    """Convierte un titulo libre en un nombre de archivo seguro."""
    nombre = texto.strip().lower().replace(" ", "_")
    nombre = re.sub(r"[^a-z0-9_]+", "", nombre)
    return nombre or "caso"


if __name__ == "__main__":
    casos_prueba = [
        ("PA creciente", [2, 4, 6, 8, 10]),
        ("PA decreciente", [10, 7, 4, 1, -2]),
        ("PA constante", [5, 5, 5, 5]),
        ("No PA exponencial", [1, 2, 4, 8, 16]),
        ("No PA triangular", [3, 6, 10, 15]),
        ("PA grande", [100, 200, 300, 400]),
        ("Un solo numero", [1]),
        ("PA decimal", [1.5, 2.0, 2.5, 3.0]),
        ("PA negativa", [-10, -7, -4, -1]),
        ("Caso None", None),
        ("Texto mezclado", [1, "dos", 3]),
    ]

    carpeta_reportes = Path("reportes")

    for titulo, datos in casos_prueba:
        print(f"\nCASO: {titulo}")
        try:
            progresion = ProgresionAritmetica(datos)
            progresion.mostrar_analisis(redondeo=4)

            if progresion.es_progresion_aritmetica():
                nombre_archivo = _normalizar_nombre_archivo(titulo)
                ruta_csv = carpeta_reportes / f"pa_{nombre_archivo}.csv"
                ruta_generada = progresion.exportar_reporte_csv(str(ruta_csv), redondeo=4)
                print(f"CSV generado: {ruta_generada}")

        except ValueError as error:
            print(f"Error controlado: {error}")
        except Exception as error:
            print(f"Error no controlado: {error}")
