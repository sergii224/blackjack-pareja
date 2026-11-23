"""
cartas.py — Gestión de la baraja y de las cartas del Blackjack.
"""

import random

PALOS = ("Corazones", "Diamantes", "Tréboles", "Picas")
VALORES = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")


def crear_carta(valor, palo):
    """Crea una carta como diccionario con valor y palo."""
    return {"valor": valor, "palo": palo}


def nombre_carta(carta):
    """Devuelve el nombre legible de una carta, por ejemplo 'A de Corazones'."""
    return f"{carta['valor']} de {carta['palo']}"


def crear_baraja():
    """Crea una baraja francesa de 52 cartas (13 valores por 4 palos)."""
    baraja = []
    for palo in PALOS:
        for valor in VALORES:
            baraja.append(crear_carta(valor, palo))
    return baraja


def barajar(baraja):
    """Baraja las cartas in situ y devuelve la misma lista."""
    random.shuffle(baraja)
    return baraja


def repartir(baraja, n=1):
    """Extrae y devuelve n cartas del final de la baraja.

    Siempre devuelve una lista, aunque se pida una sola carta.
    """
    if n < 1:
        raise ValueError("Hay que repartir al menos una carta.")
    if n > len(baraja):
        raise ValueError("No quedan suficientes cartas en la baraja.")
    cartas = []
    for _ in range(n):
        cartas.append(baraja.pop())
    return cartas
