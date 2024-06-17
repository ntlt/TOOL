To automatically insert sensor data into the database continuously and update the PyQt5 UI without requiring a button press, you can use a QTimer to periodically fetch and insert the sensor data. Here’s how to achieve that:

1. Modify the ConnectToMySQL Class to Include an insert_data Method
This method will handle inserting the sensor data into the database:

python
Copy code
import mysql.connector
from datetime import datetime

class ConnectToMySQL():
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
2. Modify the UIExecute Class to Use QTimer for Continuous Data Insertion
The UIExecute class will now use QTimer to automatically fetch and insert sensor data, and update the table periodically:

python
Copy code
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import random

class UIExecute(QtWidgets.QMainWindow):
    def __init__(self):
        super(UIExecute, self).__init__()
        self.setupUi(self)
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

    def fetch_and_insert_data(self):
        # Replace this section with actual sensor data fetching logic
        reference = 'sensor_1'
        value = str(random.randint(0, 100))  # Simulating sensor data
        result = 'PASS' if random.choice([True, False]) else 'FAIL'
        ConnectToMySQL().insert_data(reference, value, result)
        self.load_data()

    def load_data(self):
        """
        Fetch data from the database and display it in the table.
        """
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
3. Ensure the Database Table Schema is Updated
Ensure that your jig table includes a DATE column:

sql
Copy code
ALTER TABLE jig ADD COLUMN DATE DATETIME;
Explanation
QTimer: The QTimer object is used to call the fetch_and_insert_data method at regular intervals (in this case, every 5 seconds). Adjust the interval as necessary.
fetch_and_insert_data: This method fetches sensor data (simulated in this example) and inserts it into the database using the insert_data method from the ConnectToMySQL class.
load_data: This method fetches all data from the database and updates the table in the UI to reflect the latest data.
Conclusion
With these changes, your application will automatically insert sensor data into the database continuously and refresh the UI to display the latest data. Replace the simulated sensor data fetching logic with actual data fetching from your sensors. Adjust the timer interval and UI design to meet your specific requirements.






