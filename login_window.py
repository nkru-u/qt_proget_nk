import sqlite3, pygame, csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, \
    QGridLayout
from PyQt5.QtCore import Qt, QRect, QTimer, QUrl, QTime
from PyQt5.QtGui import QIcon


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon('./res/rt.png'))
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
            with open('file.csv', 'a', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerow(self.login_ql + ' вошел в систему.')

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
        self.setWindowIcon(QIcon('./res/rt.png'))
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MainWindow')
        self.setWindowIcon(QIcon('./res/rt.png'))
        self.setGeometry(1100, 300, 400, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)
        box = QHBoxLayout()
        self.subheading = QLabel(
            '',
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.subheading.setObjectName('sub')

        pygame.mixer.init()
        self.playing = False
        self.last_url = None

        self.music_list = ['./res/O★Z - Zankoku Shangri-La.mp3', './res/BRADIO-Flyers.mp3',
                           './res/milet — Anytime Anywhere .mp3', './res/Перемотка-Встречная.mp3',
                           './res/Смешарики - Ветер, ветер.mp3']
        self.current_music_index = 0

        self.play = QPushButton('▶')
        self.backward = QPushButton('<')
        self.forward = QPushButton('>')

        self.play.clicked.connect(self.playbutton)
        self.backward.clicked.connect(self.backwardbutton)
        self.forward.clicked.connect(self.forwardbutton)

        self.lcdtimer = QTimer()
        self.lcdtimer.timeout.connect(self.lcd_timer)
        self.time_counter = 0

        self.image_layout = QHBoxLayout()
        self.label = QLabel()
        self.label.setObjectName('main_wig')
        self.label.setFixedSize(300, 300)
        self.image_layout.addWidget(self.label)

        layout.addStretch(stretch=2)
        layout.addLayout(self.image_layout)
        layout.addStretch(stretch=4)
        box.addWidget(self.backward)
        box.addWidget(self.play)
        box.addWidget(self.forward)
        layout.addWidget(self.subheading)
        layout.addLayout(box)
        layout.addStretch(stretch=4)

        self.show()

    def lcd_timer(self):
        time = QTime(self.time_counter // 3600, self.time_counter // 60, self.time_counter % 60)
        text = time.toString('hh:mm:ss')
        self.timer.display(text)
        self.time_counter += 1

        if self.time_counter == round(self.sound.get_length()):
            self.time_counter = 0
            self.playing = False
            self.last_url = None

            self.lcdtimer.stop()
            self.play_next_music()

    def playbutton(self):
        if self.playing:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music_list[self.current_music_index])
        self.last_url = self.music_list[self.current_music_index]
        pygame.mixer.music.play()


        self.sound = pygame.mixer.Sound(self.music_list[self.current_music_index])
        self.time_counter = 0
        self.current_music_index += 1
        if self.current_music_index >= len(self.music_list):
            self.current_music_index = 0

        self.subheading.setText(self.music_list[self.current_music_index -1 ][6:-4])

        self.lcdtimer.start(round(self.sound.get_length() * 1000))
        self.playing = True

    def play_next_music(self):
        pygame.mixer.music.stop()
        self.playbutton()

    def backwardbutton(self):
        if self.playing:
            if self.time_counter > 10:
                pygame.mixer.music.pause()
                pygame.mixer.music.set_pos(self.time_counter - 10)
                self.time_counter -= 10
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.rewind()
                self.time_counter = 0

    def forwardbutton(self):
        if self.playing:
            if self.time_counter + 10 < self.sound.get_length():
                pygame.mixer.music.pause()
                pygame.mixer.music.set_pos(self.time_counter + 10)
                self.time_counter += 10
                pygame.mixer.music.unpause()
            else:
                pass

