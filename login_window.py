import sqlite3
from PyQt5 import QtMultimedia
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, \
    QGridLayout
from PyQt5.QtCore import Qt, QRect, QTimer, QUrl
from PyQt5.QtGui import QIcon


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon('./res/tt.jpg'))
        self.setGeometry(1100, 300, 400, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.image_layout = QHBoxLayout()
        self.label = QLabel(
            '',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.label.setObjectName('round_image')
        self.label.setFixedSize(200, 200)
        self.image_layout.addWidget(self.label)

        heading = QLabel(
            'Welcome Back',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        heading.setObjectName('heading')

        self.subheading = QLabel(
            'Please enter your email and password to log in.',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.subheading.setObjectName('subheading')

        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Enter your email')

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText('Enter your password')

        self.btn_login = QPushButton('Login')
        self.btn_create = QPushButton('Сreate account')

        self.btn_login.clicked.connect(self.open_main_window)
        self.btn_create.clicked.connect(self.open_create_window)

        layout.addStretch(stretch=1)
        layout.addLayout(self.image_layout)
        layout.addStretch(stretch=1)
        layout.addWidget(heading)
        layout.addWidget(self.subheading)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_create)
        layout.addStretch(stretch=1)

        self.show()

    def open_main_window(self):
        self.login_ql = self.email.text()
        self.password_ql = self.password.text()

        con = sqlite3.connect('login_and_pass.db')
        cur = con.cursor()
        ans_user_in = cur.execute('''select id from logs_and_pass 
        where email = ? and pass = ?''', (self.login_ql, self.password_ql,)).fetchone()
        if ans_user_in:
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            self.subheading.setText("Sorry wrong username or password.")
        con.close()

    def open_create_window(self):
        self.hide()
        self.main_window = CreateWindow()
        self.main_window.show()


class CreateWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Create account')
        self.setWindowIcon(QIcon('./assets/lock.png'))
        self.setGeometry(1100, 300, 400, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.image_layout = QHBoxLayout()
        self.label = QLabel(
            '',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.label.setObjectName('cr_acc')
        self.label.setFixedSize(200, 200)
        self.image_layout.addWidget(self.label)

        heading = QLabel(
            'Welcome Back',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        heading.setObjectName('heading')

        subheading = QLabel(
            'Please enter your email and password to log in.',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        subheading.setObjectName('subheading')

        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Enter your email')

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText('Enter your password')

        self.btn_create = QPushButton('Create account')
        self.btn_create.clicked.connect(self.open_login_window)

        layout.addStretch(stretch=1)
        layout.addLayout(self.image_layout)
        layout.addStretch(stretch=1)
        layout.addWidget(heading)
        layout.addWidget(subheading)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(self.btn_create)
        layout.addStretch(stretch=1)

        self.show()

    def open_login_window(self):
        self.login_ql = self.email.text()
        self.password_ql = self.password.text()

        con = sqlite3.connect('login_and_pass.db')
        cur = con.cursor()
        cur.execute('''INSERT INTO logs_and_pass (email, pass) VALUES (?, ?)''', (self.login_ql, self.password_ql))
        con.commit()

        self.hide()
        self.main_window = LoginWindow()
        self.main_window.show()

        con.close()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('MainWindow')
        # self.setWindowIcon(QIcon('./assets/lock.png'))
        self.setGeometry(1100, 300, 400, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.image_layout = QHBoxLayout()
        self.label = QLabel()
        self.label.setObjectName('main_wig')
        self.label.setFixedSize(300, 300)
        self.image_layout.addWidget(self.label)
        layout.addStretch(stretch=1)
        layout.addLayout(self.image_layout)
        layout.addStretch(stretch=4)

        self.dict = {
            'D:/_Qt/EXE/Mp3/new_build/QThread_mp3/img/zvuki_prirody.mp3': []
        }
        self.song = ''

        self.player = QtMultimedia.QMediaPlayer()
        self.player.stateChanged.connect(self.playerState)

        self.qsl = QSlider(self)
        self.qsl.setFixedSize(350, 30)  # +++
        self.qsl.setOrientation(Qt.Horizontal)

        self.qsl.sliderMoved[int].connect(self.SetPlayPosition)
        self.qsl.sliderReleased.connect(self.slider_released)

        self.box = QGridLayout(self)

        for line, song in enumerate(self.dict):
            play_btn = QPushButton('Play', clicked=lambda ch, song=song: self.play(song))

            pause_btn = QPushButton('Pause', clicked=self.pause, enabled=False)

            label = QLabel(song.rsplit('/', maxsplit=1)[-1])
            self.box.addWidget(play_btn, line, 0)
            self.box.addWidget(pause_btn, line, 1)
            self.box.addWidget(label, line, 2)

            self.dict[song].append(play_btn)
            self.dict[song].append(pause_btn)

        self.box.addWidget(self.qsl, 2, 0, 1, 3)
        layout.addLayout(self.box)
        self.Play_Pause = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.PlayMode)
        self.timer.start(1000)

        self.show()

    def PlayMode(self):
        if self.Play_Pause == False:
            self.qsl.setMinimum(0)
            self.qsl.setMaximum(self.player.duration())
            self.qsl.setValue(self.qsl.value() + 1000)

    def slider_released(self):
        self.player.setPosition(self.qsl.value())

    def SetPlayPosition(self, val):
        pass

    def play(self, song):
        if self.player.isAudioAvailable() == False:
            self.player.setMedia(QtMultimedia.QMediaContent(QUrl(song)))
            self.dict[song][1].setEnabled(True)
            self.song = song

        if self.song == song:
            pass
        else:
            self.player.setMedia(QtMultimedia.QMediaContent(QUrl(song)))
            self.dict[self.song][1].setEnabled(False)
            self.dict[song][1].setEnabled(True)
            self.song = song

        self.player.play()
        self.Play_Pause = False

    def pause(self):
        self.player.pause()
        self.Play_Pause = True

    def playerState(self, state):
        if state == 0:
            self.Play_Pause = True
            self.qsl.setSliderPosition(0)


