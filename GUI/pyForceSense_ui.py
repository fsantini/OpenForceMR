# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyForceSense.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PyForceSenseWidget(object):
    def setupUi(self, PyForceSenseWidget):
        PyForceSenseWidget.setObjectName(_fromUtf8("PyForceSenseWidget"))
        PyForceSenseWidget.resize(640, 480)
        self.curForceLabel = QtGui.QLabel(PyForceSenseWidget)
        self.curForceLabel.setGeometry(QtCore.QRect(27, 140, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.curForceLabel.setFont(font)
        self.curForceLabel.setStyleSheet(_fromUtf8("background-color: rgb(46, 255, 53)"))
        self.curForceLabel.setFrameShape(QtGui.QFrame.Panel)
        self.curForceLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.curForceLabel.setLineWidth(3)
        self.curForceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.curForceLabel.setObjectName(_fromUtf8("curForceLabel"))
        self.maxForceLabel = QtGui.QLabel(PyForceSenseWidget)
        self.maxForceLabel.setGeometry(QtCore.QRect(147, 140, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.maxForceLabel.setFont(font)
        self.maxForceLabel.setStyleSheet(_fromUtf8("background-color: rgb(255, 78, 81)"))
        self.maxForceLabel.setFrameShape(QtGui.QFrame.Panel)
        self.maxForceLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.maxForceLabel.setLineWidth(3)
        self.maxForceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.maxForceLabel.setObjectName(_fromUtf8("maxForceLabel"))
        self.serialOutputText = QtGui.QPlainTextEdit(PyForceSenseWidget)
        self.serialOutputText.setGeometry(QtCore.QRect(350, 10, 271, 231))
        self.serialOutputText.setReadOnly(True)
        self.serialOutputText.setObjectName(_fromUtf8("serialOutputText"))
        self.forcePlot = PlotWidget(PyForceSenseWidget)
        self.forcePlot.setGeometry(QtCore.QRect(20, 260, 601, 201))
        self.forcePlot.setObjectName(_fromUtf8("forcePlot"))
        self.resetMaxBtn = QtGui.QPushButton(PyForceSenseWidget)
        self.resetMaxBtn.setGeometry(QtCore.QRect(250, 140, 81, 21))
        self.resetMaxBtn.setObjectName(_fromUtf8("resetMaxBtn"))
        self.comportCombo = QtGui.QComboBox(PyForceSenseWidget)
        self.comportCombo.setGeometry(QtCore.QRect(20, 10, 211, 28))
        self.comportCombo.setObjectName(_fromUtf8("comportCombo"))
        self.connectButton = QtGui.QPushButton(PyForceSenseWidget)
        self.connectButton.setGeometry(QtCore.QRect(240, 10, 91, 29))
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.logButton = QtGui.QPushButton(PyForceSenseWidget)
        self.logButton.setGeometry(QtCore.QRect(20, 90, 311, 31))
        self.logButton.setObjectName(_fromUtf8("logButton"))
        self.logName = QtGui.QLineEdit(PyForceSenseWidget)
        self.logName.setGeometry(QtCore.QRect(20, 60, 211, 27))
        self.logName.setObjectName(_fromUtf8("logName"))
        self.autoNameButton = QtGui.QPushButton(PyForceSenseWidget)
        self.autoNameButton.setGeometry(QtCore.QRect(240, 60, 91, 29))
        self.autoNameButton.setObjectName(_fromUtf8("autoNameButton"))
        self.resetTareButton = QtGui.QPushButton(PyForceSenseWidget)
        self.resetTareButton.setGeometry(QtCore.QRect(250, 160, 81, 21))
        self.resetTareButton.setObjectName(_fromUtf8("resetTareButton"))
        self.clearButton = QtGui.QPushButton(PyForceSenseWidget)
        self.clearButton.setGeometry(QtCore.QRect(350, 240, 271, 21))
        self.clearButton.setObjectName(_fromUtf8("clearButton"))

        self.retranslateUi(PyForceSenseWidget)
        QtCore.QMetaObject.connectSlotsByName(PyForceSenseWidget)

    def retranslateUi(self, PyForceSenseWidget):
        PyForceSenseWidget.setWindowTitle(_translate("PyForceSenseWidget", "Form", None))
        self.curForceLabel.setText(_translate("PyForceSenseWidget", "0", None))
        self.maxForceLabel.setText(_translate("PyForceSenseWidget", "0", None))
        self.resetMaxBtn.setText(_translate("PyForceSenseWidget", "Reset Max", None))
        self.connectButton.setText(_translate("PyForceSenseWidget", "Connect", None))
        self.logButton.setText(_translate("PyForceSenseWidget", "Start logging", None))
        self.logName.setText(_translate("PyForceSenseWidget", "LogFile.txt", None))
        self.autoNameButton.setText(_translate("PyForceSenseWidget", "Auto Name", None))
        self.resetTareButton.setText(_translate("PyForceSenseWidget", "Reset Tare", None))
        self.clearButton.setText(_translate("PyForceSenseWidget", "Clear", None))

from pyqtgraph import PlotWidget
