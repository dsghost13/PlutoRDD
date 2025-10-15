from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class DroneDataPane(QWidget):
    def __init__(self):
        super().__init__()

        fields = ['ID', 'Azimuth', 'Distance', 'Time', 'Velocity', 'Heading']
        self.values = {}

        cell_style = """
            color: #F8F8F8;
            background-color: #292929;
            border-right: 0.5px solid black;
            border-bottom: 0.5px solid black;
        """

        # white background stretching entire data pane
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#292929'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # outer layout encompassing data entries
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        self.setLayout(outer_layout)

        # inner layout with grid for data entries
        inner_layout = QGridLayout()
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setHorizontalSpacing(0)
        inner_layout.setVerticalSpacing(0)
        outer_layout.addLayout(inner_layout)

        # propagates grid with proper text
        for row, field in enumerate(fields):
            name_label = QLabel(field)
            name_label.setStyleSheet(cell_style)
            name_label.setContentsMargins(8, 4, 4, 4)
            name_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            inner_layout.addWidget(name_label, row, 0)

            value_label = QLabel("")
            value_label.setStyleSheet(cell_style)
            value_label.setContentsMargins(8, 4, 4, 4)
            value_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            inner_layout.addWidget(value_label, row, 1)
            self.values[field] = value_label

        # adds blank space below data entries
        filler = QWidget()
        filler.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        outer_layout.addWidget(filler)

    def update_values(self, data):
        units = ['', '°', ' m', ' ns', ' m/s', '°']
        for (field, value), unit in zip(data.items(), units):
            value_label = self.values.get(field)
            value_label.setText(f'{str(value)}{unit}')