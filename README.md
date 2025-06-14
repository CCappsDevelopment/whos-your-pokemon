# Who's Your Pokémon!

A Python-based "Guess Who" inspired game where two players try to guess each other's chosen Pokémon. Now featuring **all 1,280+ Pokémon** with official sprites from the PokéAPI!

## Features

- **Complete Pokédex**: All Pokémon from the PokéAPI with official sprites
- **Smart Autocomplete**: Type to search through 1,280+ Pokémon with fuzzy matching
- **Visual Gameplay**: Uniform grid with properly sized Pokémon sprites
- **Intuitive Interface**: Clean design with white text fields and blue buttons
- **Cross-platform GUI**: Optimized window interface using tkinter
- **Two-Player Gameplay**: Alternating turns between players
- **Interactive Grids**: 6x4 grids of clickable Pokémon buttons for each player
- **Real-time Feedback**: Visual indicators for eliminated Pokémon and current player
- **Multiple Win Conditions**: Win by correct guess or lose by eliminating your target

## Requirements

- Python 3.7+
- tkinter (included with Python)
- Pillow (for image handling)
- requests (for API calls)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **First-time setup**: Run the Pokémon data service to fetch all Pokémon data:
   ```bash
   python3 pokemon_data/pokemon_data_service.py
   ```
   This will create a `pokemon_data/pokemon_data.json` file with all Pokémon names and sprite URLs.

## How to Run

```bash
python3 main.py
```

**Note**: The game will open in a standard window. The first time you play, it may take a moment to download Pokémon sprites from the internet.

## How to Play

1. **Start**: Click the "Start" button on the main screen
2. **Player Setup**: Each player enters their name and chooses a Pokémon using the smart autocomplete search (start typing any Pokémon name!)
3. **Gameplay**:
   - Players take turns eliminating Pokémon from their opponent's grid
   - Click on opponent's Pokémon sprites to mark them with a red 'X'
   - Click again to unmark (toggle functionality)
   - Use "End Turn" to switch to the other player
   - Use "Make Guess" to guess the opponent's chosen Pokémon (also with autocomplete search)
4. **Winning**:
   - **Win**: Correctly guess the opponent's chosen Pokémon
   - **Lose**: Accidentally eliminate the opponent's chosen Pokémon or make an incorrect guess

## Pokémon Data

The game uses the [PokéAPI](https://pokeapi.co/) to provide:
- **1,280+ Pokémon** from all generations
- **Official sprite images** for visual gameplay
- **Automatic data caching** for faster subsequent plays

### Updating Pokémon Data

To refresh the Pokémon database with the latest data:
```bash
python3 pokemon_data/pokemon_data_service.py
```

## Files

- `main.py` - Main game application
- `pokemon_data/pokemon_data_service.py` - Service to fetch Pokémon data from PokéAPI
- `pokemon_data/pokemon_data.json` - Cached Pokémon names and sprite URLs
- `assets/` - Image assets (icons, sprites)
- `utils/` - Build scripts and utilities
- `tests/` - Test files and mockups
- `requirements.txt` - Python package dependencies

## How to Play

1. **Start**: Click the "Start" button on the main screen
2. **Player Setup**: Each player enters their name and chooses a Pokémon from the dropdown
3. **Gameplay**:
   - Players take turns eliminating Pokémon from their opponent's grid
   - Click on opponent's Pokémon to mark them with a red 'X'
   - Click again to unmark (toggle functionality)
   - Use "End Turn" to switch to the other player
   - Use "Make Guess" to guess the opponent's chosen Pokémon
4. **Winning**:
   - **Win**: Correctly guess the opponent's chosen Pokémon
   - **Lose**: Accidentally eliminate the opponent's chosen Pokémon or make an incorrect guess

## Controls

- **Mouse**: Click to interact with buttons and Pokémon grid
- **Enter**: Submit forms during player setup
- **Escape**: Exit fullscreen mode (when in fullscreen)

## Game Features

- **24 Pokémon**: Includes classic Generation 1 Pokémon
- **Smart Grid Generation**: Ensures each player's chosen Pokémon appears in their grid
- **Visual Feedback**: 
  - Green border around active player's name
  - Red 'X' overlay on eliminated Pokémon
  - Remaining count for each player
- **Error Handling**: Input validation and user-friendly error messages

## Technical Details

- **Framework**: tkinter (cross-platform GUI)
- **Architecture**: Object-oriented design with modular functions
- **Grid System**: 6x4 button layout with dynamic content
- **State Management**: Comprehensive game state tracking
- **UI/UX**: Responsive design with visual feedback

## Future Enhancements

- API integration for more Pokémon data
- Pokémon images support
- Sound effects and animations
- Different grid sizes
- AI opponent mode
- Network multiplayer support

## File Structure

```
Who's Your Pokemon/
├── main.py              # Main game application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Troubleshooting

**Fullscreen Issues**: If fullscreen doesn't work properly, the game will fall back to a maximized window. Use the Escape key to exit fullscreen mode.

**Display Problems**: The game is designed to work on various screen sizes, but optimal experience is on screens 1200x800 or larger.

**Performance**: The game should run smoothly on most modern systems. If you experience lag, try closing other applications.

## Contributing

This project is structured for easy enhancement and modification. Key areas for contribution:

- Adding more Pokémon to the list
- Implementing image support
- Adding sound effects
- Creating different game modes
- Improving UI/UX design

## License

This project is for educational and entertainment purposes. Pokémon is a trademark of Nintendo/Game Freak.
