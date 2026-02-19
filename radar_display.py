from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QBrush, QColor, QPainter

from graph_elements import *
from drone_node import DroneObject

DETECTED_DRONES = []

class RadarGraphicsView(QGraphicsView):
    drone_select_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        # scene configuration
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        self.scene.setSceneRect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        # graphics view configuration
        self.setScene(self.scene)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # empty radar display
        draw_graph(self)
        label_x_axis(self)
        label_y_axis(self)

    # TODO: fetch drone tracks from external source
    def display_drones(self, drones=DETECTED_DRONES):
        # Assigning custom colors per drone
        colors = [
            QColor(153, 0, 255),    # Neon Purple (Drone 0)
            QColor(248, 231, 28),   # Yellow (Drone 1)
            QColor(255, 33, 179),   # Neon Pink (Drone 2)
        ]

        # Bolding the vertical grid line where the drone is located
        self.highlight_drone_columns(drones)

        for i, drone in enumerate(drones):
            drone.color = colors[i % len(colors)]
            drone.select_signal.connect(self.update_selected_drone)
            self.scene.addItem(drone)

    def highlight_drone_columns(self, drones=DETECTED_DRONES):
        for drone in drones:
            # Converting azimuth degrees to X screen coordinate (same scaling formula)
            x = MARGIN + (drone.x + MAX_AZIMUTH_DEGREES) * (DISPLAY_WIDTH - 2 * MARGIN) / (MAX_AZIMUTH_DEGREES * 2)
            pen.setWidth(5) 
            pen = QPen(Qt.GlobalColor.green)
            self.scene.addLine(x, MARGIN, x, DISPLAY_HEIGHT - MARGIN, pen)

    def update_selected_drone(self, drone):
        data = {
            "ID": drone.id,
            "Range": drone.range_m,
            "Velocity": drone.velocity_mps,
            "Power": drone.power_db,
            "Azimuth": drone.azimuth_deg,
            "Quality": drone.quality,
        }
        self.drone_select_signal.emit(data)

    def clear(self):
        self.scene.clear()
        draw_graph(self)
        label_x_axis(self)
        label_y_axis(self)