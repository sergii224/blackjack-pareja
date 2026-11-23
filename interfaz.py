"""
interfaz.py — Interacción con el usuario y presentación de resultados.
"""

from cartas import nombre_carta
from juego import calcular_puntuacion


def mostrar_titulo():
    """Muestra la cabecera del juego."""
    print()
    print("=" * 42)
    print("           BLACKJACK")
    print("=" * 42)
    print()


def mostrar_mano(titulo, mano, oculta=False, mostrar_puntos=True):
    """Muestra una mano por pantalla.

    Si oculta es True, solo se ve la primera carta; el resto aparece
    como [carta oculta] y no se muestran los puntos totales.
    """
    if oculta and len(mano) > 0:
        visibles = [nombre_carta(mano[0])]
        for _ in mano[1:]:
            visibles.append("[carta oculta]")
        texto = ", ".join(visibles)
        print(f"{titulo}: {texto}")
        return

    nombres = [nombre_carta(carta) for carta in mano]
    texto = ", ".join(nombres)
    if mostrar_puntos:
        puntos = calcular_puntuacion(mano)
        print(f"{titulo}: {texto}  (puntos: {puntos})")
    else:
        print(f"{titulo}: {texto}")


def pedir_accion():
    """Pregunta al jugador si pide carta o se planta.

    Acepta varias formas equivalentes y repite la pregunta si la
    respuesta no es válida. Devuelve 'pedir' o 'plantarse'.
    """
    while True:
        respuesta = input("¿Qué quieres hacer? (pedir / plantarse): ").strip().lower()
        if respuesta in ("pedir", "p", "carta", "hit"):
            return "pedir"
        if respuesta in ("plantarse", "plantar", "s", "stand"):
            return "plantarse"
        print("Opción no válida. Escribe 'pedir' o 'plantarse'.")


def mostrar_resultado(mensaje):
    """Muestra el resultado final de la partida."""
    print()
    print("-" * 42)
    print(mensaje)
    print("-" * 42)


def preguntar_otra_partida():
    """Pregunta si se quiere jugar otra partida. Devuelve True o False."""
    while True:
        respuesta = input("¿Quieres jugar otra partida? (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí", "y", "yes"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Opción no válida. Escribe 's' o 'n'.")
