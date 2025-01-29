from pygame import Color

# Game configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
BALL_SIZE = 100

class Theme:
    # Background and surface colors
    BACKGROUND = Color("#1E1E2E")  # Dark deep blue-gray
    SURFACE = Color("#2C2C40")  # Slightly lighter dark shade
    ACCENT = Color("#89DCEB")  # Soft cyan for highlights

    # Primary text and interactive elements
    TEXT_PRIMARY = Color("#D9E0EE")  # Light grayish white for high contrast text
    TEXT_SECONDARY = Color("#8E97A4")  # Muted gray for secondary text
    BUTTON = Color("#1C658C")  # Rich dark blue for buttons
    BUTTON_HOVER = Color("#4A94C9")  # Lighter blue on hover

    # Status-based colors
    SUCCESS = Color("#89F0A9")  # Pleasant green for positive feedback
    WARNING = Color("#FF9E64")  # Vivid orange for warnings
    ERROR = Color("#FF5370")  # Bright red for errors

    # Border and outlines
    BORDER = Color("#3B3F52")  # Subtle dark border for UI components
    SHADOW = Color("#14141F")  # Deep dark shadow for depth effects

    # Gradient or fancy effects (Optional extra)
    GRADIENT_START = Color("#1F1F35")  # Start of gradient for panels
    GRADIENT_END = Color("#252537")  # End of gradient for panels

