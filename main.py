import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QTabWidget

from src.configs.constants import E
from src.display.radar_display import RadarGraphicsView
from src.display.data_pane import DroneDataPane


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self._get_tab_widget())

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.setWindowTitle("PlutoRDD")
        self.showMaximized()


    def _get_tab_widget(self):
        tabs = QTabWidget()
        tabs.setLayout(QVBoxLayout())
        tabs.setMovable(True)
        tabs.setSizePolicy(E, E)
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        tabs.addTab(self._get_display_widget(), "Radar Display")
        return tabs

    def _get_display_widget(self):
        self.radar_display = RadarGraphicsView()
        self.drone_data_pane = DroneDataPane()
        self.radar_display.drone_select_signal.connect(self.drone_data_pane.update_values)

        display_layout = QHBoxLayout()
        display_layout.addWidget(self.radar_display, stretch=4)
        display_layout.addWidget(self.drone_data_pane, stretch=1)

        display_widget = QWidget()
        display_widget.setLayout(display_layout)
        return display_widget


def main():
    app = QApplication(sys.argv)
    # app.setPalette(qdarktheme.load_palette(theme="dark"))

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()