#!/usr/bin/env python3
"""
Who's Your Pokémon! - A Python-based "Guess Who" inspired game
A two-player game where players try to guess each other's chosen Pokémon.

Main entry point for the application.
"""

from src import PokemonGuessGame


def main():
    """Main entry point for the application"""
    try:
        print("🎮 Starting Who's Your Pokemon...")
        game = PokemonGuessGame()
        print("✅ Game instance created successfully")
        game.run()
        print("✅ Game finished normally")
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        import traceback
        traceback.print_exc()
        # Keep console open in case of error
        try:
            input("Press Enter to exit...")
        except:
            pass


if __name__ == "__main__":
    main()
