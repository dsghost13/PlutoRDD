import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from radar_display import RadarGraphicsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PlutoRDD - GUI")
        self.showMaximized()

        self.radar_display = RadarGraphicsView()

        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        layout.addWidget(self.radar_display)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()