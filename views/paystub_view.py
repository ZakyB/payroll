import tkinter as tk

class PayStubView(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid()

        self.lbl_employee_id = tk.Label(self, text="Employee ID: ")
        self.lbl_employee_id.grid(row=1, column=0)

        self.lbl_total_hours_worked = tk.Label(self, text="Total Hours Worked: ")
        self.lbl_total_hours_worked.grid(row=2, column=0)

        self.lbl_day_hours = tk.Label(self, text="Day Hours: ")
        self.lbl_day_hours.grid(row=3, column=0)

        self.lbl_night_hours = tk.Label(self, text="Night Hours: ")
        self.lbl_night_hours.grid(row=4, column=0)

        self.lbl_holiday_day_hours = tk.Label(self, text="Holiday Day Hours: ")
        self.lbl_holiday_day_hours.grid(row=5, column=0)

        self.lbl_holiday_night_hours = tk.Label(self, text="Holiday Night Hours: ")
        self.lbl_holiday_night_hours.grid(row=6, column=0)

        self.lbl_number_of_services = tk.Label(self, text="Number of Services: ")
        self.lbl_number_of_services.grid(row=7, column=0)

    def display_paystub(self, paystub=None):
        if paystub is None:
            self.lbl_employee_id['text'] = "Employee ID: N/A"
            self.lbl_total_hours_worked['text'] = "Total Hours Worked: N/A"
            self.lbl_day_hours['text'] = "Day Hours: N/A"
            self.lbl_night_hours['text'] = "Night Hours: N/A"
            self.lbl_holiday_day_hours['text'] = "Holiday Day Hours: N/A"
            self.lbl_holiday_night_hours['text'] = "Holiday Night Hours: N/A"
            self.lbl_number_of_services['text'] = "Number of Services: N/A"
        else:
            self.lbl_employee_id['text'] = f"Employee ID: {paystub.employee_id}"
            self.lbl_total_hours_worked['text'] = f"Total Hours Worked: {paystub.total_hours_worked}"
            self.lbl_day_hours['text'] = f"Day Hours: {paystub.day_hours}"
            self.lbl_night_hours['text'] = f"Night Hours: {paystub.night_hours}"
            self.lbl_holiday_day_hours['text'] = f"Holiday Day Hours: {paystub.holiday_day_hours}"
            self.lbl_holiday_night_hours['text'] = f"Holiday Night Hours: {paystub.holiday_night_hours}"
            self.lbl_number_of_services['text'] = f"Number of Services: {paystub.number_of_services}"