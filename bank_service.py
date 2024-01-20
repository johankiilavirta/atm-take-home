from atm import ATM

"""
    TODO: Need to query real data
"""
bankAccounts = dict()

class BankService:
    def cardIsVerified(self, card_number : str, pin :str) -> None:
        return True

    def createAccount(self, account_id: tuple(int, int)) -> bool:
        accounts = dict(("checking", 0), ("savings", 0))
        bankAccounts[account_id] = accounts

        return True

    def getAccount(self, card_number : str, pin : str) -> None:
        account_id = (card_number, pin)
        if account_id not in bankAccounts:
            self.createAccount(account_id)

        return bankAccounts[account_id]

    def hasSubAccount(self, card_number, pin, account_name: str):
        account = self.getAccount(card_number, pin)
        return account_name in account

    def canWithdraw(self, ATM : ATM, 
                account_id: tuple(int, int), account_name : str, 
                withdrawal_amount: int) -> bool:
        account = self.getAccount(account_id)
        if account_name not in account:
            return False
        
        account_balance = account[account_name]
        if 0 < withdrawal_amount <= account_balance:
            return True
    
        return False
         

    def withdraw(self, ATM : ATM, 
                 account_id: tuple(int, int), account_name : str, 
                 withdrawal_amount: int) -> bool:
        if not ATM.canWithdraw(withdrawal_amount) or \
                not self.canWithdraw(ATM, account_id, account_name, withdrawal_amount):
            return False
        
        account = self.getAccount(account_id)
        account[account_name] -= withdrawal_amount
        return True        
    
    
    def canDeposit(self, ATM : ATM, 
                   account_id: tuple(int, int), account_name : str) -> bool:
        account = self.getAccount(account_id)
        return account_name in account
         

    def deposit(self, ATM : ATM, 
                account_id: tuple(int, int), account_name : str, 
                deposit_amount: int) -> bool:
        if not ATM.canDeposit(ATM, account_id, account_name) and \
            self.canDeposit(ATM, account_id, account_name):
            return False
        
        account = self.getAccount(account_id)
        account[account_name] += deposit_amount
        return True   


