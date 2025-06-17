"""
Font configuration for cross-platform compatibility
"""
from .platform_utils import get_font_config


class FontManager:
    """Manages fonts across different platforms"""
    
    def __init__(self):
        self._fonts = {}
    
    def get_font(self, size=12, weight='normal'):
        """Get a platform-appropriate font"""
        key = f"{size}_{weight}"
        if key not in self._fonts:
            self._fonts[key] = get_font_config(size, weight)
        return self._fonts[key]
    
    def get_title_font(self):
        """Get font for titles"""
        return self.get_font(24, 'bold')
    
    def get_subtitle_font(self):
        """Get font for subtitles"""
        return self.get_font(16, 'bold')
    
    def get_body_font(self):
        """Get font for body text"""
        return self.get_font(12, 'normal')
    
    def get_small_font(self):
        """Get font for small text"""
        return self.get_font(10, 'normal')
    
    def get_button_font(self):
        """Get font for buttons"""
        return self.get_font(14, 'normal')
    
    def get_entry_font(self):
        """Get font for text entries"""
        return self.get_font(14, 'normal')
    
    def get_grid_font(self):
        """Get font for grid labels"""
        return self.get_font(7, 'bold')
    
    def get_large_display_font(self):
        """Get font for large display text"""
        return self.get_font(48, 'bold')


# Global font manager instance
font_manager = FontManager()


def get_title_font():
    """Convenience function for title font"""
    return font_manager.get_title_font()


def get_subtitle_font():
    """Convenience function for subtitle font"""
    return font_manager.get_subtitle_font()


def get_body_font():
    """Convenience function for body font"""
    return font_manager.get_body_font()


def get_small_font():
    """Convenience function for small font"""
    return font_manager.get_small_font()


def get_button_font():
    """Convenience function for button font"""
    return font_manager.get_button_font()


def get_entry_font():
    """Convenience function for entry font"""
    return font_manager.get_entry_font()


def get_grid_font():
    """Convenience function for grid font"""
    return font_manager.get_grid_font()


def get_large_display_font():
    """Convenience function for large display font"""
    return font_manager.get_large_display_font()
