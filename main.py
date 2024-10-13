import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtCore import QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon

class GameUlar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Ular | Copyright Arif Maulana Azis 2024')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(400, 400, 500, 500)
        self.center()
        self.board = GameBoard(self)
        self.setCentralWidget(self.board)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class GameBoard(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.high_score = 0
        self.initBoard()

    def initBoard(self):
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)
        self.ular = [(50, 50), (40, 50), (30, 50)]
        self.arah = 'RIGHT'
        self.dalam_game = True
        self.skor = 0
        self.rintangan = []
        self.makanan = (0, 0)
        self.initGame()

    def initGame(self):
        self.TempatkanMakanan()
        self.BuatRintangan()
        self.timer.start(140, self)

    def BuatRintangan(self):
        jumlah_rintangan = 5
        self.rintangan.clear()
        for _ in range(jumlah_rintangan):
            obs_x = random.randint(0, self.width() // 10 - 1) * 10
            obs_y = random.randint(0, self.height() // 10 - 1) * 10
            self.rintangan.append((obs_x, obs_y))

    def TempatkanMakanan(self):
        self.makanan = (random.randint(0, self.width() // 10 - 1) * 10,
                      random.randint(0, self.height() // 10 - 1) * 10)

    def PeriksaTabrakan(self):
        kepala_ular = self.ular[0]
        if kepala_ular in self.ular[1:]:
            self.dalam_game = False
        if kepala_ular[0] < 0 or kepala_ular[0] >= self.width() or kepala_ular[1] < 0 or kepala_ular[1] >= self.height():
            self.dalam_game = False
        if kepala_ular in self.rintangan:
            self.dalam_game = False

    def Gerak(self):
        kepala_ular = self.ular[0]
        if self.arah == 'LEFT':
            new_head = (kepala_ular[0] - 10, kepala_ular[1])
        elif self.arah == 'RIGHT':
            new_head = (kepala_ular[0] + 10, kepala_ular[1])
        elif self.arah == 'UP':
            new_head = (kepala_ular[0], kepala_ular[1] - 10)
        elif self.arah == 'DOWN':
            new_head = (kepala_ular[0], kepala_ular[1] + 10)

        self.ular = [new_head] + self.ular[:-1]

    def PeriksaMakananDimakan(self):
        if self.ular[0] == self.makanan:
            self.ular.append(self.ular[-1]) 
            self.skor += 10
            self.TempatkanMakanan()

    def paintEvent(self, event):
        qp = QPainter(self)
        if self.dalam_game:
            self.LetakkanObjek(qp)
        else:
            self.gameOver(qp)

    def LetakkanObjek(self, qp):
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(self.makanan[0], self.makanan[1], 10, 10)

        for i, (x, y) in enumerate(self.ular):
            if i == 0:
                qp.setBrush(QColor(0, 255, 0))
            else:
                qp.setBrush(QColor(0, 128, 0))
            qp.drawRect(x, y, 10, 10)

        qp.setBrush(QColor(128, 128, 128))
        for (x, y) in self.rintangan:
            qp.drawRect(x, y, 10, 10)

        self.TulisSkor(qp)

    def TulisSkor(self, qp):
        qp.setFont(QFont('Arial', 12, QFont.Bold))
        qp.setPen(QColor(0, 0, 0))
        qp.drawText(10, 20, f"Skor saat ini: {self.skor}")
        qp.drawText(10, 40, f"Skor Tertinggi: {self.high_score}")

    def gameOver(self, qp):
        if self.skor > self.high_score:
            self.high_score = self.skor

        qp.setFont(QFont('Arial', 16, QFont.Bold))
        qp.setPen(QColor(255, 0, 0))
        qp.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignCenter, "Game Berakhir\nTekan Spasi untuk memulai ulang")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left and self.arah != 'RIGHT':
            self.arah = 'LEFT'
        if key == Qt.Key_Right and self.arah != 'LEFT':
            self.arah = 'RIGHT'
        if key == Qt.Key_Up and self.arah != 'DOWN':
            self.arah = 'UP'
        if key == Qt.Key_Down and self.arah != 'UP':
            self.arah = 'DOWN'
        if key == Qt.Key_Space and not self.dalam_game:
            self.MulaiUlangGame()

    def timerEvent(self, event):
        if self.dalam_game:
            self.PeriksaMakananDimakan()
            self.PeriksaTabrakan()
            self.Gerak()
        self.update()

    def MulaiUlangGame(self):
        self.ular = [(50, 50), (40, 50), (30, 50)]
        self.arah = 'RIGHT'
        self.skor = 0
        self.dalam_game = True
        self.initGame()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ular = GameUlar()
    sys.exit(app.exec_())
