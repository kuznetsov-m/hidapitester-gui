import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QComboBox)
from PyQt6.QtGui import QFont


class MainWindow(QMainWindow):
    _args = {}

    def __init__(self):
        super().__init__()

        self.setWindowTitle('HIDAPITester')

        mono_font = QFont('Courier', 13)

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

        current_device_hl = QHBoxLayout()
        current_device_hl.addWidget(QLabel('Device:'))
        self.current_device_cb = QComboBox()
        self.current_device_cb.currentText()
        self.current_device_cb.addItems(self.get_devices_list())
        self.current_device_cb.currentIndexChanged.connect(self.on_current_device_cb_index_changed)
        current_device_hl.addWidget(self.current_device_cb)

        cmd_hl = QHBoxLayout()
        cmd_hl.addWidget(self.label)
        cmd_hl.addWidget(self.input)
        cmd_hl.addWidget(self.sendBtn)

        vl = QVBoxLayout()
        vl.addLayout(current_device_hl)
        vl.addWidget(self.output)
        vl.addLayout(cmd_hl)

        container = QWidget()
        container.setLayout(vl)

        self.setCentralWidget(container)

    def send_btn_slot(self):
        command = [v for item in self._args.items() for v in item]
        command += list(filter(self.input.text().split(' ')))
        c = self.exec_cmd(command)
        try:
            self.output.appendPlainText(f'> hidapitester {" ".join(command)}')

            stdout = c[0].decode()
            stderr = c[1].decode()
            if stdout: self.output.appendPlainText(stdout)
            if stderr: self.output.appendPlainText(stderr)
        except UnicodeDecodeError:
            print('UnicodeDecodeError')

    def on_current_device_cb_index_changed(self):
        text = self.current_device_cb.currentText()
        if text == '(none)':
            del self._args['--vidpid']
        else:
            self._args['--vidpid'] = text.split(':')[0]
        self.update_args()

    def get_devices_list(self):
        c = self.exec_cmd(['--list'])
        try:
            stdout = c[0].decode()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
        
        return ['(none)'] + list(filter(None, stdout.split('\n'))) if stdout else []

    def update_args(self):
        text = '> hidapitester'
        for k, v in self._args.items():
            text += f' {k} {v}'
        self.label.setText(text)

    def exec_cmd(self, args: list) -> dict:
        print(args)
        p1 = subprocess.Popen(
            [f'{os.getcwd()}/hidapitester'] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        return p1.communicate()





if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()