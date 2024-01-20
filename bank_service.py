from atm import ATM
"""
    TODO: Need to query real data
"""
bankAccounts = dict()

class BankCard:
    def __init__(self, card_number: int, card_pin: int):
        self.card_number = card_number
        self.card_pin = card_pin

    def __eq__(self, object: object) -> bool:
        return isinstance(object, BankCard) and self.card_number == object.card_number and self.card_pin == object.card_pin
    
    def __hash__(self):
        return hash((self.card_number, self.card_pin))

class BankService:
    def card_is_verified(self, bank_card: BankCard) -> None:
        return True

    def create_account(self, bank_card: BankCard):
        accounts = dict([("checking", 0), ("savings", 0)])
        bankAccounts[bank_card] = accounts

        return True

    def get_account(self, bank_card : BankCard):
        if bank_card not in bankAccounts:
            #print("creating new account for", bank_card.card_number, bank_card.card_pin)
            self.create_account(bank_card)

        return bankAccounts[bank_card]

    def has_sub_account(self, bank_card: BankCard, account_name: str):
        account = self.get_account(bank_card)
        return account_name in account
    
    def get_account_balance(self, bank_card: BankCard, account_name : str):
        account = self.get_account(bank_card)
        return account[account_name]

    def can_withdraw(self, ATM : ATM, 
                bank_card: BankCard, account_name : str, 
                withdrawal_amount: int) -> bool:
        account = self.get_account(bank_card)
        if account_name not in account:
            return False
        
        account_balance = account[account_name]
        if 0 < withdrawal_amount <= account_balance:
            return True
    
        return False

    def withdraw(self, ATM : ATM, 
                 bank_card: BankCard, account_name : str, 
                 withdrawal_amount: int) -> bool:
        if not ATM.can_withdraw(withdrawal_amount) or \
                not self.can_withdraw(ATM, bank_card, account_name, withdrawal_amount):
            return False
        
        account = self.get_account(bank_card)
        account[account_name] -= withdrawal_amount
        ATM.withdraw(withdrawal_amount)
        return True        
    
    
    def can_deposit(self, ATM : ATM, 
                   bank_card: BankCard, account_name : str) -> bool:
        account = self.get_account(bank_card)
        return account_name in account

    def deposit(self, ATM : ATM, 
                bank_card: BankCard, account_name : str, 
                deposit_amount: int) -> bool:
        
        if not ATM.can_deposit(deposit_amount) or \
            not self.can_deposit(ATM, bank_card, account_name):
            return False
        

        account = self.get_account(bank_card)
        account[account_name] += deposit_amount
        ATM.deposit(deposit_amount)
        return True   


