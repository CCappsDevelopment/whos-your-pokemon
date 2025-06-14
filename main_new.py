#!/usr/bin/env python3
"""
Who's Your Pokémon! - A Python-based "Guess Who" inspired game
A two-player game where players try to guess each other's chosen Pokémon.

Main entry point for the application.
"""

from src import PokemonGuessGame


def main():
    """Main entry point for the application"""
    game = PokemonGuessGame()
    game.run()


if __name__ == "__main__":
    main()
