To send sensor data to your PyQt5 application and insert it into a MySQL database, you can set up a method to receive data from the sensors. Typically, sensors communicate with applications via various interfaces such as serial communication (e.g., UART, SPI, I2C), network communication (e.g., HTTP, MQTT), or directly through hardware interfaces. Here’s how you can handle the process:

Example Using a Serial Interface (e.g., UART)
Set up the sensor to send data via a serial port.

Modify your PyQt5 application to read data from the serial port and insert it into the database.

First, install the pyserial library if you haven't already:

sh
Copy code
pip install pyserial
1. Modify the UIExecute Class to Use PySerial for Reading Sensor Data
Here’s an example of how you can integrate PySerial into your PyQt5 application:

python
Copy code
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import random
import serial

class ConnectToMySQL:
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'Linhtrang2112@'
        self.port = '3306'
        self.database = 'mydatabase'
        self.con = None

    def connect(self):
        self.con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port,
            database=self.database
        )

    def get_all_data_from_db(self):
        try:
            self.connect()
            cursor = self.con.cursor(dictionary=True)
            sql = "SELECT * FROM jig;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except Exception as e:
            print("get data fail")
            print(e)

        finally:
            if self.con:
                self.con.close()

    def insert_data(self, reference, value, result):
        try:
            self.connect()
            cursor = self.con.cursor()
            sql = "INSERT INTO jig (REFERENCE, VALUE, RESULT, DATE) VALUES (%s, %s, %s, %s)"
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(sql, (reference, value, result, current_date))
            self.con.commit()

        except Exception as e:
            print("insert data fail")
            print(e)

        finally:
            if self.con:
                self.con.close()

class UIExecute(QtWidgets.QMainWindow):
    def __init__(self):
        super(UIExecute, self).__init__()
        self.setupUi()
        self.setWindowTitle('Sensor Data Logger')
        self.showMaximized()

        # Initialize the table or other UI elements
        self.result_table = QtWidgets.QTableWidget(self)
        self.result_table.setGeometry(QtCore.QRect(50, 50, 600, 500))
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Reference', 'Value', 'Result', 'Date'])

        self.load_data()

        # Setup QTimer to fetch and insert data periodically
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.fetch_and_insert_data)
        self.timer.start(5000)  # Set the interval to 5000 ms (5 seconds)

        # Setup serial port for sensor data
        self.serial_port = serial.Serial('COM3', 9600)  # Replace 'COM3' with your actual serial port
        self.serial_timer = QtCore.QTimer(self)
        self.serial_timer.timeout.connect(self.read_serial_data)
        self.serial_timer.start(1000)  # Check serial port every 1000 ms (1 second)

    def setupUi(self):
        # Setup UI elements
        self.setGeometry(100, 100, 800, 600)

    def fetch_and_insert_data(self):
        # Placeholder for any periodic fetching logic
        pass

    def read_serial_data(self):
        if self.serial_port.in_waiting > 0:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                reference = 'sensor_1'
                value = line  # Assuming the line contains the sensor value
                result = 'PASS'  # Determine result based on value, replace with actual logic
                ConnectToMySQL().insert_data(reference, value, result)
                self.load_data()
            except Exception as e:
                print(f"Failed to read serial data: {e}")

    def load_data(self):
        result = ConnectToMySQL().get_all_data_from_db()

        if result:
            self.result_table.setRowCount(len(result))

            for row, item in enumerate(result):
                column_1_item = QTableWidgetItem(str(item['REFERENCE']))
                column_2_item = QTableWidgetItem(str(item['VALUE']))
                column_3_item = QTableWidgetItem(str(item['RESULT']))
                column_4_item = QTableWidgetItem(str(item['DATE']))

                self.result_table.setItem(row, 0, column_1_item)
                self.result_table.setItem(row, 1, column_2_item)
                self.result_table.setItem(row, 2, column_3_item)
                self.result_table.setItem(row, 3, column_4_item)
        else:
            QMessageBox.information(self, 'Warning', 'No data retrieved from the database, please try again')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = UIExecute()
    mainWin.show()
    sys.exit(app.exec_())
Explanation
QTimer for Serial Data: This uses a QTimer (self.serial_timer) to periodically check the serial port for incoming data.
Serial Data Reading: The read_serial_data method reads from the serial port, decodes the incoming data, and inserts it into the database.
Sensor Data Assumption: In this example, it's assumed that the sensor sends a single value per line. Adjust this to fit your actual sensor data format.
Adjustments for Different Interfaces
If your sensor uses a different communication method (e.g., network communication like HTTP, MQTT, etc.), you would replace the serial communication logic with the appropriate method to receive data.

For example, for HTTP requests, you might use the requests library to poll an endpoint, or for MQTT, you might use the paho-mqtt library to subscribe to a topic.

Conclusion
By incorporating PySerial (or other communication methods) and using a QTimer to periodically read sensor data and update the database, your PyQt5 application can continuously receive and process sensor data without requiring user interaction. Adjust the sensor data handling logic to fit your specific requirements and sensor communication protocols.






