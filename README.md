# Who's Your Pokémon!

A Python-based "Guess Who" inspired game where two players try to guess each other's chosen Pokémon. Features **all 1,280+ Pokémon** with official sprites from the PokéAPI!

## Features

- **Complete Pokédex**: All Pokémon from the PokéAPI with official sprites
- **Smart Autocomplete**: Type to search through 1,280+ Pokémon with fuzzy matching
- **Visual Gameplay**: Uniform grid with properly sized Pokémon sprites
- **Intuitive Interface**: Clean design with modern UI components
- **Cross-platform GUI**: Optimized window interface using tkinter
- **Two-Player Gameplay**: Alternating turns between players
- **Interactive Grids**: 6x4 grids of clickable Pokémon buttons for each player
- **Real-time Feedback**: Visual indicators for eliminated Pokémon and current player
- **Multiple Win Conditions**: Win by correct guess or lose by eliminating your target
- **Generation Selection**: Choose which Pokémon generations to include in the game

## Requirements

- Python 3.7+
- tkinter (included with Python)
- Pillow (for image handling)
- requests (for API calls)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/CCappsDevelopment/whos-your-pokemon.git
   cd whos-your-pokemon
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **First-time setup**: Run the Pokémon data service to fetch all Pokémon data:
   ```bash
   python3 data_sources/pokemon_data_service.py
   ```
   This will create a `data_sources/pokemon_data.json` file with all Pokémon names and sprite URLs.

## How to Run

```bash
python3 main.py
```

**Note**: The first time you play, it may take a moment to download Pokémon sprites from the internet.

## How to Play

1. **Start**: Click the "Start" button on the main screen
2. **Generation Selection**: Choose which Pokémon generations you want to include in the game
3. **Player Setup**: Each player enters their name and chooses a Pokémon using the smart autocomplete search
4. **Gameplay**:
   - Players take turns eliminating Pokémon from their opponent's grid
   - Click on opponent's Pokémon sprites to mark them with a red 'X'
   - Click again to unmark (toggle functionality)
   - Use "End Turn" to switch to the other player
   - Use "Make Guess" to guess the opponent's chosen Pokémon (also with autocomplete search)
5. **Winning**:
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
python3 data_sources/pokemon_data_service.py
```

## Project Structure

```
whos-your-pokemon/
├── main.py                    # Main game application entry point
├── requirements.txt           # Python dependencies
├── LICENSE                    # Project license
├── README.md                  # This file
├── ARCHITECTURE.md           # Project architecture documentation
├── Whos Your Pokemon.spec    # PyInstaller build specification
│
├── src/                      # Source code modules
│   ├── data/                 # Data management
│   │   └── pokemon_data_manager.py
│   ├── game/                 # Core game logic
│   │   └── pokemon_game.py
│   ├── screens/              # UI screens
│   │   ├── base_screen.py
│   │   ├── startup_screen.py
│   │   ├── generation_selection_screen.py
│   │   ├── player_setup_screen.py
│   │   ├── game_screen.py
│   │   └── game_over_screen.py
│   ├── widgets/              # Custom UI components
│   │   └── autocomplete_entry.py
│   └── utils/                # Utility functions
│       ├── image_loader.py
│       └── resource_path.py
│
├── data_sources/             # Pokémon data and services
│   ├── pokemon_data_service.py
│   ├── pokemon_data.json
│   └── pokemon_data_backup.json
│
├── assets/                   # Game assets
│   ├── whos-your-pokemon-logo.png
│   ├── select-generations-logo.png
│   ├── player-setup-logo.png
│   ├── game-over-logo.png
│   ├── question_mark.png
│   └── x_icon.png
│
├── build_tools/              # Build and deployment tools
│   ├── build_app.py
│   ├── build.sh
│   ├── create_release.sh
│   └── BUILD_INSTRUCTIONS.md
│
├── build/                    # Build output directory
├── dist/                     # Distribution files
└── test_files/               # Test and development files
```

## Controls

- **Mouse**: Click to interact with buttons and Pokémon grid
- **Enter**: Submit forms during player setup
- **Escape**: Exit fullscreen mode (when in fullscreen)

## Technical Details

- **Framework**: tkinter (cross-platform GUI)
- **Architecture**: Modular object-oriented design
- **Grid System**: 6x4 button layout with dynamic content
- **State Management**: Comprehensive game state tracking
- **UI/UX**: Modern responsive design with visual feedback
- **Data Management**: JSON-based Pokémon data caching
- **Image Handling**: Pillow for sprite processing and display

## Building Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python3 build_tools/build_app.py
   ```

The executable will be created in the `dist/` directory.

## Troubleshooting

**Display Problems**: The game is designed to work on various screen sizes, but optimal experience is on screens 1200x800 or larger.

**Performance**: The game should run smoothly on most modern systems. If you experience lag, try closing other applications.

**Missing Pokémon Data**: If Pokémon don't load, run the data service script to refresh the database.

## Contributing

This project welcomes contributions! Key areas for enhancement:

- Adding more game modes
- Implementing sound effects and animations
- Improving UI/UX design
- Adding network multiplayer support
- Performance optimizations

## License

This project is licensed under the terms specified in the LICENSE file. Pokémon is a trademark of Nintendo/Game Freak.
