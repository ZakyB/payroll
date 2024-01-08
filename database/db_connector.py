import mysql.connector

from models.paystub import PayStub
from collections import namedtuple


class DBConnector:
    def __init__(self, host, database, user, password):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
        
    def get_paystubs_by_employee(self, employee_id, year, month):
        date = f"{year}-{str(month).zfill(2)}-01"  # add "-01" to represent the first day of the month
        results = self.execute_query('SELECT * FROM paystubs WHERE employee_id = %s AND month_year = %s', (employee_id, date))
        return [PayStub(*row) for row in results]
    
    def get_all_employees(self):
        Employee = namedtuple('Employee', ['id', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'salary'])

        cursor = self.connection.cursor()
        query = "SELECT * FROM employees"
        cursor.execute(query)

        employees = [Employee(*row) for row in cursor.fetchall()]
        return employees