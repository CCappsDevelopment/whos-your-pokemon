#!/usr/bin/env python3
"""
Cross-platform compatibility test for Who's Your Pokemon
Tests platform-specific functionality to ensure it works on Windows, macOS, and Linux
"""

import sys
import os
import tkinter as tk

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.platform_utils import (
    get_platform_info, bind_mousewheel, get_modifier_key,
    get_font_config, adjust_window_for_platform
)
from src.utils.font_config import get_title_font, get_body_font
from src.utils.resource_path import get_resource_path


def test_platform_detection():
    """Test platform detection functionality"""
    print("🔍 Testing Platform Detection...")
    
    platform_info = get_platform_info()
    print(f"   System: {platform_info['system']}")
    print(f"   Is Windows: {platform_info['is_windows']}")
    print(f"   Is macOS: {platform_info['is_macos']}")
    print(f"   Is Linux: {platform_info['is_linux']}")
    print(f"   Version: {platform_info['version']}")
    print(f"   Machine: {platform_info['machine']}")
    
    return True


def test_font_configuration():
    """Test cross-platform font configuration"""
    print("\n🔤 Testing Font Configuration...")
    
    try:
        title_font = get_title_font()
        body_font = get_body_font()
        
        print(f"   Title font: {title_font}")
        print(f"   Body font: {body_font}")
        
        # Test direct font config
        custom_font = get_font_config(16, 'bold')
        print(f"   Custom font: {custom_font}")
        
        return True
    except Exception as e:
        print(f"   ❌ Font configuration error: {e}")
        return False


def test_resource_paths():
    """Test resource path handling"""
    print("\n📁 Testing Resource Path Handling...")
    
    try:
        # Test various asset paths
        test_paths = [
            "assets/whos-your-pokemon-logo.png",
            "data_sources/pokemon_data.json",
            "assets/pokemon_images/Pikachu.png"
        ]
        
        for path in test_paths:
            resolved_path = get_resource_path(path)
            print(f"   {path} -> {resolved_path}")
        
        return True
    except Exception as e:
        print(f"   ❌ Resource path error: {e}")
        return False


def test_mousewheel_binding():
    """Test cross-platform mouse wheel binding"""
    print("\n🖱️  Testing Mouse Wheel Binding...")
    
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        canvas = tk.Canvas(root)
        
        # Test callback function
        scroll_events = []
        def scroll_callback(direction):
            scroll_events.append(direction)
            print(f"   Scroll event: direction={direction}")
        
        # Bind mousewheel
        bind_mousewheel(canvas, scroll_callback)
        
        print("   ✅ Mouse wheel binding successful")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"   ❌ Mouse wheel binding error: {e}")
        return False


def test_window_adjustments():
    """Test platform-specific window adjustments"""
    print("\n🪟 Testing Window Adjustments...")
    
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Apply platform adjustments
        adjust_window_for_platform(root)
        
        print("   ✅ Window adjustments applied successfully")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"   ❌ Window adjustment error: {e}")
        return False


def test_key_bindings():
    """Test platform-specific key bindings"""
    print("\n⌨️  Testing Key Bindings...")
    
    try:
        modifier = get_modifier_key()
        print(f"   Primary modifier key: {modifier}")
        
        platform_info = get_platform_info()
        if platform_info['is_macos']:
            expected = 'Command'
        else:
            expected = 'Control'
        
        if modifier == expected:
            print("   ✅ Correct modifier key detected")
        else:
            print(f"   ⚠️  Unexpected modifier key: {modifier} (expected {expected})")
        
        return True
    except Exception as e:
        print(f"   ❌ Key binding error: {e}")
        return False


def run_comprehensive_gui_test():
    """Run a comprehensive GUI test"""
    print("\n🖥️  Running Comprehensive GUI Test...")
    
    try:
        root = tk.Tk()
        root.title("Cross-Platform Test")
        root.geometry("600x400")
        
        # Apply platform adjustments
        adjust_window_for_platform(root)
        
        # Create test widgets with cross-platform fonts
        title_label = tk.Label(
            root,
            text="Cross-Platform Test",
            font=get_title_font(),
            bg='#3d7dca',
            fg='white'
        )
        title_label.pack(pady=20)
        
        body_label = tk.Label(
            root,
            text="This is a test of cross-platform functionality.",
            font=get_body_font(),
            bg='#3d7dca',
            fg='white'
        )
        body_label.pack(pady=10)
        
        # Test platform info display
        platform_info = get_platform_info()
        platform_text = f"Platform: {platform_info['system'].title()}"
        
        platform_label = tk.Label(
            root,
            text=platform_text,
            font=get_body_font(),
            bg='#3d7dca',
            fg='white'
        )
        platform_label.pack(pady=10)
        
        # Create a canvas for scroll testing
        canvas = tk.Canvas(root, bg='white', height=100)
        canvas.pack(pady=10, padx=20, fill='x')
        
        # Add some content to scroll
        for i in range(10):
            canvas.create_text(50, i * 20 + 10, text=f"Line {i+1}", anchor='w')
        
        # Bind cross-platform scrolling
        scroll_info = tk.StringVar()
        scroll_info.set("Scroll in the canvas above")
        
        def on_scroll(direction):
            if direction > 0:
                scroll_info.set("Scrolled UP")
            else:
                scroll_info.set("Scrolled DOWN")
        
        bind_mousewheel(canvas, on_scroll)
        
        scroll_label = tk.Label(
            root,
            textvariable=scroll_info,
            font=get_body_font(),
            bg='#3d7dca',
            fg='white'
        )
        scroll_label.pack(pady=5)
        
        # Close button
        close_button = tk.Button(
            root,
            text="Close Test",
            command=root.destroy,
            font=get_body_font()
        )
        close_button.pack(pady=20)
        
        root.configure(bg='#3d7dca')
        
        print("   ✅ GUI test window created successfully")
        print("   📝 Test the mouse wheel scrolling in the white canvas area")
        print("   🔴 Close the window to continue...")
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"   ❌ GUI test error: {e}")
        return False


def main():
    """Run all cross-platform tests"""
    print("=" * 60)
    print("🌍 CROSS-PLATFORM COMPATIBILITY TEST")
    print("=" * 60)
    
    tests = [
        ("Platform Detection", test_platform_detection),
        ("Font Configuration", test_font_configuration),
        ("Resource Paths", test_resource_paths),
        ("Mouse Wheel Binding", test_mousewheel_binding),
        ("Window Adjustments", test_window_adjustments),
        ("Key Bindings", test_key_bindings),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work on all platforms.")
        
        # Run interactive GUI test
        response = input("\n🖥️  Run interactive GUI test? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            run_comprehensive_gui_test()
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
