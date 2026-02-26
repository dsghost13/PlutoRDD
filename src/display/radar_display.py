from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen

from src.display.graph_elements import *
from src.display.drone_node import DroneObject

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

        # empty display display
        # initial draw
        self.refresh()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Make scene match the visible viewport size (autofit)
        w = max(1, self.viewport().width())
        h = max(1, self.viewport().height())
        self.scene.setSceneRect(0, 0, w, h)

        self.refresh()

    def refresh(self, drones=None):
        if drones is None:
            drones = DETECTED_DRONES

        # Remove items without deleting the underlying Python objects
        for item in list(self.scene.items()):
            self.scene.removeItem(item)

        draw_graph(self)
        label_x_axis(self)
        label_y_axis(self)

        self.display_drones(drones)

    # TODO: fetch drone tracks from external source
    def display_drones(self, drones=DETECTED_DRONES):
        # Assigning custom colors per drone
        colors = [
            QColor(153, 0, 255),    # Neon Purple (Drone 0)
            QColor(248, 231, 28),   # Yellow (Drone 1)
            QColor(255, 33, 179),   # Neon Pink (Drone 2)
        ]

        # Recompute drone positions using the current scene size (autofit)
        rect = self.scene.sceneRect()
        for drone in drones:
            if hasattr(drone, "set_display_coordinates"):
                try:
                    drone.set_display_coordinates(rect)  # if drone_node.py supports scene_rect
                except TypeError:
                    drone.set_display_coordinates()  # fallback if signature is old

        # Bolding the vertical grid line where the drone is located
        self.highlight_drone_columns(drones)

        for i, drone in enumerate(drones):
            drone.color = colors[i % len(colors)]
            if not getattr(drone, "_select_connected", False):
                drone.select_signal.connect(self.update_selected_drone)
                drone._select_connected = True

            self.scene.addItem(drone)

    def highlight_drone_columns(self, drones=DETECTED_DRONES):
        rect = self.scene.sceneRect()
        w = rect.width()
        h = rect.height()

        pen = QPen(Qt.GlobalColor.green)
        pen.setWidth(5)

        for drone in drones:
            # use CURRENT scene width, not DISPLAY_WIDTH
            x = MARGIN + (drone.x + MAX_AZIMUTH_DEGREES) * (w - 2 * MARGIN) / (MAX_AZIMUTH_DEGREES * 2)
            self.scene.addLine(x, MARGIN, x, h - MARGIN, pen)

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
        self.refresh([])