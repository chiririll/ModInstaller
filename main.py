import os
import sys
import utils
from PyQt5 import QtWidgets

from Widgets import main


class ModUpdater(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.link_events()
        self.set_default_values()
        # TODO: get mods list and update field

    def link_events(self):
        self.MCPathSelect.clicked.connect(self.select_mc_folder)

    def set_default_values(self):
        self.MCPathText.setText(utils.get_mc_path())
        # self.update_mods_list()

    def select_mc_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder", self.MCPathText.text())
        if path:
            self.MCPathText.setText(str(path))

    def update_mods_list(self):
        mc_path = self.MCPathText.text()
        if mc_path == '':
            return

        mod_path = os.path.join(mc_path, 'mods')
        print(utils.check_mods(mod_path))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ModUpdater()
    window.show()
    app.exec_()
