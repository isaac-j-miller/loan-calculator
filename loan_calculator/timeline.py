import datetime as dt
from dateutil.relativedelta import relativedelta

INCREMENT_DEFAULT = relativedelta(months=1)

class Timeline:
    def __init__(self, start_date, initialLoans, increment=INCREMENT_DEFAULT):
        self.date = dt.date.fromisoformat(start_date)
        self.increment = increment
        self.events = dict()
        self.initialLoans = initialLoans
    
    def advanceDate(self):
        self.date += self.increment
    
    def addEvent(self,date,payoffAmount):
        self.events[date] = payoffAmount
    
    def getEventString(self,date):
        stringList = [f'{date.strftime("%B %Y")}', *[f'${v:,.2f}' for v in self.events[date].values()]]
        return '\t'.join(stringList)
    
    def outputEventLog(self, fname):
        headerString = ['Month', *[f'{v.provider} #{v.id}' for v in self.initialLoans.values()]]
        eventStrings = [self.getEventString(date) for date in self.events.keys()]
        data = '\t'.join(headerString) + '\n' + '\n'.join(eventStrings)
        with open(fname, 'w') as f:
            f.write(data)