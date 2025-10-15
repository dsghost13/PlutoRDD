from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QBrush, QColor, QPainter

from graph_elements import *
from drone_node import DroneItem

class RadarGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # scene configuration
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        self.scene.setSceneRect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        # graphics view configuration
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # empty radar display
        draw_graph(self)
        label_x_axis(self)
        label_y_axis(self)

        # test drone
        drone = DroneItem(id=0, x=0, y=10, t=0, v=4, heading=210)
        self.scene.addItem(drone)

    def clear(self):
        self.scene.clear()
        draw_graph(self)
        label_x_axis(self)
        label_y_axis(self)