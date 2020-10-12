from loan_calculator import Payer
import json
if __name__ == '__main__':
    with open ('./example.json', 'r') as f:
        data = json.load(f)
        
    payer = Payer(**data)
    payer.calculate()
    payer.writeLog('example.tab')