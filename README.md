# Who's Your Pokémon!

A Python-based "Guess Who" inspired game where two players try to guess each other's chosen Pokémon. Features **all 1,280+ Pokémon** with official sprites from the PokéAPI!

## Features

- **Complete Pokédex**: All Pokémon from the PokéAPI with official sprites
- **Enhanced Autocomplete**: Type to search through 1,280+ Pokémon with fuzzy matching, featuring:
  - **Visual Suggestions**: Pokémon sprites displayed alongside names in dropdown
  - **Smart Filtering**: Real-time search with immediate visual feedback
  - **Local Image Caching**: Fast loading with pre-downloaded Pokémon images
- **Manual Grid Setup**: Players can manually select all 24 Pokémon for their grid
  - **Interactive Grid Builder**: Visual 6x4 grid with autocomplete for each position
  - **Duplicate Prevention**: Once selected, Pokémon are removed from other autocomplete options
  - **Visual Feedback**: Selected Pokémon highlighted, empty slots show Pokéballs
- **Visual Gameplay**: Uniform grid with properly sized Pokémon sprites and names
- **Intuitive Interface**: Clean design with modern UI components and consistent styling
- **Cross-platform GUI**: Optimized window interface using tkinter
- **Two-Player Gameplay**: Alternating turns between players
- **Interactive Grids**: 6x4 grids of clickable Pokémon buttons for each player
- **Real-time Feedback**: Visual indicators for eliminated Pokémon and current player
- **Multiple Win Conditions**: Win by correct guess or lose by eliminating your target
- **Generation Selection**: Choose which Pokémon generations to include in the game
- **Variant Selection**: Include regional variants, Mega evolutions, Gigantamax forms, and more
- **Flexible Selection**: Choose between randomized grid generation or manual grid setup

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

3. **First-time setup**: Run the Pokémon data service to fetch all Pokémon data and download images:
   ```bash
   python3 data_sources/pokemon_data_service.py
   ```
   This will create a `data_sources/pokemon_data.json` file with all Pokémon names and sprite URLs, and download all Pokémon images to `assets/pokemon_images/` for faster loading.

## How to Run

```bash
python3 main.py
```

**Note**: The first time you play, the game will load quickly using pre-downloaded Pokémon sprites from the local assets folder.

## How to Play

1. **Start**: Click the "Start" button on the main screen
2. **Generation Selection**: Choose which Pokémon generations you want to include in the game
3. **Game Settings**: Configure variant inclusion and Pokémon selection method (randomized or manual)
4. **Player Setup**: Each player enters their name and chooses a Pokémon using the enhanced autocomplete search with visual sprites
5. **Manual Grid Setup** (if selected): 
   - Each player sets up their 6x4 grid by selecting Pokémon for each position
   - Use autocomplete with visual previews to choose Pokémon
   - Selected Pokémon are highlighted and removed from other position options
   - Confirm button activates only when all 24 positions are filled
6. **Gameplay**:
   - Players take turns eliminating Pokémon from their opponent's grid
   - Click on opponent's Pokémon sprites to mark them with a red 'X'
   - Click again to unmark (toggle functionality)
   - Use "End Turn" to switch to the other player
   - Use "Make Guess" to guess the opponent's chosen Pokémon (with autocomplete search and sprites)
7. **Winning**:
   - **Win**: Correctly guess the opponent's chosen Pokémon
   - **Lose**: Accidentally eliminate the opponent's chosen Pokémon or make an incorrect guess

## Pokémon Data

The game uses the [PokéAPI](https://pokeapi.co/) to provide:
- **1,280+ Pokémon** from all generations
- **Official sprite images** for visual gameplay
- **Local image caching** for instant loading and offline gameplay
- **Automatic data caching** for faster subsequent plays

### Updating Pokémon Data

To refresh the Pokémon database with the latest data and re-download all images:
```bash
python3 data_sources/pokemon_data_service.py
```

This will update both the JSON data file and refresh all Pokémon images in the `assets/pokemon_images/` directory.

## Recent Updates

### Version 2.0 - Enhanced Visual Experience & Manual Grid Setup

**Major Features Added:**
- **Manual Grid Setup**: Players can now manually select all 24 Pokémon for their grid instead of random generation
- **Visual Autocomplete**: Enhanced autocomplete widget with Pokémon sprite previews
- **Local Image Caching**: All Pokémon images are pre-downloaded for instant loading
- **Improved UI/UX**: Consistent styling, better visual feedback, and responsive design

**Technical Improvements:**
- Enhanced autocomplete with fuzzy search and visual suggestions
- Duplicate prevention system in manual grid setup
- Optimized image loading with local asset management
- Improved grid state management and validation
- Better error handling and user feedback

**Performance Enhancements:**
- Instant sprite loading using local image cache
- Reduced API calls through local asset storage
- Optimized autocomplete rendering and scrolling
- Improved memory management for large sprite collections

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
│   │   ├── game_settings_screen.py
│   │   ├── player_setup_screen.py
│   │   ├── pokemon_grid_setup_screen.py  # Manual grid setup
│   │   ├── game_screen.py
│   │   └── game_over_screen.py
│   ├── widgets/              # Custom UI components
│   │   └── autocomplete_entry.py  # Enhanced with sprite support
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
│   ├── game-settings-logo.png
│   ├── player-setup-logo.png
│   ├── pokemon-grid-setup-logo.png  # Manual grid setup logo
│   ├── game-over-logo.png
│   ├── question_mark.png
│   ├── pokeball.png          # Used in manual grid setup
│   ├── x_icon.png
│   └── pokemon_images/       # Local cache of all Pokémon sprites
│       ├── Pikachu.png
│       ├── Charizard.png
│       └── [1,280+ Pokémon images]
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
- **Local Asset Management**: Pre-downloaded Pokémon images for optimal performance
- **Enhanced Autocomplete**: Visual suggestions with sprite previews and fuzzy search
- **Manual Grid Setup**: Interactive grid builder with duplicate prevention

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

- Adding more game modes and gameplay variations
- Implementing sound effects and animations
- Improving UI/UX design and accessibility
- Adding network multiplayer support
- Performance optimizations and code improvements
- Enhanced visual effects and transitions
- Additional Pokémon data integration (stats, types, etc.)

## License

This project is licensed under the terms specified in the LICENSE file. Pokémon is a trademark of Nintendo/Game Freak.
