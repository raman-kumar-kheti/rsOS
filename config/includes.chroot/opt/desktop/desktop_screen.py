#!/usr/bin/env python3

from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGraphicsBlurEffect,
    QVBoxLayout
)
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QFont
from PyQt6.QtCore import Qt, QTimer
import sys, os, datetime

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class DesktopRoot:
    def __init__(self):
        self.bottomArea = BottomDock()
        self.bottomArea.setGeometry(0, 1003, 0, 0)
        self.bottomArea.show()

        self.ToAreaSectionSection = ToAreaSection()
        self.ToAreaSectionSection.show()


class BottomDock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(650, 75)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnBottomHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.corner_radius = 30
        self.slant_length = 60
        self.slant_drop = 30
        self.bg_color = QColor(2, 3, 3, 130)

        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(1.5)
        self.setGraphicsEffect(blur_effect)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        r = self.corner_radius
        slant_x = w / 2 - self.slant_length
        slant_y = self.slant_drop

        path = QPainterPath()
        path.moveTo(w / 2, 0)
        path.lineTo(slant_x, slant_y)
        path.quadTo(0, slant_y, 0, slant_y)
        path.lineTo(0, h - r)
        path.quadTo(0, h, r, h)
        path.lineTo(w - r, h)
        path.quadTo(w, h, w, h - r)
        path.lineTo(w, r)
        path.quadTo(w, 0, w - r, 0)
        path.closeSubpath()

        pen = painter.pen()
        pen.setColor(QColor(255, 255, 255, 80))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(self.bg_color)
        painter.drawPath(path)


class ToAreaSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        widget_width = 350

        x = int((screen_width - widget_width) / 2)
        y = 10

        self.setGeometry(x, -10, widget_width, 35)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnBottomHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.dateTimeLabel = QLabel()
        self.dateTimeLabel.setFont(QFont("San Francisco", 11))
        self.update_time()
        self.dateTimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dateTimeLabel.setFixedSize(350, 20)
        self.dateTimeLabel.setStyleSheet("""
            background-color: none;
            border: none;
            font-size:13px;
            color: white;
        """)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 7, 0, 0)
        layout.addWidget(self.dateTimeLabel)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = 17

        bg_color = QColor(0, 0, 0, 30)
        painter.setBrush(bg_color)

        border_color = QColor(0, 0, 0, 80)
        pen = painter.pen()
        pen.setColor(border_color)
        pen.setWidthF(0.2)
        painter.setPen(pen)

        painter.drawRoundedRect(rect, radius, radius)

    def update_time(self):
        self.dateTimeLabel.setText(datetime.datetime.now().strftime("%a %b %d  %I:%M %p"))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = DesktopRoot()
    sys.exit(app.exec())
