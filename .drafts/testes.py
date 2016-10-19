from PySide import QtCore, QtGui


class Form(QtGui.QDialog):

    app = QApplication(sys.argv)
    # Create a Label and show it
    label = QLabel("Hello World")
    label.show()
    # Enter Qt application main loop
    app.exec_()
    sys.exit()
