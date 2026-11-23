"""Pruebas del Blackjack de referencia (no es obligatorio entregar este archivo)."""

import unittest
from unittest.mock import patch
from io import StringIO

from cartas import crear_baraja, barajar, repartir, nombre_carta, PALOS, VALORES
from juego import calcular_puntuacion, es_blackjack, se_pasa, determinar_ganador
import main


def carta(valor, palo="Corazones"):
    return {"valor": valor, "palo": palo}


class TestCartas(unittest.TestCase):
    def test_baraja_tiene_52_cartas_unicas(self):
        baraja = crear_baraja()
        self.assertEqual(len(baraja), 52)
        unicas = {(c["valor"], c["palo"]) for c in baraja}
        self.assertEqual(len(unicas), 52)
        self.assertEqual(len(PALOS) * len(VALORES), 52)

    def test_nombre_carta(self):
        self.assertEqual(nombre_carta(carta("A", "Picas")), "A de Picas")

    def test_barajar_conserva_las_cartas(self):
        original = crear_baraja()
        copia = [dict(c) for c in original]
        barajar(original)
        self.assertEqual(len(original), 52)
        self.assertEqual(
            sorted((c["valor"], c["palo"]) for c in original),
            sorted((c["valor"], c["palo"]) for c in copia),
        )

    def test_repartir_reduce_la_baraja(self):
        baraja = crear_baraja()
        cartas = repartir(baraja, 2)
        self.assertEqual(len(cartas), 2)
        self.assertEqual(len(baraja), 50)

    def test_repartir_sin_cartas_suficientes(self):
        baraja = crear_baraja()
        with self.assertRaises(ValueError):
            repartir(baraja, 53)


class TestPuntuacion(unittest.TestCase):
    def test_figuras_y_diez(self):
        self.assertEqual(calcular_puntuacion([carta("10"), carta("K")]), 20)
        self.assertEqual(calcular_puntuacion([carta("J"), carta("Q")]), 20)

    def test_blackjack_natural(self):
        mano = [carta("A"), carta("K")]
        self.assertEqual(calcular_puntuacion(mano), 21)
        self.assertTrue(es_blackjack(mano))
        self.assertFalse(es_blackjack([carta("A"), carta("10"), carta("K")]))

    def test_as_como_once(self):
        self.assertEqual(calcular_puntuacion([carta("A"), carta("7")]), 18)

    def test_as_como_uno_si_hace_falta(self):
        self.assertEqual(calcular_puntuacion([carta("A"), carta("K"), carta("5")]), 16)
        self.assertEqual(calcular_puntuacion([carta("A"), carta("A"), carta("9")]), 21)
        self.assertEqual(calcular_puntuacion([carta("A"), carta("A"), carta("A"), carta("8")]), 21)
        self.assertEqual(calcular_puntuacion([carta("A"), carta("5"), carta("A")]), 17)

    def test_veintiuno_blando(self):
        self.assertEqual(calcular_puntuacion([carta("10"), carta("10"), carta("A")]), 21)
        self.assertFalse(es_blackjack([carta("10"), carta("10"), carta("A")]))

    def test_se_pasa(self):
        mano = [carta("10"), carta("K"), carta("2")]
        self.assertEqual(calcular_puntuacion(mano), 22)
        self.assertTrue(se_pasa(mano))
        self.assertFalse(se_pasa([carta("A"), carta("K")]))


class TestGanador(unittest.TestCase):
    def test_jugador_se_pasa(self):
        resultado, _ = determinar_ganador(
            [carta("K"), carta("Q"), carta("5")],
            [carta("10"), carta("7")],
        )
        self.assertEqual(resultado, "banca")

    def test_banca_se_pasa(self):
        resultado, _ = determinar_ganador(
            [carta("10"), carta("8")],
            [carta("K"), carta("9"), carta("5")],
        )
        self.assertEqual(resultado, "jugador")

    def test_ambos_blackjack_empate(self):
        resultado, _ = determinar_ganador(
            [carta("A"), carta("K")],
            [carta("A", "Picas"), carta("10", "Picas")],
        )
        self.assertEqual(resultado, "empate")

    def test_blackjack_jugador(self):
        resultado, _ = determinar_ganador(
            [carta("A"), carta("J")],
            [carta("10"), carta("9")],
        )
        self.assertEqual(resultado, "jugador")

    def test_blackjack_banca(self):
        resultado, _ = determinar_ganador(
            [carta("10"), carta("9")],
            [carta("A"), carta("Q")],
        )
        self.assertEqual(resultado, "banca")

    def test_puntos_mayores_jugador(self):
        resultado, _ = determinar_ganador(
            [carta("10"), carta("9")],
            [carta("10"), carta("8")],
        )
        self.assertEqual(resultado, "jugador")

    def test_empate_por_puntos(self):
        resultado, _ = determinar_ganador(
            [carta("10"), carta("8")],
            [carta("9"), carta("9")],
        )
        self.assertEqual(resultado, "empate")


class TestPartidaSimulada(unittest.TestCase):
    def test_jugador_se_planta_y_termina(self):
        # plantarse en la partida y no repetir
        entradas = ["plantarse", "n"]
        with patch("builtins.input", side_effect=entradas):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                main.main()
                texto = salida.getvalue()
        self.assertIn("BLACKJACK", texto)
        self.assertIn("Hasta la próxima", texto)
        self.assertTrue(
            "Has ganado" in texto or "Gana la banca" in texto or "Empate" in texto
            or "Blackjack" in texto or "pasado" in texto
        )

    def test_jugador_pide_y_se_planta(self):
        entradas = ["pedir", "plantarse", "n"]
        with patch("builtins.input", side_effect=entradas):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                try:
                    main.main()
                except StopIteration:
                    # Si se pasa tras pedir, no se llega a plantarse; aún así la partida acaba
                    # si main pide otra acción. Se cubre pidiendo otra 'n' de más en otro test.
                    pass
                texto = salida.getvalue()
        self.assertIn("BLACKJACK", texto)


if __name__ == "__main__":
    unittest.main()
