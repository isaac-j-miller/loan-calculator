import datetime as dt

class Loan:
    def __init__(self, owed, interest, ID, start, provider, **kwargs):
        self.owed = owed
        self.annualInterest = interest
        self.monthlyInterest = interest / 12
        self.id = ID
        self.term = 144
        self.start = dt.date.fromisoformat(start)
        self.provider = provider
        for k,v in kwargs.items():
            self.__setattr__(k,v)
    
    def setPeriod(self, term):
        self.term = term
    
    def getMonthlyPaymentAmount(self):
        d = (((1+self.monthlyInterest)*self.term)-1)/(self.monthlyInterest*self.term*(1+self.monthlyInterest))
        return self.owed/d
    
    def getMinimumPayment(self, today):
        if today >= self.start:
            return self.getMonthlyPaymentAmount()
        else:
            return 0.0
    
    def payOffAmount(self, amount):
        self.owed -= amount
        if self.owed <= 0.0:
            refund = self.owed * -1
            self.owed = 0.0
        else:
            refund = 0.0
        return refund
    
    def calculatePayoffRefundAmount(self, amount):
        owed = self.owed
        owed -= amount
        if owed <= 0.0:
            refund = owed * -1
        else:
            refund = 0.0
        return refund
    
    def accumulateInterest(self):
        self.owed *= (1+self.monthlyInterest)
    
