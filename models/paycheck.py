from datetime import datetime
from decimal import Decimal

class Paycheck:
    def __init__(self, employee, year, month, paystub):
        self.employee = employee
        self.date = datetime(year, month, 1)
        self.paystub = paystub
        self.day_hours = None
        self.night_hours = None
        self.holiday_day_hours = None
        self.holiday_night_hours = None
        self.gross_pay = None
        self.avs_ai_apg = None
        self.amat_ge = None
        self.ac = None
        self.laa_anp = None
        self.ijm = None
        self.withholding_tax_day = None
        self.net_pay = None

    def calculateHours(self):
        self.day_hours = self.paystub.day_hours * self.employee.salary
        self.night_hours = self.paystub.night_hours * ( self.employee.salary * Decimal(1.10))
        self.holiday_day_hours = self.paystub.holiday_day_hours * (self.employee.salary * Decimal(1.10))
        self.holiday_night_hours = self.paystub.holiday_night_hours * (self.employee.salary * Decimal(1.20))

    def calculateGrossPay(self):
        self.gross_pay = self.day_hours + self.night_hours + self.holiday_day_hours + self.holiday_night_hours


    def calculateDeductions(self):
        self.avs_ai_apg = self.gross_pay * Decimal(0.053)
        self.amat_ge = self.gross_pay * Decimal(0.00041)
        self.ac = self.gross_pay * Decimal(0.011)
        self.laa_anp = self.gross_pay * Decimal(0.013)
        self.ijm = self.gross_pay * Decimal(0.007225)
        self.withholding_tax_day = self.gross_pay * Decimal(0.0858)

    def getDeductions(self):
        return self.avs_ai_apg + self.amat_ge + self.ac + self.laa_anp + self.ijm + self.withholding_tax_day
    
    def calculateNetPay(self):
        self.net_pay = self.gross_pay - self.getDeductions()