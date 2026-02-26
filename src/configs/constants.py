from PyQt6.QtWidgets import QSizePolicy

# size policy
E = QSizePolicy.Policy.Expanding
F = QSizePolicy.Policy.Fixed
P = QSizePolicy.Policy.Preferred

# display constraints
MAX_DISTANCE_M = 20
MAX_AZIMUTH_DEGREES = 60

# display display
DISPLAY_WIDTH = 1250
DISPLAY_HEIGHT = 700
MARGIN = 25
SPACING = 50

# drone node
CIRCLE_RADIUS = 10
ARROW_LENGTH_SF = 25    # px per m/s
ARROW_HEAD_SIZE = 20