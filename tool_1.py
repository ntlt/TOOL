import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import QSettings
import serial.tools.list_ports

class SerialPortTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Populate COM ports
        self.populateCOMPorts()

        # Load settings
        self.loadSettings()

    def initUI(self):
        self.setWindowTitle('Serial Port Tool')

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.portLabel = QLabel('Select COM Port:')
        self.layout.addWidget(self.portLabel)

        self.portComboBox = QComboBox()
        self.layout.addWidget(self.portComboBox)

        self.baudRateLabel = QLabel('Select Baud Rate:')
        self.layout.addWidget(self.baudRateLabel)

        self.baudRateComboBox = QComboBox()
        self.baudRateComboBox.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.layout.addWidget(self.baudRateComboBox)

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectSerialPort)
        self.layout.addWidget(self.connectButton)

        self.refreshButton = QPushButton('Refresh COM Ports')
        self.refreshButton.clicked.connect(self.populateCOMPorts)
        self.layout.addWidget(self.refreshButton)

    def populateCOMPorts(self):
        ports = serial.tools.list_ports.comports()
        self.portComboBox.clear()
        for port in ports:
            self.portComboBox.addItem(port.device)

    def connectSerialPort(self):
        com_port = self.portComboBox.currentText()
        baud_rate = self.baudRateComboBox.currentText()

        # Here you can add code to actually connect to the serial port using pyserial
        # Example:
        # ser = serial.Serial(com_port, baud_rate)

        # Save settings
        self.saveSettings(com_port, baud_rate)

    def loadSettings(self):
        settings = QSettings('MyCompany', 'SerialPortTool')
        com_port = settings.value('com_port', '')
        baud_rate = settings.value('baud_rate', '9600')

        # Check if the saved com_port is in the current list of ports
        index = self.portComboBox.findText(com_port)
        if index != -1:
            self.portComboBox.setCurrentIndex(index)
        else:
            # If not found, select the first available port or leave empty if no ports are available
            if self.portComboBox.count() > 0:
                self.portComboBox.setCurrentIndex(0)

        index = self.baudRateComboBox.findText(baud_rate)
        if index != -1:
            self.baudRateComboBox.setCurrentIndex(index)

    def saveSettings(self, com_port, baud_rate):
        settings = QSettings('MyCompany', 'SerialPortTool')
        settings.setValue('com_port', com_port)
        settings.setValue('baud_rate', baud_rate)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialPortTool()
    window.show()
    sys.exit(app.exec_())
