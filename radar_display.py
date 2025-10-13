from PyQt6.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsView
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtCore import Qt

MAX_DISTANCE_M = 13
FOV_DEGREES = 90

SPACING = 50
MARGIN = 25

class RadarGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # scene configuration
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        self.scene.setSceneRect(0, 0, 1250, 700)

        # graphics view configuration
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # radar display
        self.draw_graph(SPACING)
        self.label_x_axis()
        self.label_y_axis()

        #self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


    def draw_graph(self, spacing):
        rect = self.scene.sceneRect()

        # line features
        grid_pen = QPen(Qt.GlobalColor.green)
        axis_pen = QPen(Qt.GlobalColor.green)
        grid_pen.setWidth(1)
        axis_pen.setWidth(2)

        # vertical lines
        x = rect.left() + MARGIN
        while x <= (rect.right() - MARGIN):
            pen = axis_pen if x == (rect.left() + MARGIN) else grid_pen
            self.scene.addLine(x, rect.top() + MARGIN, x, rect.bottom() - MARGIN, pen)
            x += spacing

        # horizontal lines
        y = rect.bottom() - MARGIN
        while y >= (rect.top() + MARGIN):
            pen = axis_pen if y == (rect.bottom() - MARGIN) else grid_pen
            self.scene.addLine(rect.left() + MARGIN, y, rect.right() - MARGIN, y, pen)
            y -= spacing

    def label_x_axis(self):
        font = QFont("Arial", 10)
        rect = self.scene.sceneRect()

        # label interval setup
        x_start = int(rect.left() + MARGIN)
        x_end = int(rect.right() - MARGIN)
        x_step = (x_end - x_start) / 6
        y_axis_pos = rect.bottom() - MARGIN

        x = x_start
        x_val = -FOV_DEGREES
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

            self.scene.addItem(label_item)

            x_val += 30
            x += x_step

    def label_y_axis(self):
        font = QFont("Arial", 10)
        rect = self.scene.sceneRect()

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

            self.scene.addItem(label_item)

            y_val += MAX_DISTANCE_M / 13
            y -= y_step

    def clear(self):
        self.scene.clear()
        self.draw_graph(SPACING)