import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget

from radar_display import RadarGraphicsView
from data_pane import DroneDataPane

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window container setup
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # main window widgets
        self.radar_display = RadarGraphicsView()
        self.drone_data_pane = DroneDataPane()
        layout.addWidget(self.radar_display, stretch=4)
        layout.addWidget(self.drone_data_pane, stretch=1)

        # event connections
        self.radar_display.drone_select_signal.connect(self.drone_data_pane.update_values)

        self.setWindowTitle("PlutoRDD - GUI")
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()