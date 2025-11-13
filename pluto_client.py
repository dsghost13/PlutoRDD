import socket
import numpy as np
import threading
import sys
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg

SERVER_IP = ''
PORT = 12345
BUFFER_SIZE = 4096

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

class IQViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PlutoSDR IQ Viewer")

        # PyQtGraph Widget
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.graph_widget)

        self.plot = self.graph_widget.addPlot(title="IQ Magnitude")
        self.curve = self.plot.plot(pen='y')

        # Timer to control UI update rate
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # refresh every 50 ms

        self.latest_iq = np.zeros(1024, dtype=np.complex64)

    def update_plot(self):
        """Refresh the GUI with the latest IQ data."""
        self.curve.setData(np.abs(self.latest_iq))

    def set_iq_data(self, iq_data):
        """Update IQ data safely from another thread."""
        self.latest_iq = iq_data


# === DATA RECEIVING THREAD ===
def receive_iq(viewer):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            iq_samples = np.frombuffer(data, dtype=np.complex64)
            viewer.set_iq_data(iq_samples)
        except Exception as e:
            print(f"Connection error: {e}")
            break


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    viewer = IQViewer()
    viewer.show()

    thread = threading.Thread(target=receive_iq, args=(viewer,), daemon=True)
    thread.start()

    sys.exit(app.exec())
