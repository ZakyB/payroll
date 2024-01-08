import tkinter as tk

class EmployeeView(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid()

        self.lbl_name = tk.Label(self, text="Name: ")
        self.lbl_name.grid(row=0, column=0)

        self.lbl_salary = tk.Label(self, text="Salary: ")
        self.lbl_salary.grid(row=1, column=0)

    def display_employee(self, employee):
        self.lbl_name['text'] = f"Name: {employee.first_name} {employee.last_name}"
        self.lbl_salary['text'] = f"Salary: {employee.salary}"