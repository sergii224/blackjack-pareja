"""
main.py — Desarrollo de la partida y punto de entrada del programa.

Asignado a: Alumno B ([COMPAÑERO])
Práctica colaborativa: Blackjack con Git y GitHub
IES María Moliner (Segovia) — 2.º DAW — Grupo DAW S2I
"""

from cartas import crear_baraja, barajar, repartir, nombre_carta
from juego import (
    calcular_puntuacion,
    es_blackjack,
    se_pasa,
    determinar_ganador,
)
from interfaz import (
    mostrar_titulo,
    mostrar_mano,
    pedir_accion,
    mostrar_resultado,
    preguntar_otra_partida,
)

# La banca pide carta mientras su puntuación sea menor que 17.
PUNTUACION_MINIMA_BANCA = 17


def mostrar_mesa(mano_jugador, mano_banca, banca_oculta=True):
    """Muestra las dos manos. La banca puede tener la segunda carta oculta."""
    mostrar_mano("Tu mano", mano_jugador)
    mostrar_mano("Banca  ", mano_banca, oculta=banca_oculta)


def turno_jugador(baraja, mano_jugador, mano_banca):
    """Gestiona el turno del jugador: pedir carta o plantarse.

    Devuelve True si el jugador se pasa de 21.
    """
    while True:
        if calcular_puntuacion(mano_jugador) == 21:
            print("Tienes 21. Te plantas automáticamente.")
            return False

        accion = pedir_accion()
        if accion == "plantarse":
            print("Te plantas.")
            return False

        nuevas = repartir(baraja, 1)
        mano_jugador.extend(nuevas)
        print(f"Recibes: {nombre_carta(nuevas[0])}")
        mostrar_mesa(mano_jugador, mano_banca, banca_oculta=True)
        if se_pasa(mano_jugador):
            return True


def turno_banca(baraja, mano_banca):
    """La banca pide cartas hasta alcanzar 17 o más (se planta en 17)."""
    print()
    print("Turno de la banca...")
    while calcular_puntuacion(mano_banca) < PUNTUACION_MINIMA_BANCA:
        nuevas = repartir(baraja, 1)
        mano_banca.extend(nuevas)
        print(f"La banca pide carta: {nombre_carta(nuevas[0])}")
    if se_pasa(mano_banca):
        print("La banca se pasa de 21.")
    else:
        print(f"La banca se planta con {calcular_puntuacion(mano_banca)} puntos.")


def jugar_partida():
    """Desarrolla una partida completa de Blackjack."""
    mostrar_titulo()

    baraja = barajar(crear_baraja())
    mano_jugador = repartir(baraja, 2)
    mano_banca = repartir(baraja, 2)

    print("Cartas iniciales:")
    mostrar_mesa(mano_jugador, mano_banca, banca_oculta=True)
    print()

    # Si hay Blackjack en el reparto inicial, no se piden más cartas.
    if es_blackjack(mano_jugador) or es_blackjack(mano_banca):
        print("Se revela la mano de la banca.")
        mostrar_mesa(mano_jugador, mano_banca, banca_oculta=False)
        _, mensaje = determinar_ganador(mano_jugador, mano_banca)
        mostrar_resultado(mensaje)
        return

    if turno_jugador(baraja, mano_jugador, mano_banca):
        mostrar_mesa(mano_jugador, mano_banca, banca_oculta=False)
        _, mensaje = determinar_ganador(mano_jugador, mano_banca)
        mostrar_resultado(mensaje)
        return

    turno_banca(baraja, mano_banca)
    print()
    print("Manos finales:")
    mostrar_mesa(mano_jugador, mano_banca, banca_oculta=False)
    _, mensaje = determinar_ganador(mano_jugador, mano_banca)
    mostrar_resultado(mensaje)


def main():
    """Bucle principal: permite jugar varias partidas seguidas."""
    print("Bienvenido al Blackjack.")
    print("El objetivo es acercarse a 21 sin pasarse. La banca pide hasta 17.")
    while True:
        jugar_partida()
        if not preguntar_otra_partida():
            print("Gracias por jugar. ¡Hasta la próxima!")
            break


if __name__ == "__main__":
    main()
