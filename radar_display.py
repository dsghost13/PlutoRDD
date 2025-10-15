from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QBrush, QColor, QPainter

from graph_elements import *
from drone_node import DroneObject

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
    def display_drones(self, drones=None):
        # test drones
        drones = [
            DroneObject(id=0, x=0, y=10, t=0, v=4, heading=210),
            DroneObject(id=1, x=-30, y=15, t=0, v=2, heading=60),
            DroneObject(id=2, x=30, y=5, t=0, v=6, heading=300),
        ]

        for drone in drones:
            drone.select_signal.connect(self.update_selected_drone)
            self.scene.addItem(drone)

    def update_selected_drone(self, drone):
        data = {
            "ID": drone.id,
            "Azimuth": drone.x,
            "Distance": drone.y,
            "Time": drone.t,
            "Velocity": drone.v,
            "Heading": drone.heading,
        }
        self.drone_select_signal.emit(data)

    def clear(self):
        self.scene.clear()
        draw_graph(self)
        label_x_axis(self)
        label_y_axis(self)