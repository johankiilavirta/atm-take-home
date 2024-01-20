import sys
from atm_controller import ATM_Controller
TEST_PIN_1 = "0000"

class ATM_RESULT:
    def __init__(self, state, current_cash, max_bills, checking_balance, savings_balance):
        self.state = state
        self.current_cash = current_cash
        self.max_bills = max_bills
        self.checking_balance = checking_balance
        self.savings_balance = savings_balance

    def __str__(self) -> str:
        return str((self.state, self.current_cash, "/", self.max_bills, "savings:", self.checking_balance, "checking:", self.savings_balance))


def get_atm_status(controller: ATM_Controller):
    controller_account = controller.session.selected_account
    controller.select_account("savings")
    savings_balance = controller.get_balance()
    controller.select_account("checking")
    checking_balance = controller.get_balance()
    controller.session.selected_account = controller_account

    return ATM_RESULT(
        controller.session.state,
        controller.ATM.available_cash, controller.ATM.max_bills,
        savings_balance, checking_balance
    )

def print_atm_status(controller: ATM_Controller):
    print(get_atm_status(controller))

def quick_initialization(controller: ATM_Controller, card_number):
    controller.insert_card(card_number)
    controller.insert_pin("test_pin")
    controller.select_account("savings")

def make_valid_deposit(controller: ATM_Controller):
    quick_initialization(controller, 0)

    controller.deposit(1)

    if controller.ATM.available_cash != 1 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully")

def make_repeated_deposits(controller: ATM_Controller):
    quick_initialization(controller, 1)

    total = 0
    for i in range(6):
        controller.deposit(i)
        total += i
        if controller.ATM.available_cash != total or controller.get_balance() != total:
            raise Exception("Was not able to deposit successfully")
        
def withdraw_from_empty_atm(controller : ATM_Controller):
    quick_initialization(controller, 2)

    controller.withdraw(1)
    if controller.ATM.available_cash != 0 or controller.get_balance() != 0:
        raise Exception("Was able to withdraw from empty ATM")

def deposit_in_savings_and_checking(controller: ATM_Controller):
    quick_initialization(controller, 2)

    controller.deposit(1)

    if controller.ATM.available_cash != 1 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully")

    controller.select_account()
    print_atm_status(controller)



make_valid_deposit(ATM_Controller(0, 100))
make_repeated_deposits(ATM_Controller(0, 100))
withdraw_from_empty_atm(ATM_Controller(0, 100))
