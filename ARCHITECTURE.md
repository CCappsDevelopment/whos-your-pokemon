# Project Structure

This document describes the refactored modular structure of the Pokemon Guess Game.

## Directory Structure

```
├── main.py                    # Application entry point (minimal launcher)
├── src/                       # Main source code package
│   ├── __init__.py
│   ├── game/                  # Game controller and main logic
│   │   ├── __init__.py
│   │   └── pokemon_game.py    # Main game class with core logic
│   ├── screens/               # Individual game screens
│   │   ├── __init__.py
│   │   ├── base_screen.py     # Base class for all screens
│   │   ├── startup_screen.py  # Initial startup screen
│   │   ├── game_settings_screen.py  # Game settings (generations, variants, selection)
│   │   ├── player_setup_screen.py  # Player name and Pokemon selection
│   │   ├── game_screen.py     # Main game interface
│   │   └── game_over_screen.py  # End game results
│   ├── widgets/               # Custom tkinter widgets
│   │   ├── __init__.py
│   │   └── autocomplete_entry.py  # Autocomplete text entry widget
│   ├── utils/                 # Utility modules
│   │   ├── __init__.py
│   │   ├── resource_path.py   # Resource path handling for PyInstaller
│   │   └── image_loader.py    # Image loading and caching
│   └── data/                  # Data management
│       ├── __init__.py
│       └── pokemon_data_manager.py  # Pokemon data loading and filtering
├── assets/                    # Image assets and logos
├── data_sources/              # Pokemon data and API scripts
├── test_files/                # Test files and mockups
├── build_tools/               # Build scripts and utilities
└── dist/                      # Built application output
```

## Key Benefits of This Structure

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Game logic separated from UI presentation
- Data management isolated from business logic

### 2. **Maintainability**
- Easy to locate and modify specific functionality
- Clear dependencies between modules
- Easier debugging and testing

### 3. **Scalability**
- New screens can be added easily by extending BaseScreen
- New widgets can be added to the widgets package
- Game logic can be extended without touching UI code

### 4. **Reusability**
- Widgets can be reused across different screens
- Utility functions are available throughout the application
- Screen classes can be extended or customized

## Module Descriptions

### `src/game/pokemon_game.py`
Main game controller containing:
- Game state management
- Player data handling
- Generation selection logic
- Grid generation and management
- Turn management and game flow

### `src/screens/`
Individual screen classes, each responsible for:
- UI layout and styling
- User interaction handling
- Communication with game controller
- Screen-specific logic

### `src/widgets/autocomplete_entry.py`
Custom autocomplete widget with:
- Fuzzy search functionality
- Keyboard navigation
- Mouse interaction
- Visual feedback

### `src/utils/`
Utility modules for:
- Resource path resolution (PyInstaller compatibility)
- Image loading and caching
- Common helper functions

### `src/data/pokemon_data_manager.py`
Data management for:
- Pokemon data loading from JSON
- Generation-based filtering
- Sprite URL management
- Data validation

## Running the Application

### Development
```bash
python main.py
```

### Building
```bash
python build.py
```

## Adding New Features

### New Screen
1. Create new class in `src/screens/` extending `BaseScreen`
2. Implement `show()` method with UI layout
3. Add to screens `__init__.py`
4. Initialize in `pokemon_game.py`

### New Widget
1. Create new widget class in `src/widgets/`
2. Add to widgets `__init__.py`
3. Import and use in screen classes

### New Utility
1. Create new module in `src/utils/`
2. Add to utils `__init__.py`
3. Import where needed

This modular structure makes the codebase much more maintainable and follows Python best practices for large tkinter applications.

### Enhanced Game Settings System

The `game_settings_screen.py` now provides comprehensive configuration options:

#### Generation Selection
- Choose specific Pokémon generations (I-IX)
- Master "All Generations" checkbox for quick selection
- Individual generation toggles with region names

#### Variant Selection
- Regional variants (Alolan, Galarian, Hisuian, Paldean)
- Special forms (Mega Evolution, Gigantamax)
- Unique Pokémon (Special Pikachus, Totem Pokémon, Paradox Pokémon)
- Form and size variants
- Master "All Variants" checkbox for easy management

#### Pokémon Selection Method
- **Randomize**: Automatically select 24 Pokémon for each player (current implementation)
- **Manual**: Allow players to manually choose their Pokémon pool (coming soon)

### Enhanced Data Management

The Pokémon data now includes:
- **Name**: Formatted Pokémon name
- **Sprite URL**: Best available sprite from PokéAPI
- **Generation**: Numeric generation (1-9, or -1 for unknown)
- **Variant**: Classification of variant type (null for standard Pokémon)

Data filtering supports both generation and variant criteria, always including standard (non-variant) Pokémon in gameplay.
