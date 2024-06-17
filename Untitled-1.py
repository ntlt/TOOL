Create a method to insert data into the database.
Modify the UI to call this method.
Here is a revised version of your code with these functionalities added:

1. Modify the ConnectToMySQL class to include an insert_data method:
python
Copy code
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

    def set_all_data_from_db(self):
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
2. Modify the UIExecute class to add buttons and connect them to functions that will insert data into the database:
Add buttons to the UI in the setupUi method (this is a placeholder, and the actual implementation may vary based on your UI design):

python
Copy code
class UIExecute(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UIExecute, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(window_title)
        self.showMaximized()

        # Add buttons for inserting data
        self.btn_add_data = QtWidgets.QPushButton("Add Data", self)
        self.btn_add_data.setGeometry(QtCore.QRect(100, 600, 100, 30))
        self.btn_add_data.clicked.connect(self.add_data_to_db)

        self.btn_refresh = QtWidgets.QPushButton("Refresh", self)
        self.btn_refresh.setGeometry(QtCore.QRect(220, 600, 100, 30))
        self.btn_refresh.clicked.connect(self.load_data)

        # Other initializations...

        self.load_data()

    def add_data_to_db(self):
        reference = 'sensor_1'
        value = '123'  # Replace this with actual sensor data
        result = 'PASS'  # Replace this with the actual result
        ConnectToMySQL().insert_data(reference, value, result)
        QMessageBox.information(self, 'Info', 'Data added successfully!')
        self.load_data()
In the add_data_to_db method, you can replace the hard-coded values (reference, value, and result) with actual data from your sensors or other input sources.

3. Ensure the load_data method updates the table:
python
Copy code
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
            return
4. Update your database table schema to include a DATE column if not already present:
sql
Copy code
ALTER TABLE jig ADD COLUMN DATE DATETIME;
Conclusion:
With these changes, your application will have the capability to insert sensor data into the database and refresh the UI to reflect the latest data. Adjust the UI design and database schema as necessary to match your specific requirements.