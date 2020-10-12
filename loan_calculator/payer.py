from .timeline import Timeline
from .loan import Loan

class Payer:
    def __init__(self, start_date, max_monthly_payment, loans, beginning_lump_sum=0.0):
        self.maxPayment = max_monthly_payment
        self.activeLoans = {elem['ID']: Loan(**elem) for elem in loans}
        self.totalBalance = self.getTotalBalance()
        self.timeline = Timeline(start_date, self.activeLoans)
        self.lumpSum = beginning_lump_sum
        self.totalPaid = 0.0
    
    def writeLog(self, fname):
        self.timeline.outputEventLog(fname)
    
    def getTotalBalance(self):
        return sum([loan.owed for loan in self.activeLoans.values()])
    
    def getMinimumPayment(self):
        return sum([loan.getMinimumPayment(self.timeline.date) for loan in self.activeLoans.values()])

    def advanceDate(self):
        print(f'For month {self.timeline.date.strftime("%B %Y")}:')
        print(f'Starting balance: ${self.getTotalBalance():,.2f}')
        self.accumulateInterest()
        self.payOff()
        print(f'Ending balance: ${self.getTotalBalance():,.2f}. Total Paid: ${self.totalPaid:,.2f}')
        self.timeline.advanceDate()
    
    def accumulateInterest(self):
        for loan in self.activeLoans.values():
            loan.accumulateInterest()

    def calculateOptimalPaymentAmounts(self):
        return self._calculateOptimalPaymentAmounts(self.maxPayment)        
    
    def _calculateOptimalPaymentAmounts(self, availableAmount):
        minimumPaymentAmount = self.getMinimumPayment()
        leftover = availableAmount - minimumPaymentAmount
        payments = {loan.id:loan.getMinimumPayment(self.timeline.date) for loan in self.activeLoans.values()}
        idsInOrderOfInterest = sorted(list(self.activeLoans.keys()),key= lambda x: self.activeLoans[x].annualInterest*-1)
        for loan in idsInOrderOfInterest:
            refund = self.activeLoans[loan].calculatePayoffRefundAmount(leftover)
            payments[loan] = leftover - refund
            leftover = refund
            if not leftover:
                break
        return payments
    
    def _payOff(self, paymentAmounts):
        self.timeline.addEvent(self.timeline.date, paymentAmounts)
        for k, v in paymentAmounts.items():
            if v:
                print(f'Making ${v:,.2f} payment on loan ID #{k}')
            self.activeLoans[k].payOffAmount(v)
            self.totalPaid += v

    def payOff(self):
        optimalPaymentAmounts = self.calculateOptimalPaymentAmounts()
        self._payOff(optimalPaymentAmounts)
        
    
    def payOffLumpSum(self):
        payoffAmounts = self._calculateOptimalPaymentAmounts(self.maxPayment+self.lumpSum)
        self._payOff(payoffAmounts)
        self.lumpSum = 0.0

    
    def calculate(self):
        month = 0
        while self.getTotalBalance()>0.0001:
            if month == 0:
                self.payOffLumpSum()
            else:
                self.advanceDate()
            month += 1
        
            
        
    
    
    