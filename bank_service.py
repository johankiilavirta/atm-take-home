from atm import ATM
"""
    TODO: For the BankService methods need to query the real bank API to make transactions and verify card# and pin#
    TODO: Using bankAccounts as a global dictionary to simulate a database. 
          The design reason for this is because it didnt really feel right to make a new empty dictionary "database"
          for each new instance of BankService. I think that should be handled seperately and this leaves it at a better
          starting point (rather than reworking a lot of BankService.)
          
"""
bankAccounts = dict()

# Little container for bank card # and pin # with eq and hash methods defined so that it can hash into the bankAccounts dictionary properly
class BankCard:
    def __init__(self, card_number: int, card_pin: int):
        self.card_number = card_number
        self.card_pin = card_pin

    def __eq__(self, object: object) -> bool:
        return isinstance(object, BankCard) and self.card_number == object.card_number and self.card_pin == object.card_pin
    
    def __hash__(self):
        return hash((self.card_number, self.card_pin))

# Kind of simulating how wed actually call the bank API that stores data of customers
class BankService:
    # TODO: Need to query another service to make sure the bank account exists, for now assume all do
    def card_is_verified(self, bank_card: BankCard) -> None:
        return True

    # Create and get methods for getting bank account data
    def create_account(self, bank_card: BankCard):
        accounts = dict([("checking", 0), ("savings", 0)])
        bankAccounts[bank_card] = accounts

        return True

    def get_account(self, bank_card : BankCard):
        if bank_card not in bankAccounts:
            self.create_account(bank_card)

        return bankAccounts[bank_card]

    # If currently logged in to a bank account checks if a sub-account like "savings" or "checking" exist
    def has_sub_account(self, bank_card: BankCard, account_name: str):
        account = self.get_account(bank_card)
        return account_name in account
    
    # Get their actual bank account balance for the given sub-account
    def get_account_balance(self, bank_card: BankCard, account_name : str):
        account = self.get_account(bank_card)
        return account[account_name]

    # Checks if the person actually has funds stored on the actual bank database
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

    # Simulates withdrawing on the bank database
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
    
    # Checks that the account exists, a bit redundant but might be useful in the future
    def can_deposit(self, ATM : ATM, 
                   bank_card: BankCard, account_name : str) -> bool:
        account = self.get_account(bank_card)
        return account_name in account
    
    # Simulates depositting the money on the bank database
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