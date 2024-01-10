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
    
    def add_paystub(self, paystub):
        try:
            cursor = self.cnx.cursor()
            add_paystub_query = ("INSERT INTO paystubs "
                                 "(employee_id, total_hours_worked, day_hours, night_hours, holiday_day_hours, holiday_night_hours, number_of_services, month_year) "
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            paystub_data = (paystub.employee_id, paystub.total_hours_worked, paystub.day_hours, paystub.night_hours, paystub.holiday_day_hours, paystub.holiday_night_hours, paystub.number_of_services, paystub.month_year)
            cursor.execute(add_paystub_query, paystub_data)
            self.cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")

    def update_paystub(self, paystub):
        try:
            cursor = self.cnx.cursor()
            update_paystub_query = ("UPDATE paystubs SET total_hours_worked = %s, day_hours = %s, night_hours = %s, holiday_day_hours = %s, holiday_night_hours = %s, number_of_services = %s, month_year = %s "
                                    "WHERE id = %s")
            paystub_data = (paystub.total_hours_worked, paystub.day_hours, paystub.night_hours, paystub.holiday_day_hours, paystub.holiday_night_hours, paystub.number_of_services, paystub.month_year, paystub.id)
            cursor.execute(update_paystub_query, paystub_data)
            self.cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")