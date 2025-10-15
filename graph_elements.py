from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QPen
from PyQt6.QtCore import Qt

from constants import *

def draw_graph(view, spacing=SPACING):
    rect = view.scene.sceneRect()

    # line features
    grid_pen = QPen(Qt.GlobalColor.green)
    axis_pen = QPen(Qt.GlobalColor.green)
    grid_pen.setWidth(1)
    axis_pen.setWidth(2)

    # vertical lines
    x = rect.left() + MARGIN
    while x <= (rect.right() - MARGIN):
        pen = axis_pen if x == (rect.left() + MARGIN) else grid_pen
        view.scene.addLine(x, rect.top() + MARGIN, x, rect.bottom() - MARGIN, pen)
        x += spacing

    # horizontal lines
    y = rect.bottom() - MARGIN
    while y >= (rect.top() + MARGIN):
        pen = axis_pen if y == (rect.bottom() - MARGIN) else grid_pen
        view.scene.addLine(rect.left() + MARGIN, y, rect.right() - MARGIN, y, pen)
        y -= spacing


def label_x_axis(view):
    font = QFont("Arial", 10, QFont.Weight.Bold)
    rect = view.scene.sceneRect()

    # label interval setup
    x_start = int(rect.left() + MARGIN)
    x_end = int(rect.right() - MARGIN)
    x_step = (x_end - x_start) / 4
    y_axis_pos = rect.bottom() - MARGIN

    x = x_start
    x_val = -MAX_AZIMUTH_DEGREES
    while x <= x_end:
        # label text
        label_sign = "+" if x_val > 0 else ""
        label_text = f"{label_sign}{x_val}°"

        # label features
        label_item = QGraphicsTextItem(label_text)
        label_item.setFont(font)
        label_item.setDefaultTextColor(Qt.GlobalColor.green)

        # label position
        text_rect = label_item.boundingRect()
        label_item.setPos(x - text_rect.width() / 2, y_axis_pos + 5)

        view.scene.addItem(label_item)

        x_val += 30
        x += x_step


def label_y_axis(view):
    font = QFont("Arial", 10)
    rect = view.scene.sceneRect()

    # label interval setup
    y_start = int(rect.bottom() - MARGIN)
    y_end = int(rect.top() + MARGIN)
    y_step = (y_start - y_end) / 13
    x_axis_pos = rect.left() + MARGIN

    y = y_start
    y_val = 0
    while y >= y_end:
        # label text
        label_text = f"{int(y_val)}m"

        # label features
        label_item = QGraphicsTextItem(label_text)
        label_item.setFont(font)
        label_item.setDefaultTextColor(Qt.GlobalColor.green)

        # label position
        text_rect = label_item.boundingRect()
        label_item.setPos(x_axis_pos - text_rect.width() - 3, y - text_rect.height() / 2)

        view.scene.addItem(label_item)

        y_val += MAX_DISTANCE_M / 13
        y -= y_step