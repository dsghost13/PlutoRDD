import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from radar_display import RadarGraphicsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PlutoRDD - GUI")
        self.showMaximized()

        # main window container setup
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # main window widgets
        self.radar_display = RadarGraphicsView()
        layout.addWidget(self.radar_display)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()