#!/usr/bin/env python3

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QVBoxLayout,
    QGraphicsBlurEffect, QLabel, QHBoxLayout 
)
from PyQt6.QtCore import Qt, QTimer, QSize, QThreadPool, QRunnable, pyqtSignal, QObject, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QMovie

import sys, datetime, pwd, os, subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class WorkerSignals(QObject):
    finished = pyqtSignal(bool)


class AuthWorker(QRunnable):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.signals = WorkerSignals()

    def run(self):
        import pam
        user = pam.pam()
        result = user.authenticate(self.username, self.password)
        self.signals.finished.emit(result)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        subprocess.run("/usr/local/bin/kill-splash-screen.sh")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGeometry(0, 0, 1920, 1080)

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

        self.threadpool = QThreadPool.globalInstance()

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
        password.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)        
        self.get_username()

        self.loginSpinner = QMovie(os.path.join(SCRIPT_DIR, "loading-loading-forever.gif"))
        self.loginMover = QLabel(self)
        self.loginMover.setMovie(self.loginSpinner)
        self.loginMover.setVisible(False)
        self.loginSpinner.setScaledSize(QSize(15, 15))

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

        self.loginMover.setParent(self)
        self.loginMover.move(1055, 815)
        self.loginMover.show()


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
        if not password:
            return

        self.loginSpinner.start()
        self.loginMover.setVisible(True)
        self.loginMover.setFixedSize(15, 15)


        worker = AuthWorker(self.user_name, password)
        worker.signals.finished.connect(self.on_auth_finished)
        self.threadpool.start(worker)

    def on_auth_finished(self, isTrue):
        if isTrue:
            self.close()
            subprocess.run(["/usr/local/bin/switch-user.sh", self.user_name])
            sys.exit(0)
        else:
            self.loginSpinner.stop()
            self.loginMover.setVisible(False)
            self.run_animation()

    def run_animation(self):
        animation = QPropertyAnimation(self.user_password, b"pos")
        animation.setDuration(350)
        animation.setLoopCount(1)

        original_pos = self.user_password.pos()

        animation.setKeyValueAt(0, original_pos)
        animation.setKeyValueAt(0.1, original_pos + QPoint(-10, 0))
        animation.setKeyValueAt(0.2, original_pos + QPoint(10, 0))
        animation.setKeyValueAt(0.3, original_pos + QPoint(-10, 0))
        animation.setKeyValueAt(0.4, original_pos + QPoint(10, 0))
        animation.setKeyValueAt(0.5, original_pos + QPoint(-5, 0))
        animation.setKeyValueAt(0.6, original_pos + QPoint(5, 0))
        animation.setKeyValueAt(0.7, original_pos + QPoint(-2, 0))
        animation.setKeyValueAt(0.8, original_pos + QPoint(2, 0))
        animation.setKeyValueAt(0.9, original_pos)
        animation.setKeyValueAt(1, original_pos)

        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        
        # Prevent garbage collection
        self.shake_animation = animation

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

    window = LoginWindow()
    window.showFullScreen()

    app.exec()
