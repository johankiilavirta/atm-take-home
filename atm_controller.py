from atm import ATM
from bank_service import BankService, BankCard

# Container for storing some state information
class Session:
    def __init__(self, state, card_number, pin_number):
        self.state = state
        self.card_number = card_number
        self.card_pin = pin_number
        self.selected_account = None

    def select_account(self, selected_account):
        self.selected_account = selected_account
    
    def get_bank_card(self):
        return BankCard(self.card_number, self.card_pin)

# Controller for the ATM. Errors if we try to transition from a state to another that is not possible
# Directly communicates with the actual ATM and the BankService
# Has states sign-in, waiting-for-pin, signed-in account-selected
# which represent 
#    1. waiting for a new card to be inserted, 
#    2.the card is inserted and waiting for the pin
#    3. the pin and card were validated and waiting to do something to the saving or checking account
#    4. a saving/checking account was picked and a see balance/deposit/withdraw operation could be done
    
class ATM_Controller:
    def __init__(self, bills_in_atm : int, max_bills_in_atm : int):
        self.ATM = ATM(bills_in_atm, max_bills_in_atm)
        self.session = Session("sign-in", None, None)
        self.bank_service = BankService()

    def insert_card(self, card_number):
        self.session = Session("waiting-for-pin", card_number, None)
        return True

    def insert_pin(self, pin_number):
        if self.session.state != "waiting-for-pin":
            raise Exception("Trying to insert pin at wrong stage")
        
        card_number = self.session.card_number
        bank_card = self.session.get_bank_card()
        if not self.bank_service.card_is_verified(bank_card):
            return False

        self.session = Session("signed-in", card_number, pin_number)
        return True
    
    def select_account(self, selected_account: str):
        if self.session.state not in ["signed-in", "account-selected"]:
            raise Exception("Trying to select a saving/checking account at wrong stage")
        
        bank_card = self.session.get_bank_card()

        if self.bank_service.has_sub_account(bank_card, selected_account):
            self.session.select_account(selected_account)
            self.session.state = "account-selected"
        else:
            self.session.select_account(None)
            
    def get_balance(self):
        if self.session.state != "account-selected":
            raise Exception("Trying to get balance when no account selected")
        
        bank_card = self.session.get_bank_card()
        selected_account = self.session.selected_account
        return self.bank_service.get_account_balance(bank_card, selected_account)
        
    def withdraw(self, withdrawal_amount):
        if self.session.state != "account-selected":
            raise Exception("Trying to withdraw when no account selected")
        
        bank_card = self.session.get_bank_card()
        selected_account = self.session.selected_account
        return self.bank_service.withdraw(self.ATM, bank_card, selected_account, withdrawal_amount)
    
    def deposit(self, deposit_amount):
        if self.session.state != "account-selected":
            raise Exception("Trying to deposit when no account selected")
        
        bank_card = self.session.get_bank_card()
        selected_account = self.session.selected_account
        return self.bank_service.deposit(self.ATM, bank_card, selected_account, deposit_amount)
        
    def logout(self):
        self.session = Session("sign-in", None, None)

        



