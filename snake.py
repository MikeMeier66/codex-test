#!/usr/bin/env python3
"""Ein einfaches Snake-Spiel für das Terminal unter Verwendung von curses."""

from __future__ import annotations

import curses
import os
import random
import sys
import time
from typing import List, Tuple


Position = Tuple[int, int]


def platzieren_futter(max_y: int, max_x: int, schlange: List[Position]) -> Position:
    """Platziert das Futter an einer zufälligen Position, die nicht von der Schlange belegt ist."""
    freie_felder = [
        (y, x)
        for y in range(1, max_y - 1)
        for x in range(1, max_x - 1)
        if (y, x) not in schlange
    ]
    if not freie_felder:
        return 1, 1
    return random.choice(freie_felder)


def sicher_addch(stdscr: "curses._CursesWindow", y: int, x: int, ch: str) -> None:
    """Schreibt ein Zeichen und ignoriert Fehler, die bei engen Grenzen auftreten."""
    try:
        stdscr.addch(y, x, ch)
    except curses.error:
        pass


def sicher_addstr(stdscr: "curses._CursesWindow", y: int, x: int, text: str) -> None:
    try:
        stdscr.addstr(y, x, text)
    except curses.error:
        pass


def spiel_loop(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.timeout(100)

    max_y, max_x = stdscr.getmaxyx()

    # Startposition der Schlange in der Mitte des Spielfelds
    start_y, start_x = max_y // 2, max_x // 2
    schlange: List[Position] = [
        (start_y, start_x + i)
        for i in range(3, -1, -1)
    ]
    aktuelle_richtung = curses.KEY_RIGHT

    futter = platzieren_futter(max_y, max_x, schlange)
    punkte = 0

    while True:
        stdscr.erase()

        # Spielfeld-Rand zeichnen
        for x in range(max_x):
            sicher_addch(stdscr, 0, x, "#")
            sicher_addch(stdscr, max_y - 1, x, "#")
        for y in range(max_y):
            sicher_addch(stdscr, y, 0, "#")
            sicher_addch(stdscr, y, max_x - 1, "#")

        # Futter zeichnen
        sicher_addch(stdscr, futter[0], futter[1], "*")

        # Schlange zeichnen
        for index, (y, x) in enumerate(schlange):
            sicher_addch(stdscr, y, x, "@" if index == 0 else "o")

        sicher_addstr(stdscr, 0, 2, f" Punkte: {punkte} ")
        stdscr.refresh()

        try:
            taste = stdscr.getch()
        except curses.error:
            taste = -1

        if taste in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            gegenteil = {
                curses.KEY_UP: curses.KEY_DOWN,
                curses.KEY_DOWN: curses.KEY_UP,
                curses.KEY_LEFT: curses.KEY_RIGHT,
                curses.KEY_RIGHT: curses.KEY_LEFT,
            }
            if gegenteil[taste] != aktuelle_richtung:
                aktuelle_richtung = taste

        kopf_y, kopf_x = schlange[0]
        if aktuelle_richtung == curses.KEY_RIGHT:
            kopf_x += 1
        elif aktuelle_richtung == curses.KEY_LEFT:
            kopf_x -= 1
        elif aktuelle_richtung == curses.KEY_UP:
            kopf_y -= 1
        elif aktuelle_richtung == curses.KEY_DOWN:
            kopf_y += 1

        neuer_kopf = (kopf_y, kopf_x)
        wird_wachsen = neuer_kopf == futter

        # Kollisionen prüfen
        koerper_ohne_schwanz = schlange if wird_wachsen else schlange[:-1]
        if (
            kopf_y in (0, max_y - 1)
            or kopf_x in (0, max_x - 1)
            or neuer_kopf in koerper_ohne_schwanz
        ):
            break

        schlange.insert(0, neuer_kopf)

        if wird_wachsen:
            punkte += 1
            futter = platzieren_futter(max_y, max_x, schlange)
        else:
            schlange.pop()

        time.sleep(0.05)

    stdscr.nodelay(False)
    nachricht = f"Game Over! Punkte: {punkte}. Drücke eine Taste zum Beenden."
    sicher_addstr(stdscr, max_y // 2, max(0, (max_x - len(nachricht)) // 2), nachricht)
    stdscr.refresh()
    stdscr.getch()


def main() -> None:
    if os.environ.get("SNAKE_NO_CURSES") == "1" or not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("Dieses Spiel benötigt ein interaktives Terminal (TTY).")
        return

    try:
        curses.wrapper(spiel_loop)
    except (curses.error, OSError):
        # Fallback, falls das Terminal curses nicht unterstützt.
        print("Konnte curses nicht initialisieren. Bitte in einem kompatiblen Terminal ausführen.")


if __name__ == "__main__":
    random.seed(os.environ.get("SNAKE_RANDOM_SEED"))
    main()
