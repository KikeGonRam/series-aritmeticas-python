import unittest
from pathlib import Path

from main import ProgresionAritmetica


class TestProgresionAritmetica(unittest.TestCase):
    def test_pa_creciente(self):
        pa = ProgresionAritmetica([2, 4, 6, 8])
        self.assertTrue(pa.es_progresion_aritmetica())
        self.assertEqual(pa.obtener_razon(), 2.0)

    def test_no_pa(self):
        pa = ProgresionAritmetica([1, 2, 4, 8])
        self.assertFalse(pa.es_progresion_aritmetica())
        self.assertIsNone(pa.obtener_razon())

    def test_pa_decimal(self):
        pa = ProgresionAritmetica([1.5, 2.0, 2.5, 3.0])
        self.assertTrue(pa.es_progresion_aritmetica())
        self.assertAlmostEqual(pa.obtener_razon(), 0.5)

    def test_pa_negativa(self):
        pa = ProgresionAritmetica([10, 7, 4, 1])
        self.assertTrue(pa.es_progresion_aritmetica())
        self.assertEqual(pa.obtener_razon(), -3.0)

    def test_un_solo_numero(self):
        pa = ProgresionAritmetica([7])
        self.assertFalse(pa.es_progresion_aritmetica())

    def test_none_lanza_error(self):
        with self.assertRaises(ValueError):
            ProgresionAritmetica(None)

    def test_texto_mezclado_lanza_error(self):
        with self.assertRaises(ValueError):
            ProgresionAritmetica([1, "dos", 3])

    def test_predecir_siguiente(self):
        pa = ProgresionAritmetica([3, 6, 9])
        self.assertEqual(pa.predecir_siguiente(3), [12.0, 15.0, 18.0])

    def test_predecir_siguiente_no_pa_lanza_error(self):
        pa = ProgresionAritmetica([1, 2, 4])
        with self.assertRaises(ValueError):
            pa.predecir_siguiente(2)

    def test_obtener_termino(self):
        pa = ProgresionAritmetica([2, 4, 6])
        self.assertEqual(pa.obtener_termino(10), 20.0)

    def test_obtener_termino_posicion_invalida(self):
        pa = ProgresionAritmetica([2, 4, 6])
        with self.assertRaises(ValueError):
            pa.obtener_termino(0)

    def test_reporte_columnas(self):
        pa = ProgresionAritmetica([2, 4, 6])
        reporte = pa.obtener_reporte()
        self.assertListEqual(
            list(reporte.columns),
            ["posicion", "valor", "diferencia_con_anterior"],
        )

    def test_exportar_csv(self):
        pa = ProgresionAritmetica([2, 4, 6])
        carpeta = Path("tests") / "tmp"
        ruta = carpeta / "reporte_prueba.csv"
        ruta_generada = pa.exportar_reporte_csv(str(ruta))
        self.assertTrue(Path(ruta_generada).exists())


if __name__ == "__main__":
    unittest.main()

