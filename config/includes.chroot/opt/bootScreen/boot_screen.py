#!/usr/bin/env python3

from PyQt6.QtWidgets import (QWidget, QApplication, QVBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMovie, QPixmap, QIcon
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint)
        self.setStyleSheet("background: black;")
        self.setGeometry(0, 0, 1920, 1080)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        bottomBtn = QPushButton(
            text="Bottom",
            parent=self
        )
        bottomBtn.clicked.connect(self.closeSplashScreen)

        self.os_logo = QLabel()
        self.os_logo.setPixmap(QPixmap(os.path.join(SCRIPT_DIR,"os_logo.png")).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.os_logo.setFixedSize(200, 200)
        self.os_logo.setScaledContents(True)

        self.spinner_mover = QMovie(os.path.join(SCRIPT_DIR, "initial_spinner.gif"))
        self.spinner_mover.start()
        self.spinner_mover.setScaledSize(QSize(25, 25))

        self.spinner_holder = QLabel(self)
        self.spinner_holder.setMovie(self.spinner_mover)
        self.spinner_holder.setVisible(True)
        self.spinner_holder.setFixedSize(25, 25)

        self.bottom_heading = QLabel()
        self.bottom_heading.setStyleSheet("""
            QLabel{
                font-size:40px;
                margin-bottom:100px;
                margin-top:20px;
                font-family: "Times New Roman", Times, serif;
                color:white;
            }
        """)
        self.bottom_heading.setText("Fllamingo.")

        middle_container = QVBoxLayout()
        middle_container.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        middle_container.setSpacing(180)
        middle_container.addWidget(bottomBtn)
        middle_container.addWidget(self.os_logo)
        middle_container.addWidget(self.spinner_holder, alignment=Qt.AlignmentFlag.AlignHCenter)


        self.main_layout.addLayout(middle_container)
        self.main_layout.addWidget(self.bottom_heading)

    def closeSplashScreen(self):
            print("Is This method called")
            self.close()
            sys.exit(0)
if __name__ == "__main__":
    splash_screen = QApplication([])

    splash_screen_View = SplashScreen()
    splash_screen_View.showFullScreen()

    splash_screen.exec()