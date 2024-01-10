import tkinter as tk

from database.db_connector import DBConnector
from views.employee_view import EmployeeView
from views.paystub_view import PayStubView
from datetime import datetime
from tkinter import messagebox
from decimal import Decimal
from tkinter import ttk
from models.paycheck import Paycheck
from models.paystub import PayStub
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Payroll System")
        self.geometry("500x400")

        self.employee_view = EmployeeView(self)
        self.employee_view.grid(row=0, column=0)

        self.paystub_view = PayStubView(self)
        self.paystub_view.grid(row=0, column=1)

        self.db = DBConnector('127.0.0.1', 'payroll', 'root', '')

        self.selected_employee = tk.StringVar(self)
        self.selected_employee.set("List of Employees")

        self.employee_dropdown = tk.OptionMenu(self, self.selected_employee, ())
        self.employee_dropdown.grid(row=1, column=0)

        self.selected_year = tk.StringVar(self)
        self.selected_month = tk.StringVar(self)

        current_year = datetime.now().year
        current_month = datetime.now().month

        self.selected_year.set(current_year)
        self.selected_month.set(current_month)

        self.year_label = tk.Label(self, text="Year:")
        self.year_label.grid(row=1, column=1, sticky='e')
        self.month_label = tk.Label(self, text="Month:")
        self.month_label.grid(row=1, column=3, sticky='e')

        self.year_dropdown = tk.OptionMenu(self, self.selected_year, *range(2022, 2030))
        self.year_dropdown.grid(row=1, column=2)
        self.month_dropdown = tk.OptionMenu(self, self.selected_month, *range(1, 13))
        self.month_dropdown.grid(row=1, column=4)

        self.selected_employee.trace_add('write', self.update_employee_view)
        self.selected_year.trace_add('write', self.update_employee_view)
        self.selected_month.trace_add('write', self.update_employee_view)

        self.calculate_button = tk.Button(self, text="Calculate Paycheck", command=self.calculate_paycheck)
        self.calculate_button.grid(row=2, column=0)

        self.edit_paystub_button = tk.Button(self, text="Edit/Add Paystub", command=self.edit_paystub)
        self.edit_paystub_button.grid(row=3, column=0)


    def update_views(self):
        employees = self.db.get_all_employees()

        menu = self.employee_dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="List of Employees", state="disabled")
        for employee in employees:
            menu.add_command(label=f"{employee.first_name} {employee.last_name}", command=lambda emp=employee: self.selected_employee.set(f"{emp.first_name} {emp.last_name}"))

    def update_employee_view(self, *args):
        selected = self.selected_employee.get()

        if selected == "List of Employees":
            return

        first_name, last_name = selected.split(' ')

        employees = self.db.get_all_employees()
        for employee in employees:
            if employee.first_name == first_name and employee.last_name == last_name:
                self.employee_view.display_employee(employee)
                paystubs = self.db.get_paystubs_by_employee(employee.id, self.selected_year.get(), self.selected_month.get())
                if paystubs:
                    for paystub in paystubs:
                        self.paystub_view.display_paystub(paystub)
                else:
                    self.paystub_view.display_paystub()
                break

    def calculate_paycheck(self):
        selected = self.selected_employee.get()

        if selected == "List of Employees":
            messagebox.showerror("Error", "No employee selected")
            return

        first_name, last_name = selected.split(' ')

        employees = self.db.get_all_employees()
        for employee in employees:
            if employee.first_name == first_name and employee.last_name == last_name:
                paystubs = self.db.get_paystubs_by_employee(employee.id, self.selected_year.get(), self.selected_month.get())
                if paystubs:
                    for paystub in paystubs:

                        base_salary = Decimal(employee.salary)
                        night_bonus = Decimal(0.10)
                        holiday_bonus = Decimal(0.10)
                        night_holiday_bonus = Decimal(0.20)
                    
                        day_hours = paystub.day_hours
                        night_hours = paystub.night_hours
                        holiday_day_hours = paystub.holiday_day_hours
                        holiday_night_hours = paystub.holiday_night_hours

                        year = int(self.selected_year.get())
                        month = int(self.selected_month.get())
                        paycheck = Paycheck(employee, year, month, paystub)
                        paycheck.calculateHours()
                        paycheck.calculateGrossPay()
                        paycheck.calculateDeductions()
                        paycheck.calculateNetPay()

                        paycheck_window = tk.Toplevel(self)
                        paycheck_window.title(f"Paycheck for {first_name} {last_name} - {self.selected_month.get()}/{self.selected_year.get()}")

                        treeview = ttk.Treeview(paycheck_window, columns=("salary component","number", "rate", "total"), show="headings")
                        treeview.heading("salary component", text="Salary component")
                        treeview.heading("number", text="Number")
                        treeview.heading("rate", text="Rate")
                        treeview.heading("total", text="Total")

                        treeview.insert("", "end", values=("Day hours", day_hours, format(base_salary, '.4f'), format(paycheck.day_hours, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Night hours", night_hours, format(base_salary * (1 + night_bonus), '.4f'), format(paycheck.night_hours, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Holiday day hours", holiday_day_hours, format(base_salary * (1 + holiday_bonus), '.4f'), format(paycheck.holiday_day_hours, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Holiday night hours", holiday_night_hours, format(base_salary * (1 + night_holiday_bonus), '.4f'), format(paycheck.holiday_night_hours, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Gross pay", "", "", format(paycheck.gross_pay, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("AVS/AI/APG Contribution", "", "5.3000%", format(-paycheck.avs_ai_apg, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Amat GE Contribution", "", "0.0410%", format(-paycheck.amat_ge, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("AC Contribution", "", "1.1000%", format(-paycheck.ac, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("LAA ANP Contribution", "", "1.3000%", format(-paycheck.laa_anp, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("IJM Contribution", "", "0.7225%", format(-paycheck.ijm, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Withholding tax Day", "", "8.5800%", format(-paycheck.withholding_tax_day, '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Total deductions", "", "", format(-paycheck.getDeductions(), '.2f') + " CHF"))
                        treeview.insert("", "end", values=("Net pay", "", "", format(paycheck.net_pay, '.2f') + " CHF"))

                        lines_to_display = len(treeview.get_children()) + 1

                        treeview.configure(height=lines_to_display)

                        treeview.pack()

                        filename = f"paychecks/{first_name}_{last_name}_{self.selected_month.get()}_{self.selected_year.get()}.pdf"
                        doc = SimpleDocTemplate(filename, pagesize=letter)

                        data = [
                            ["Employee", f"{first_name} {last_name}"],
                            ["Month/Year", f"{self.selected_month.get()}/{self.selected_year.get()}"],
                            ["Day hours", day_hours],
                            ["Night hours", night_hours],
                            ["Holiday day hours", holiday_day_hours],
                            ["Holiday night hours", holiday_night_hours],
                            ["Gross pay", f"{format(paycheck.gross_pay, '.2f')} CHF"],
                            ["Total deductions", f"{format(-paycheck.getDeductions(), '.2f')} CHF"],
                            ["Net pay", f"{format(paycheck.net_pay, '.2f')} CHF"],
                        ]
                        table = Table(data)

                        style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 14),

                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0,0), (-1,-1), 1, colors.black)
                        ])
                        table.setStyle(style)

                        elements = []
                        elements.append(table)
                        doc.build(elements)

                        tk.messagebox.showinfo("PDF Generated", "The paycheck PDF has been generated.")

                else:
                    messagebox.showerror("Error", "No paystubs found for the selected employee in the selected year and month")
                break
    def edit_paystub(self):

        selected = self.selected_employee.get()

        if selected == "List of Employees":
            messagebox.showerror("Error", "No employee selected")
            return

        first_name, last_name = selected.split(' ')

        employees = self.db.get_all_employees()
        for employee in employees:
            if employee.first_name == first_name and employee.last_name == last_name:
                paystubs = self.db.get_paystubs_by_employee(employee.id, self.selected_year.get(), self.selected_month.get())
                if paystubs:

                    self.open_paystub_window(paystubs[0])
                else:

                    self.open_paystub_window()

    def open_paystub_window(self, paystub=None):

        paystub_window = tk.Toplevel(self)

        paystub_view = PayStubView(master=paystub_window, window=paystub_window)

        paystub_view.display_paystub(paystub,True)

        save_button = tk.Button(paystub_window, text="Save", command=lambda: self.save_paystub(paystub_view, paystub))
        save_button.grid(row=8, column=0)

    def save_paystub(self, paystub_view, paystub=None):

        day_hours = paystub_view.entry_day_hours.get()
        night_hours = paystub_view.entry_night_hours.get()
        holiday_day_hours = paystub_view.entry_holiday_day_hours.get()
        holiday_night_hours = paystub_view.entry_holiday_night_hours.get()
        total_hours_worked = paystub_view.entry_total_hours_worked.get()
        number_of_services = paystub_view.entry_number_of_services.get()

        selected = self.selected_employee.get()
        first_name, last_name = selected.split(' ')

        employees = self.db.get_all_employees()
        for employee in employees:
            if employee.first_name == first_name and employee.last_name == last_name:

                if paystub:
                    paystub.day_hours = day_hours
                    paystub.night_hours = night_hours
                    paystub.holiday_day_hours = holiday_day_hours
                    paystub.holiday_night_hours = holiday_night_hours
                    paystub.total_hours_worked = total_hours_worked
                    paystub.number_of_services = number_of_services
                    self.db.update_paystub(paystub)
                else:
                    month_year = f"{self.selected_year.get()}-{self.selected_month.get()}-01"
                    new_paystub = PayStub(None, employee.id, total_hours_worked, day_hours, night_hours, holiday_day_hours, holiday_night_hours, number_of_services, month_year)
                    self.db.add_paystub(new_paystub)
        
        paystub_view.window.destroy()

        paystubs = self.db.get_paystubs_by_employee(employee.id, self.selected_year.get(), self.selected_month.get())
        if paystubs:
            for paystub in paystubs:
                self.paystub_view.display_paystub(paystub)
            