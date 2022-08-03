import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit)
from PyQt6.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('HIDAPITester')

        mono_font = QFont('Courier',13)

        self.label = QLabel()
        self.label.setFont(mono_font)
        self.label.setText('> hidapitester ')

        self.sendBtn = QPushButton('Send')
        self.sendBtn.setAutoDefault(True)
        self.sendBtn.clicked.connect(self.send_btn_slot)

        self.input = QLineEdit('--list')        
        self.input.setFont(mono_font)
        self.input.returnPressed.connect(self.sendBtn.click)
        # self.input.textChanged.connect(self.label.setText)

        self.output = QPlainTextEdit()
        self.output.setFont(mono_font)
        self.output.setReadOnly(True)

        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(self.label)
        cmd_layout.addWidget(self.input)
        cmd_layout.addWidget(self.sendBtn)

        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addLayout(cmd_layout)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def send_btn_slot(self):
        command = self.input.text().split(' ')
        p1 = subprocess.Popen(
            [f'{os.getcwd()}/hidapitester'] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        c = p1.communicate()
        try:
            self.output.appendPlainText(f'> hidapitester {" ".join(command)}')

            stdout = c[0].decode()
            stderr = c[1].decode()
            if stdout: self.output.appendPlainText(stdout)
            if stderr: self.output.appendPlainText(stderr)
        except UnicodeDecodeError:
            print('UnicodeDecodeError')



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()