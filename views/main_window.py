import tkinter as tk

from database.db_connector import DBConnector
from views.employee_view import EmployeeView
from views.paystub_view import PayStubView
from datetime import datetime
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Payroll System")
        self.geometry("400x400")

        self.employee_view = EmployeeView(self)
        self.employee_view.grid(row=0, column=0)

        self.paystub_view = PayStubView(self)
        self.paystub_view.grid(row=0, column=1)

        self.db = DBConnector('127.0.0.1', 'payroll', 'root', '')

        # Create a StringVar to hold the selected employee
        self.selected_employee = tk.StringVar(self)
        self.selected_employee.set("List of Employees")  # Set the initial value

        # Create the dropdown menu
        self.employee_dropdown = tk.OptionMenu(self, self.selected_employee, ())
        self.employee_dropdown.grid(row=1, column=0)

        # Create a StringVar for the selected year and month
        self.selected_year = tk.StringVar(self)
        self.selected_month = tk.StringVar(self)

        
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Set the initial value of the year and month dropdowns to the current year and month
        self.selected_year.set(current_year)
        self.selected_month.set(current_month)

        # Create labels for the year and month dropdowns
        self.year_label = tk.Label(self, text="Year:")
        self.year_label.grid(row=1, column=1, sticky='e')
        self.month_label = tk.Label(self, text="Month:")
        self.month_label.grid(row=1, column=3, sticky='e')

        # Create the year and month dropdown menus
        self.year_dropdown = tk.OptionMenu(self, self.selected_year, *range(2022, 2030))
        self.year_dropdown.grid(row=1, column=2)
        self.month_dropdown = tk.OptionMenu(self, self.selected_month, *range(1, 13))
        self.month_dropdown.grid(row=1, column=4)

        # Update the dropdown menu when an employee is selected
        self.selected_employee.trace_add('write', self.update_employee_view)
        self.selected_year.trace_add('write', self.update_employee_view)
        self.selected_month.trace_add('write', self.update_employee_view)

    def update_views(self):
        employees = self.db.get_all_employees()

        # Update the dropdown menu with the names of the employees
        menu = self.employee_dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="List of Employees", state="disabled")
        for employee in employees:
            menu.add_command(label=f"{employee.first_name} {employee.last_name}", command=lambda emp=employee: self.selected_employee.set(f"{emp.first_name} {emp.last_name}"))

    def update_employee_view(self, *args):
        # Get the selected employee
        selected = self.selected_employee.get()

        # If no employee is selected, do nothing
        if selected == "List of Employees":
            return

        first_name, last_name = selected.split(' ')

        # Find the employee with the selected name
        employees = self.db.get_all_employees()
        for employee in employees:
            if employee.first_name == first_name and employee.last_name == last_name:
                self.employee_view.display_employee(employee)
                paystubs = self.db.get_paystubs_by_employee(employee.id, self.selected_year.get(), self.selected_month.get())
                if paystubs:
                    for paystub in paystubs:
                        self.paystub_view.display_paystub(paystub)
                else:
                    self.paystub_view.display_paystub()  # Display "N/A" for all values
                break