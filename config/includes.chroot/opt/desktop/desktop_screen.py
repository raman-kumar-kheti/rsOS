#!/usr/bin/env python3

from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGraphicsBlurEffect,
    QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QSlider
)
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QFont, QPixmap, QIcon, QMouseEvent
from PyQt6.QtCore import Qt, QTimer, QSize
import sys, os, datetime, subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class DesktopRoot:
    def __init__(self):
        self.bottomArea = BottomDock()
        self.bottomArea.setGeometry(0, 1003, 0, 0)
        self.bottomArea.show()

        self.ToAreaSectionSection = ToAreaSection()
        self.ToAreaSectionSection.show()



class ButtonDock(QPushButton):
    def __init__(self, id, icons, parent=None):
        super().__init__(parent)
        self.id = id
        self.setIcon(QIcon(os.path.join(SCRIPT_DIR, icons)))
        self.setStyleSheet("background: transparent; border: none;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"Button {self.id}: Left click")
            if self.id == 1:
                self.showPowerOption = PowerController()
                self.showPowerOption.show()
            if self.id == 3:
                    self.openController = ControlPopup()
                    self.openController.show()
        elif event.button() == Qt.MouseButton.RightButton:
            print(f"Button {self.id}: Right click")
        super().mousePressEvent(event)

class BottomDock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(650, 75)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_X11NetWmWindowTypeDock)

        middle_container = QHBoxLayout()

        icon_paths = [
            "power_off.png",
            "wifi.png",
            "controller.png",
            "folders.png",
            "chrome.png",
            "trash.png"
        ]

        for i, icon in enumerate(icon_paths, start=1):
            button = ButtonDock(i, icon, self)
            button.resize(60, 60)
            if i == 1:
                button.move(10, 28)
                button.resize(50, 50)
                button.setIconSize(QSize(30, 58))
            elif i == 2:
                button.move(65, 28)
                button.resize(50, 50)
                button.setIconSize(QSize(50, 90))
            elif i == 3:
                button.move(120, 30)
                button.resize(50, 50)
                button.setIconSize(QSize(20, 35))
            elif i == 4:
                button.move(320, 10)
                button.setIconSize(QSize(48, 58))
            elif i == 5:
                button.move(390, 10)
                button.setIconSize(QSize(38, 58))
            elif i == 6:
                button.move(450, 10)
                button.setIconSize(QSize(35, 58))
                            
        vline = QFrame(self)
        vline.setFrameShape(QFrame.Shape.VLine)
        vline.setFrameShadow(QFrame.Shadow.Sunken)
        vline.setStyleSheet("""
            QFrame {
                border-left: 2px solid rgba(255, 255, 255, 50);
                background: transparent;
            }
        """)
        vline.move(264, 38)

        self.setLayout(middle_container)

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
            Qt.WindowType.WindowStaysOnTopHint
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

class ControlPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint
                        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(50, 820, 220, 100)

        self.layout = QVBoxLayout()

        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(88)
        # self.brightness_slider.setValue(self.get_current_brightness())
        # self.brightness_slider.valueChanged.connect(self.on_brightness_changed)

        self.brightness_label = QLabel(f"Brightness: {self.brightness_slider.value()}%")

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(35)
        # self.volume_slider.valueChanged.connect(self.on_volume_changed)

        self.volume_label = QLabel(f"Volume: {self.volume_slider.value()}%")

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        self.layout.addWidget(self.brightness_label)
        self.layout.addWidget(self.brightness_slider)
        self.layout.addWidget(self.volume_label)
        self.layout.addWidget(self.volume_slider)

        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = 17

        bg_color = QColor(0, 0, 0, 200)
        painter.setBrush(bg_color)

        border_color = QColor(0, 0, 0, 80)
        pen = painter.pen()
        pen.setColor(border_color)
        pen.setWidthF(0.2)
        painter.setPen(pen)

        painter.drawRoundedRect(rect, radius, radius)


class PowerController(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(50, 820, 220, 100)

        self.layout = QVBoxLayout()

        self.shutdown_button = QPushButton("Shutdown")
        self.shutdown_button.clicked.connect(self.initiate_shutdown)
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self.initiate_restart)
        self.sleep_button = QPushButton("Sleep")
        self.sleep_button.clicked.connect(self.initiate_sleep)

        for btn in (self.shutdown_button, self.restart_button, self.sleep_button):
            btn.setFixedWidth(80)
            self.layout.addWidget(btn)

        self.footer_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_action)
        self.cancel_button.setFixedWidth(60)

        self.timer_label = QLabel("15s")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("color: white;")
        self.timer_label.setFixedWidth(40)

        self.footer_layout.addWidget(self.cancel_button)
        self.footer_layout.addWidget(self.timer_label)

        self.footer_container = QWidget()
        self.footer_container.setLayout(self.footer_layout)
        self.layout.addWidget(self.footer_container)

        self.footer_container.hide()

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.time_remaining = 15
        self.action_to_perform = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = 12
        painter.setBrush(QColor(0, 0, 0, 200))
        pen = painter.pen()
        pen.setColor(QColor(0, 0, 0, 80))
        pen.setWidthF(0.2)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, radius, radius)

    def initiate_shutdown(self):
        self.initiate_action("shutdown")

    def initiate_restart(self):
        self.initiate_action("restart")

    def initiate_sleep(self):
        self.initiate_action("sleep")

    def initiate_action(self, action):
        self.action_to_perform = action
        self.time_remaining = 15
        self.timer_label.setText(f"{self.time_remaining}s")
        self.footer_container.show()
        self.timer.start(1000)

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.setText(f"{self.time_remaining}s")
        if self.time_remaining <= 0:
            self.timer.stop()
            if self.action_to_perform == "shutdown":
                self.shutdown()
            elif self.action_to_perform == "restart":
                self.restart()
            elif self.action_to_perform == "sleep":
                self.sleep()
            self.close()

    def cancel_action(self):
        self.timer.stop()
        self.close()

    def shutdown(self):
        print("Shut down")
        # subprocess.run(["shutdown", "-h", "now"])

    def restart(self):
        print("Restart")
        # subprocess.run(["reboot"])

    def sleep(self):
        print("sleep")
        # subprocess.run(["systemctl", "suspend"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = DesktopRoot()
    sys.exit(app.exec())
