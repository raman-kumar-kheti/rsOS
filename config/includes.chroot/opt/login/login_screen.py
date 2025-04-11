#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QGraphicsBlurEffect, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor
import sys, datetime, pam, pwd, os
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGeometry(0, 0, 1920, 1080)  # Adjust window size

        self.background_widget = QWidget(self)
        self.background_widget.setGeometry(self.rect())

        backgroundEffect = QGraphicsBlurEffect()
        backgroundEffect.setBlurRadius(15)
        self.background_widget.setGraphicsEffect(backgroundEffect)

        self.background_widget.setStyleSheet(f"""
            background-repeat: no-repeat;
            background-position: center;
            background-image: url({os.path.join(SCRIPT_DIR, "login_screen2.jpg")});
        """)

        self.main_layout = QVBoxLayout(self)

        self.top_layout = QVBoxLayout()
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.currentTime = QLabel(self)
        self.update_time()
        self.currentTime.setStyleSheet("""
            QLabel {
                padding: 5px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 150px;
                font-family: Arial, sans-serif;
                border-width: 2px;
                margin-top: 40px;
            }
        """)
        self.full_name = QLabel()
        self.user_name = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.top_layout.addWidget(self.currentTime)
        self.main_layout.addLayout(self.top_layout)

        self.setup_profile_picture()

        self.setup_user_inputs()

    def update_time(self):
        self.currentTime.setText(datetime.datetime.now().strftime("%I:%M"))

    def setup_profile_picture(self):
        profilePicture = QVBoxLayout()
        profile_picture = QLabel(self)

        pixmap = QPixmap(os.path.join(SCRIPT_DIR, "profile_pictures.png"))
        scaled_pixmap = pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio)

        rounded_pixmap = QPixmap(180, 180)
        rounded_pixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(scaled_pixmap))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 180, 180)
        painter.end()

        profile_picture.setFixedSize(180, 180)
        profile_picture.setPixmap(rounded_pixmap)

        profilePicture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profilePicture.addWidget(profile_picture)

        self.main_layout.addLayout(profilePicture)

    def setup_user_inputs(self):

        user_name_label = QHBoxLayout()
        user_name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        password = QHBoxLayout()
        password.setAlignment(Qt.AlignmentFlag.AlignHCenter |Qt.AlignmentFlag.AlignTop)

        self.get_username()

        self.user_password = QLineEdit(self)
        self.user_password.setPlaceholderText("Enter Password")
        self.user_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.user_password.setFixedSize(170, 30)
        self.user_password.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.6);
                border-radius: 15px;
                color: #333;
                font-size: 14px;
                border-width:0.5px;
                border-color:#545454;
                border-style:solid;
                padding-left:10px;
            }
        """)

        self.user_password.returnPressed.connect(self.get_input)

        user_name_label.addWidget(self.full_name)
        password.addWidget(self.user_password)


        self.main_layout.addLayout(user_name_label)
        self.main_layout.addLayout(password)


    def get_username(self):
            username = self.get_human_users_mac()
            self.user_name = username[1]['username']
            self.full_name.setText(username[1]['fullname'])
            self.full_name.setStyleSheet("""
            QLabel {
                padding: 5px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 20px;
                font-family: Arial, sans-serif;
                border-width: 2px;
            }
        """)

    def get_input(self):
        password = self.user_password.text()
        user = pam.pam()

        if password:
            if user.authenticate(self.user_name, password):
                self.close()
                sys.exit(0)
            else:
                print("Unable to login")
                self.run_animation()

    def run_animation(self):
        original_style = self.user_password.styleSheet()
        
        self.user_password.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.6);
                border-radius: 15px;
                color: #333;
                border-width:1px;
                border-color:#545454;
                border-style:solid;
                font-size: 16px;
                margin-left:0px;
                padding-left:10px;

            }
        """)
        
        shake_count = 0
        max_shakes = 4
        
        def shake():
            nonlocal shake_count
            if shake_count >= max_shakes:
                self.user_password.setStyleSheet(original_style)
                return
                
            if shake_count % 2 == 0:
                self.user_password.setStyleSheet("""
                    QLineEdit {
                        background-color: rgba(255, 255, 255, 0.5);
                        border-radius: 15px;
                        color: #333;
                        font-size: 16px;
                        margin-left:10px;
                        margin-right: 0px;
                        border-width:1px;
                        border-color:#545454;
                        border-style:solid;
                        padding-left:10px;
                    }
                """)
            else:
                self.user_password.setStyleSheet("""
                    QLineEdit {
                        background-color: rgba(255, 255, 255, 0.6);
                        border-radius: 15px;
                        color: #333;
                        font-size: 16px;
                        margin-left:0px;
                        margin-right:10px;
                        border-width:1px;
                        border-color:#545454;
                        border-style:solid;
                        padding-left:10px;
                    }
                """)
            
            shake_count += 1
            QTimer.singleShot(110, shake)
        shake()


    def get_human_users_mac(self):
        users = []
        for user in pwd.getpwall():
            if user.pw_uid >= 1000:
                users.append({
                    'username': user.pw_name,
                    'fullname': user.pw_gecos.split(',')[0] or user.pw_name
                })
        return users

if __name__ == "__main__":
    app = QApplication([])

    # Create and display the login window
    window = LoginWindow()
    window.showFullScreen()

    app.exec()