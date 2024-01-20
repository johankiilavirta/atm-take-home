class ATM:
    def __init__(self, available_cash = 0, max_bills = 100):
        self.available_cash = available_cash
        self.max_bills = max_bills

    def can_withdraw(self, cash):
        return 0 < cash <= self.available_cash
    
    def withdraw(self, withdrawal_amount):
        self.available_cash -= withdrawal_amount

    def can_deposit(self, deposit_amount: int):
        return self.available_cash + deposit_amount <= self.max_bills
    
    def deposit(self, deposit_amount):
        self.available_cash += deposit_amount