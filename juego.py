"""
juego.py — Lógica de puntuación y comprobaciones del Blackjack.

Asignado a: Alumno A (Jorge Arribas Fernández)
Práctica colaborativa: Blackjack con Git y GitHub
IES María Moliner (Segovia) — 2.º DAW — Grupo DAW S2I
"""

# Figuras y el 10 valen 10. El As se trata de forma especial (11 o 1).
VALORES_NUMERICOS = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}


def calcular_puntuacion(mano):
    """Calcula la puntuación de una mano.

    Los Ases valen 11 o 1: se usa 11 siempre que no se supere 21;
    si la mano se pasa, cada As se convierte en 1 hasta dejar de
    superarlo (o hasta no quedar Ases por ajustar).
    """
    puntos = 0
    ases = 0
    for carta in mano:
        valor = carta["valor"]
        if valor == "A":
            ases += 1
            puntos += 11
        else:
            puntos += VALORES_NUMERICOS[valor]

    while puntos > 21 and ases > 0:
        puntos -= 10
        ases -= 1

    return puntos


def es_blackjack(mano):
    """True si la mano es un Blackjack natural: 21 puntos con dos cartas."""
    return len(mano) == 2 and calcular_puntuacion(mano) == 21


def se_pasa(mano):
    """True si la puntuación de la mano es mayor que 21."""
    return calcular_puntuacion(mano) > 21


def determinar_ganador(mano_jugador, mano_banca):
    """Compara las manos y devuelve (resultado, mensaje).

    resultado puede ser: 'jugador', 'banca' o 'empate'.
    """
    puntos_jugador = calcular_puntuacion(mano_jugador)
    puntos_banca = calcular_puntuacion(mano_banca)
    blackjack_jugador = es_blackjack(mano_jugador)
    blackjack_banca = es_blackjack(mano_banca)
        

    if se_pasa(mano_jugador):
        return ("banca", "Te has pasado de 21. Gana la banca.")

    if se_pasa(mano_banca):
        return ("jugador", "La banca se ha pasado de 21. ¡Has ganado!")

    if blackjack_jugador and blackjack_banca:
        return ("empate", "Ambos tenéis Blackjack. Empate.")

    if blackjack_jugador:
        return ("jugador", "¡Blackjack! Has ganado.")

    if blackjack_banca:
        return ("banca", "La banca tiene Blackjack. Gana la banca.")


    if puntos_jugador > puntos_banca:
        return (
            "jugador",
            f"Has ganado con {puntos_jugador} puntos frente a {puntos_banca}.",
        )

    if puntos_banca > puntos_jugador:
        return (
            "banca",
            f"Gana la banca con {puntos_banca} puntos frente a {puntos_jugador}.",
        )

    return ("empate", f"Empate a {puntos_jugador} puntos.")
