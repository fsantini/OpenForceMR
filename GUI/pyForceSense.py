import sys
import glob
import serial
import re
import time
from datetime import datetime
import os.path

#import PySide
import PyQt4
import pyqtgraph as pg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyForceSense_ui import Ui_PyForceSenseWidget

BAUD = 9600
#SERIAL_PORT = '/dev/ttyUSB0'
#SERIAL_PORT = '/dev/ttyS98'
SERIAL_TIMER_INTERVAL = 20
MAXPLOTLENGTH = 100

forceStringPattern = re.compile('Force: ([-.0-9]+)')

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
        #ports = glob.glob('/dev/pts/2')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class PyForceSense(Ui_PyForceSenseWidget, QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.maxForce = 0.0
        self.curForce = 0.0
        self.serialTimer = None
        self.resetMaxBtn.clicked.connect(self.resetMax)
        self.forcePlotObj = self.forcePlot.plot()
        self.plotData = []
        ports = serial_ports()
        self.trigPositions = []
        self.comportCombo.addItems(ports)
        self.connectButton.clicked.connect(self.serialConnect)
        self.autoNameButton.clicked.connect(self.autoName)
        self.logging = False
        self.logButton.clicked.connect(self.toggleLog)
        self.logFile = None
        self.clearButton.clicked.connect(lambda : self.serialOutputText.setPlainText(""));
        self.resetTareButton.clicked.connect(self.resetTare)
        self.serial = None
        self.autoName()
        self.yellowPen = pg.mkPen('y')
        
    def resetTare(self):
        if not self.checkSerialAvailable(): return
        ans = QMessageBox.warning(self, "Reset", "Resetting tare. Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.serial.write("RESET\n");
        
    def toggleLog(self):
        if self.logging:
            # stop logging
            self.logging = False
            self.logButton.setText("Start logging")
            self.logButton.setStyleSheet("")
            if self.logFile:
                self.serialOutputText.appendPlainText("Saving log")
                self.logFile.close()
                self.logFile = None
        else:
            if os.path.isfile(str(self.logName.text())):
                ret = QMessageBox.warning(self, "Warning", "LogFile exists! Overwrite?", QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.No:
                    return
            self.serialOutputText.appendPlainText("Opening log file: " + str(self.logName.text()))
            try:
                self.logFile = open(str(self.logName.text()), 'w')
                self.logFile.write("time,force,other\n")
            except:
                self.logFile = None
                self.serialOutputText.appendPlainText("Error opening log file")
                return
            self.logging = True
            self.logButton.setText("Stop logging")
            self.logButton.setStyleSheet("background-color: #FF5555;")
        
    def autoName(self):
        oldTxt = str(self.logName.text())
        pos = oldTxt.find('_')
        if pos < 0:
            baseStr = "LogFile"
        else:
            baseStr = oldTxt[:pos]
        self.logName.setText(baseStr + time.strftime("_%Y-%m-%d_%H.%M.%S.txt"))
        
    def serialConnect(self):
        if self.serial is not None:
            # we are already connected
            ans = QMessageBox.warning(self, "Disconnect", "Are you sure you want to disconnect?", QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.serialDisconnect()
            return
        try:
            self.serial = serial.Serial(str(self.comportCombo.currentText()), BAUD, timeout=0.5)
        except (OSError, serial.SerialException):
            self.serialOutputText.appendPlainText("Cannot open serial")
            self.serial = None
            return
        
        self.connectButton.setText("Disconnect")
        self.comportCombo.setEnabled(False)
        
        self.serialTimer = QTimer()
        self.serialTimer.timeout.connect(self.checkSerial)
        self.serialTimer.start(SERIAL_TIMER_INTERVAL)

    def serialDisconnect(self):
        self.connectButton.setText("Connect")
        self.comportCombo.setEnabled(True)
        if self.serialTimer: self.serialTimer.stop()
        self.serial = None
        
    def checkSerialAvailable(self):
        if not self.serial or not self.serial.readable():
            # reset serial connection
            self.serialDisconnect()
            return False
        return True

    def checkSerial(self):
        if not self.checkSerialAvailable(): return
        if self.serial.in_waiting:
            serStr = self.serial.readline().strip()
            #print serStr
            self.processSerial(serStr)

    def makeLine(self, value):
        line = pg.InfiniteLine(movable=False, angle=90, pen=self.yellowPen, pos=value)
        self.forcePlot.addItem(line)
        return line

    def processSerial(self, serialString):
        #self.serialOutputText.appendPlainText(str)
        m = forceStringPattern.match(serialString) 
        if m is not None:
            self.curForce = float(m.group(1));
            if self.curForce > self.maxForce: self.maxForce = self.curForce
            if self.logFile:
                timestamp = time.time()
                self.logFile.write("%f,%f,\"\"\n" % (timestamp, self.curForce))
            self.updateUi()
        else:
            self.serialOutputText.appendPlainText(serialString)
            if self.logFile:
                timestamp = time.time()
                self.logFile.write("%f,,\"%s\"\n" % (timestamp, serialString))
            if serialString.upper() == "TRIG":
                self.trigPositions.append(self.makeLine(len(self.plotData)))
            
    def closeEvent(self, event):
        if self.logFile:
            print "Saving log"
            self.logFile.close()
            
        event.accept()
            
    def resetMax(self):
        #self.serialOutputText.clear()
        self.maxForce = 0.0
        self.updateUi()
            
    def updateUi(self):
        self.curForceLabel.setText('{:.2f}'.format(self.curForce))
        self.maxForceLabel.setText('{:.2f}'.format(self.maxForce))
        self.plotData.append(self.curForce)
        while len(self.plotData) > MAXPLOTLENGTH: 
            self.plotData.pop(0)
            # update trigPositions. Remove positions in the past
            while len(self.trigPositions) > 0 and self.trigPositions[0].value() <= 0:
                self.forcePlot.removeItem(self.trigPositions[0])
                self.trigPositions.pop(0)
            for posIndex in range(len(self.trigPositions)):
                self.trigPositions[posIndex].setValue(self.trigPositions[posIndex].value() - 1)
                
        self.forcePlotObj.setData(self.plotData)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyForceSense()
    window.show()

    sys.exit(app.exec_())
