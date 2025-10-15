import math

from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSignal

from constants import *

class DroneObject(QGraphicsObject):
    select_signal = pyqtSignal(object)

    def __init__(self, id, x, y, t, v, heading, parent=None):
        super().__init__(parent)

        # drone features
        self.id = id
        self.x = x
        self.y = y
        self.t = t
        self.v = v
        self.heading = heading

        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable, True)
        self.set_display_coordinates()

    def set_display_coordinates(self):
        def scale_x(x):
            return (MARGIN + (self.x + MAX_AZIMUTH_DEGREES) *
                    (DISPLAY_WIDTH - 2 * MARGIN) / (MAX_AZIMUTH_DEGREES * 2))

        def scale_y(y):
            return ((DISPLAY_HEIGHT - MARGIN) - self.y *
                    (DISPLAY_HEIGHT - 2 * MARGIN) / MAX_DISTANCE_M)

        x_scaled = scale_x(self.x)
        y_scaled = scale_y(self.y)
        self.setPos(x_scaled, y_scaled)

    def boundingRect(self) -> QRectF:
        arrow_length = self.v * ARROW_LENGTH_SF
        return QRectF(-arrow_length, -arrow_length, arrow_length * 2, arrow_length * 2)

    def paint(self, painter, option, widget=None):
        # green circle marker
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.setPen(QPen(QColor(0, 255, 0), 3))
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