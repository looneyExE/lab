from PyQt5 import QtWidgets
from view import MeterApp
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MeterApp()
    window.show()
    sys.exit(app.exec_())
