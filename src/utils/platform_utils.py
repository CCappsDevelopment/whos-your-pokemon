"""
Cross-platform utilities for the Pokemon Guess Game
Handles platform-specific differences in functionality
"""
import platform
import tkinter as tk


def get_platform_info():
    """Get detailed platform information"""
    system = platform.system().lower()
    return {
        'system': system,
        'is_windows': system == 'windows',
        'is_macos': system == 'darwin',
        'is_linux': system == 'linux',
        'version': platform.version(),
        'machine': platform.machine()
    }


def bind_mousewheel(widget, callback):
    """
    Bind mouse wheel events across platforms
    
    Args:
        widget: The tkinter widget to bind to
        callback: Function to call on scroll. Should accept (direction) parameter
                 where direction is 1 for up, -1 for down
    """
    platform_info = get_platform_info()
    
    def mousewheel_handler(event):
        """Handle mouse wheel events cross-platform"""
        if platform_info['is_windows']:
            # Windows uses event.delta (multiples of 120)
            direction = 1 if event.delta > 0 else -1
            callback(direction)
        elif platform_info['is_macos']:
            # macOS uses event.delta (can be any value)
            direction = 1 if event.delta > 0 else -1
            callback(direction)
        elif platform_info['is_linux']:
            # Linux uses different button events
            if event.num == 4:  # Scroll up
                callback(1)
            elif event.num == 5:  # Scroll down
                callback(-1)
    
    # Bind the appropriate events for each platform
    if platform_info['is_linux']:
        # Linux uses Button-4 and Button-5 for mouse wheel
        widget.bind("<Button-4>", mousewheel_handler)
        widget.bind("<Button-5>", mousewheel_handler)
    else:
        # Windows and macOS use MouseWheel
        widget.bind("<MouseWheel>", mousewheel_handler)


def get_modifier_key():
    """
    Get the primary modifier key for each platform
    Returns the key name used in tkinter bindings
    """
    platform_info = get_platform_info()
    
    if platform_info['is_macos']:
        return 'Command'  # Cmd key on Mac
    else:
        return 'Control'  # Ctrl key on Windows/Linux


def bind_copy_paste(widget, copy_callback=None, paste_callback=None):
    """
    Bind copy/paste shortcuts appropriately for each platform
    
    Args:
        widget: The tkinter widget to bind to
        copy_callback: Function to call for copy operation
        paste_callback: Function to call for paste operation
    """
    modifier = get_modifier_key()
    
    if copy_callback:
        widget.bind(f"<{modifier}-c>", lambda e: copy_callback())
    
    if paste_callback:
        widget.bind(f"<{modifier}-v>", lambda e: paste_callback())


def get_font_family():
    """
    Get appropriate font family for each platform
    Returns a font family name that should be available
    """
    platform_info = get_platform_info()
    
    if platform_info['is_macos']:
        return 'Helvetica'  # Standard on macOS
    elif platform_info['is_windows']:
        return 'Segoe UI'   # Modern Windows font
    else:  # Linux
        return 'DejaVu Sans'  # Common Linux font


def get_font_config(size=12, weight='normal'):
    """
    Get platform-appropriate font configuration
    
    Args:
        size: Font size
        weight: Font weight ('normal', 'bold')
    
    Returns:
        Tuple of (family, size, weight) for tkinter font configuration
    """
    family = get_font_family()
    
    # Adjust size slightly for different platforms if needed
    platform_info = get_platform_info()
    if platform_info['is_linux']:
        # Linux often needs slightly larger fonts
        size = max(size, 10)
    
    return (family, size, weight)


def configure_widget_appearance(widget, **kwargs):
    """
    Configure widget appearance with platform-specific adjustments
    
    Args:
        widget: The tkinter widget to configure
        **kwargs: Style parameters to apply
    """
    platform_info = get_platform_info()
    
    # Apply base configuration
    if kwargs:
        widget.configure(**kwargs)
    
    # Platform-specific adjustments
    if platform_info['is_macos']:
        # macOS might need specific relief styles
        if hasattr(widget, 'configure'):
            try:
                # Ensure buttons look native on macOS
                if isinstance(widget, tk.Button):
                    widget.configure(relief='raised', borderwidth=1)
            except tk.TclError:
                pass  # Some options might not be available
    
    elif platform_info['is_linux']:
        # Linux might need specific border adjustments
        if hasattr(widget, 'configure'):
            try:
                # Ensure consistent appearance on Linux
                if isinstance(widget, (tk.Entry, tk.Text)):
                    widget.configure(relief='sunken', borderwidth=2)
            except tk.TclError:
                pass


def get_window_manager_info():
    """
    Get information about the window manager (mainly for Linux)
    Returns info that might affect window behavior
    """
    platform_info = get_platform_info()
    
    if platform_info['is_linux']:
        try:
            import subprocess
            # Try to detect the desktop environment
            desktop = subprocess.check_output(['echo', '$XDG_CURRENT_DESKTOP'], 
                                            shell=True, text=True).strip()
            return {'desktop_environment': desktop}
        except:
            return {'desktop_environment': 'unknown'}
    
    return {}


def adjust_window_for_platform(window):
    """
    Apply platform-specific window adjustments
    
    Args:
        window: The tkinter Toplevel or Tk window
    """
    platform_info = get_platform_info()
    
    if platform_info['is_macos']:
        # macOS specific window settings
        try:
            # Enable high DPI support
            window.tk.call('tk', 'scaling', 2.0)
        except:
            pass
    
    elif platform_info['is_windows']:
        # Windows specific settings
        try:
            # Better DPI awareness
            window.wm_attributes('-dpiaware', True)
        except:
            pass
    
    elif platform_info['is_linux']:
        # Linux specific settings
        try:
            # Some window managers need this for proper centering
            window.update_idletasks()
        except:
            pass


def get_key_binding_display(key_combo):
    """
    Convert key binding to platform-appropriate display string
    
    Args:
        key_combo: Key combination like 'Control-c' or 'Command-c'
    
    Returns:
        Human-readable string for display in UI
    """
    platform_info = get_platform_info()
    
    if platform_info['is_macos']:
        # Convert to Mac-style display
        return key_combo.replace('Control', '⌃').replace('Command', '⌘').replace('Option', '⌥')
    else:
        # Windows/Linux style
        return key_combo.replace('Control', 'Ctrl')
