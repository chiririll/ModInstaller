import os
import sys
import Utils
from PyQt5 import QtWidgets

from Widgets import main


class ModUpdater(QtWidgets.QMainWindow, main.Ui_MainWindow):

    Mods = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.link_events()
        self.set_default_values()
        # TODO: get mods list and update field

    # Fields updaters #
    def set_default_values(self):
        self.MCPathText.setText(Utils.local.get_mc_path())
        self.update_mods_list()

    def update_mods_list(self):
        mc_path = self.MCPathText.text()
        if mc_path == '':
            return

        mod_path = os.path.join(mc_path, 'mods')
        self.Mods = Utils.local.check_mods(mod_path)

        for modID, params in self.Mods.items():
            if modID == '?':
                for f in params:
                    self.InstalledModsList.addItem(f)
            else:
                self.InstalledModsList.addItem(params[1])

    # =============== #

    # Events (Buttons) #
    def link_events(self):
        self.MCPathSelect.clicked.connect(self.select_mc_folder)
        self.DeleteBtn.clicked.connect(self.delete_mod)

    # Select folder
    def select_mc_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder", self.MCPathText.text())
        if path:
            self.MCPathText.setText(str(path))

    # Delete
    def delete_mod(self):
        if self.DeleteCheck.checkState():
            return

    # =============== #


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ModUpdater()
    window.show()
    app.exec_()
