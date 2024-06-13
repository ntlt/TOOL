import sys
from datetime import datetime

import mysql.connector
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from Show_Data import Ui_MainWindow

class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = ''
        self.password = ''
        self.port = '3306'
        self.database = 'test_db'
        self.con = None

    def connect(self):
        """
        create connect with database
        :return:
        """
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
            sql = "SELECT * FROM test_table;"
            cursor.execute(sql)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print("get data fail")
            print(e)

        finally:
            if self.con:
                self.con.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## Initialize the table
        self.result_table = self.ui.tableWidget

        ## Automatically fetch data from the database and display it in the table
        self.load_data()

    def load_data(self):
        """
        Fetch data from the database and display it in the table.
        """
        result = ConnectToMySQL().get_all_data_from_db()

        if result:
            self.result_table.setRowCount(len(result))

            for row, item in enumerate(result):
                column_1_item = QTableWidgetItem(str(item['column1']))
                column_2_item = QTableWidgetItem(str(item['column2']))

                self.result_table.setItem(row, 0, column_1_item)
                self.result_table.setItem(row, 1, column_2_item)
        else:
            ## Show a message if no data was retrieved from the database
            QMessageBox.information(self, 'Warning', 'No data retrieved from the database, please try again')
            return

if __name__ == '__main__':
    print("start")
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
