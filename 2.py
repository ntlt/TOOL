1. Modify the ConnectToMySQL Class to Include an insert_data Method:
Add a method to insert data into the database. Here is an updated version of your ConnectToMySQL class:

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
2. Modify the UIExecute Class to Add Buttons and Connect Them to Functions that Insert Data:
Add a button to the UI in the setupUi method and connect it to the add_data_to_db method:

python
Copy code
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class UIExecute(QtWidgets.QMainWindow):
    def __init__(self):
        super(UIExecute, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Sensor Data Logger')
        self.showMaximized()

        # Add buttons for inserting data
        self.btn_add_data = QtWidgets.QPushButton("Add Data", self)
        self.btn_add_data.setGeometry(QtCore.QRect(100, 600, 100, 30))
        self.btn_add_data.clicked.connect(self.add_data_to_db)

        self.btn_refresh = QtWidgets.QPushButton("Refresh", self)
        self.btn_refresh.setGeometry(QtCore.QRect(220, 600, 100, 30))
        self.btn_refresh.clicked.connect(self.load_data)

        # Initialize the table or other UI elements
        self.result_table = QtWidgets.QTableWidget(self)
        self.result_table.setGeometry(QtCore.QRect(50, 50, 600, 500))
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Reference', 'Value', 'Result', 'Date'])

        self.load_data()

    def add_data_to_db(self):
        reference = 'sensor_1'
        value = '123'  # Replace this with actual sensor data
        result = 'PASS'  # Replace this with the actual result
        ConnectToMySQL().insert_data(reference, value, result)
        QMessageBox.information(self, 'Info', 'Data added successfully!')
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
3. Ensure the load_data Method Updates the Table:
This method will fetch the latest data from the database and update the table:

python
Copy code
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
4. Update Your Database Table Schema to Include a DATE Column:
Ensure your jig table includes a DATE column. If not, run the following SQL command:

sql
Copy code
ALTER TABLE jig ADD COLUMN DATE DATETIME;
Conclusion:
With these changes, your application will be able to automatically insert sensor data into the database and refresh the UI to reflect the latest data. Replace the hard-coded values (reference, value, and result) in the add_data_to_db method with actual data from your sensors or other input sources. Adjust the UI design and database schema as necessary to match your specific requirements.