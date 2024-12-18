import platform
import pyautogui

# Get screen resolution
screen_width, screen_height = pyautogui.size()

def get_scaling_factor():
    if platform.system() == 'Windows':
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screen_width_actual = user32.GetSystemMetrics(0)
        scaling_factor = screen_width_actual / screen_width
        return scaling_factor
    else:
        # For macOS and other systems, return a scaling factor of 1
        return 1

scaling_factor = get_scaling_factor()

def to_relative(x, y):
    return (x / screen_width, y / screen_height)

def to_absolute(rel_x, rel_y):
    abs_x = int(rel_x * screen_width * scaling_factor)
    abs_y = int(rel_y * screen_height * scaling_factor)
    print(f"Conversion of relative coordinates ({rel_x}, {rel_y}) to absolute ({abs_x}, {abs_y})")
    return abs_x, abs_y

def to_absolute_size(rel_w, rel_h):
    abs_w = int(rel_w * screen_width * scaling_factor)
    abs_h = int(rel_h * screen_height * scaling_factor)
    print(f"Conversion of relative sizes ({rel_w}, {rel_h}) to absolute ({abs_w}, {abs_h})")
    return abs_w, abs_h