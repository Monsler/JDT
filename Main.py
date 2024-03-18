import glob
import subprocess
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
import PyQt5.uic as uic
import darkdetect
from darktheme.widget_template import DarkPalette


import os.path
import sys


def resource(file):
    try:
        res = sys._MEIPASS
    except Exception:
        res = os.path.abspath('.')
    return os.path.join(res, file)


class App:
    ui = None
    app = None
    win = None

    def __init__(self):
        if darkdetect.isDark():
            self.app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
            self.app.setStyle('Fusion')
            self.app.setPalette(DarkPalette())
        else:
            self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.ui = uic.loadUi(resource('res/MainForm.ui'), self.win)
        self.win.resize(700, 350)
        self.win.show()
        self.win.setWindowTitle('JDT')
        self.win.setWindowIcon(QIcon(resource('res/code.png')))
        self.ui.add.clicked.connect(self.class_add)
        self.ui.filesList.doubleClicked.connect(self.files_list_logic_remove)
        self.ui.process.clicked.connect(self.process_files)
        QMessageBox.information(None, 'Python info', 'Python '+sys.version)
        try:
            os.mkdir('java')
        except:
            print('Folder output already exists, skipping')

        folder = glob.glob('java/*')
        for f in folder:
            os.remove(f)
        sys.exit(self.app.exec_())

    def process_files(self):
        files_to_decompile = [self.ui.filesList.item(i).text() for i in range(self.ui.filesList.count())]
        procedure = 0
        unprocedure = 0
        for file in files_to_decompile:
            filename, ext = os.path.splitext(file)
            print('java -jar ' + str(resource('lib\\procyon.jar')) + f' {file}')
            try:
                log = subprocess.getoutput('java -jar ' + str(resource('lib/procyon.jar')) + f' {file}')
                fs = Path(f'{filename}').stem
                with open(f'./java/{fs}.java', 'w') as f:
                    if not log.startswith("!!! ERROR"):
                        f.write(log)
                        f.close()
                        procedure += 1
                    else:
                        unprocedure += 1
                print(file, 'decompiled')
            except:
                unprocedure += 1
                print('ERR')
        QMessageBox.information(None, 'Decompilation Stats', f'{procedure} file(s) decompiled, {unprocedure} skipped'
                                                             f'\nSaved to "java" directory in one dir with this '
                                                             f'program executable.')

    def files_list_logic_remove(self):
        self.ui.filesList.takeItem(self.ui.filesList.row(self.ui.filesList.currentItem()))

    def class_add(self):
        file = QFileDialog.getOpenFileName(None, 'Open .class file', 'c:\\')
        if file[0] != '':
            self.ui.filesList.addItem(file[0])
            self.ui.console.setPlainText("Open file " + file[0])


if __name__ == '__main__':
    print('JDT made with PyQt5; Python', sys.version)
    App()
