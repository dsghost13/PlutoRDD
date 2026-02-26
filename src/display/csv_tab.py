import os
import csv
from collections import deque

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView
)


class _CsvTable(QWidget):
    def __init__(self, csv_path, title, parent=None):
        super().__init__(parent)
        self.csv_path = csv_path
        self.title = title
        self._last_mtime = None

        # --- top bar ---
        top = QHBoxLayout()
        self.title_label = QLabel(f"{self.title}: {self.csv_path}")
        self.title_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(10, 5000)
        self.rows_spin.setValue(200)

        self.reload_btn = QPushButton("Reload")
        self.reload_btn.clicked.connect(self.reload_now)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        top.addWidget(self.title_label)
        top.addStretch(1)
        top.addWidget(QLabel("Rows:"))
        top.addWidget(self.rows_spin)
        top.addWidget(self.reload_btn)
        top.addWidget(self.status)

        # --- table ---
        self.table = QTableWidget()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # refresh timer (checks file changes)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._maybe_reload)
        self.timer.start(500)

        self.reload_now()

    def _maybe_reload(self):
        if not os.path.exists(self.csv_path):
            self.status.setText("waiting for file...")
            return

        mtime = os.path.getmtime(self.csv_path)
        if self._last_mtime != mtime:
            self.reload_now()

    def reload_now(self):
        if not os.path.exists(self.csv_path):
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.status.setText("waiting for file...")
            return

        self._last_mtime = os.path.getmtime(self.csv_path)

        max_rows = int(self.rows_spin.value())

        with open(self.csv_path, "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            rows = deque(reader, maxlen=max_rows)

        # build table
        self.table.clear()
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(val))

        self.status.setText(f"{len(rows)} rows")


class CsvDataTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        frames_path = os.path.join("logs", "frames.csv")
        det_path = os.path.join("logs", "detections.csv")

        tabs = QTabWidget()
        tabs.addTab(_CsvTable(frames_path, "frames.csv"), "Frames")
        tabs.addTab(_CsvTable(det_path, "detections.csv"), "Detections")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)