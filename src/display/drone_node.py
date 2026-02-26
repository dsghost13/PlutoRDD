import math

from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSignal

from src.configs.constants import *

def _as_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

class DroneObject(QGraphicsObject):
    select_signal = pyqtSignal(object)

    def __init__(self, drone_data, scene_rect=None, parent=None):
        """
        id      : int
        range_m       : float
        velocity_mps  : float 
        power_db      : float
        azimuth_deg   : float
        quality       : float
        """
        super().__init__(parent)
        self.id = drone_data.get("id", "")

        self.range_m = _as_float(drone_data.get("range_m", 0.0))
        self.velocity_mps = _as_float(drone_data.get("velocity_mps", 0.0))  # signage defined consistently by us
        self.power_db = _as_float(drone_data.get("power_db", 0.0))
        self.azimuth_deg = _as_float(drone_data.get("azimuth_deg", 0.0))
        self.quality = _as_float(drone_data.get("quality", 0.0))  # [0, 1]

        # --- fields used by set_display_coordinates() and paint() ---
        self.x = self.azimuth_deg  # x axis = azimuth (deg)
        self.y = self.range_m  # y axis = range (m)
        self.v = abs(self.velocity_mps)  # arrow length uses speed magnitude
        self.heading = self.azimuth_deg + (180.0 if self.velocity_mps < 0 else 0.0)

        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable, True)
        self.set_display_coordinates(scene_rect)

    def set_display_coordinates(self, scene_rect=None):
        # Use actual scene size if provided; otherwise fall back to constants
        if scene_rect is None:
            w = DISPLAY_WIDTH
            h = DISPLAY_HEIGHT
        else:
            w = scene_rect.width()
            h = scene_rect.height()

        def scale_x(x):
            return (MARGIN + (x + MAX_AZIMUTH_DEGREES) *
                    (w - 2 * MARGIN) / (MAX_AZIMUTH_DEGREES * 2))

        def scale_y(y):
            return ((h - MARGIN) - y *
                    (h - 2 * MARGIN) / MAX_DISTANCE_M)

        self.setPos(scale_x(self.x), scale_y(self.y))

    def boundingRect(self) -> QRectF:
        arrow_length = max(1.0, self.v * ARROW_LENGTH_SF)
        return QRectF(-arrow_length, -arrow_length, arrow_length * 2, arrow_length * 2)

    def paint(self, painter, option, widget=None):
        # Dynamic per-drone color (fallback to purple if none is assigned)
        color = getattr(self, 'color', QColor(153, 0, 255))
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color, 3))
        painter.drawEllipse(QPointF(0, 0), CIRCLE_RADIUS, CIRCLE_RADIUS)

        # arrow shaft pointing in direction of motion
        arrow_length = self.v * ARROW_LENGTH_SF
        angle_rad = math.radians((self.heading + 270) % 360)

        x_end = arrow_length * math.cos(angle_rad)
        y_end = arrow_length * math.sin(angle_rad)
        end_point = QPointF(x_end, y_end)

        painter.drawLine(QPointF(0, 0), end_point)

        # arrow head
        left_angle = angle_rad + math.radians(150)
        right_angle = angle_rad - math.radians(150)

        left_point = QPointF(
            x_end + ARROW_HEAD_SIZE * math.cos(left_angle),
            y_end + ARROW_HEAD_SIZE * math.sin(left_angle)
        )
        right_point = QPointF(
            x_end + ARROW_HEAD_SIZE * math.cos(right_angle),
            y_end + ARROW_HEAD_SIZE * math.sin(right_angle)
        )

        arrow_head = QPolygonF([end_point, left_point, right_point])
        painter.drawPolygon(arrow_head)

        # white square highlight
        if self.isSelected():
            side = CIRCLE_RADIUS * 3

            corners = [
                QPointF(-side/2, -side/2),
                QPointF(side/2, -side/2),
                QPointF(side/2, side/2),
                QPointF(-side/2, side/2)
            ]

            square = QPolygonF(corners)

            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
            painter.drawPolygon(square)

    def itemChange(self, change, value):
        if change == QGraphicsObject.GraphicsItemChange.ItemSelectedHasChanged and value:
            self.select_signal.emit(self)
        return super().itemChange(change, value)