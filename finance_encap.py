class FinanceEncap:
    def __init__(self, income, otheramt, tax, otherexp, dtofent, comment):
        self.income = income
        self.otheramt = otheramt
        self.tax = tax
        self.otherexp = otherexp
        self.dtofent = dtofent
        self.comment = comment

    #setter methods
    def set_income(self, income):
        self._income = income

    def set_otheramt(self, otheramt):
        self._otheramt = otheramt

    def set_tax(self, tax):
        self._tax = tax

    def set_otherexp(self, otherexp):
        self._otherexp = otherexp

    def set_dtofent(self, dtofent):
        self._dtofent = dtofent

    def set_comment(self, comment):
        self._comment = comment


    #getter methods
    def get_income(self):
        return self._income

    def get_otheramt(self):
        return self._otheramt

    def get_tax(self):
        return self._tax

    def get_otherexp(self):
        return self._otherexp

    def get_dtofent(self):
        return self._dtofent

    def get_comment(self):
        return self._comment