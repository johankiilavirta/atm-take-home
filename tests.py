from atm_controller import ATM_Controller

class ATM_RESULT:
    def __init__(self, card_number, pin, state, current_cash, max_bills, checking_balance, savings_balance):
        self.card_number = card_number
        self.pin = pin
        self.state = state
        self.current_cash = current_cash
        self.max_bills = max_bills
        self.checking_balance = checking_balance
        self.savings_balance = savings_balance

    def __str__(self) -> str:
        return str((self.card_number, self.pin, self.state, self.current_cash, "/", self.max_bills, "savings:", self.checking_balance, "checking:", self.savings_balance))

# Helper functions for visual debugging
def get_atm_status(controller: ATM_Controller):
    controller_account = controller.session.selected_account
    controller.select_account("savings")
    savings_balance = controller.get_balance()
    controller.select_account("checking")
    checking_balance = controller.get_balance()
    controller.session.selected_account = controller_account

    return ATM_RESULT(
        controller.session.card_number,
        controller.session.card_pin,
        controller.session.state,
        controller.ATM.available_cash, controller.ATM.max_bills,
        savings_balance, checking_balance
    )

def print_atm_status(controller: ATM_Controller):
    print(get_atm_status(controller))

# Helper function to logout, and relogin for a new card number and test pin
def quick_initialization(controller: ATM_Controller, card_number):
    controller.insert_card(card_number)
    controller.insert_pin(0)
    controller.select_account("savings")

# Tests a simple deposit
def make_valid_deposit(controller: ATM_Controller):
    quick_initialization(controller, 0)

    controller.deposit(1)

    if controller.ATM.available_cash != 1 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully")

# Tests multiple deposits for one user
def make_repeated_deposits(controller: ATM_Controller):
    quick_initialization(controller, 1)

    total = 0
    for i in range(6):
        controller.deposit(i)
        total += i
        if controller.ATM.available_cash != total or controller.get_balance() != total:
            raise Exception("Was not able to deposit successfully")

# Tests withdrawal from an empty ATM
def withdraw_from_empty_atm(controller : ATM_Controller):
    quick_initialization(controller, 2)

    controller.withdraw(1)
    if controller.ATM.available_cash != 0 or controller.get_balance() != 0:
        raise Exception("Was able to withdraw from empty ATM")

# Tests deposits in savings and checking for one user
def deposit_in_savings_and_checking(controller: ATM_Controller):
    quick_initialization(controller, 3)

    controller.deposit(1)

    if controller.ATM.available_cash != 1 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully")

    controller.select_account("checking")
    if controller.ATM.available_cash != 1 or controller.get_balance() != 0:
        raise Exception("Was not able to deposit successfully")
    
    controller.deposit(50)
    if controller.ATM.available_cash != 51 or controller.get_balance() != 50:
        raise Exception("Was not able to deposit successfully")
    
    controller.select_account("savings")
    if controller.ATM.available_cash != 51 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully")

# Tests deposits across multiple users
def different_users_depositing(controller: ATM_Controller):
    quick_initialization(controller, 4)

    controller.deposit(1)

    if controller.ATM.available_cash != 1 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully")
    
    quick_initialization(controller, 5)

    controller.deposit(10)
    if controller.ATM.available_cash != 11 or controller.get_balance() != 10:
        raise Exception("Was not able to deposit successfully on a new account")

    quick_initialization(controller, 4)

    if controller.ATM.available_cash != 11 or controller.get_balance() != 1:
        raise Exception("Was not able to deposit successfully for original account after more accounts appeared")
    
# More comprehensive test of deposits, withdrawals, edge cases for one user
def valid_deposits_and_withdrawals(controller: ATM_Controller):
    quick_initialization(controller, 6)
    controller.deposit(5)
    controller.withdraw(10) # Should not be able to withdraw 10 because not enough money in ATM
    controller.deposit(50)
    controller.withdraw(3)
    controller.withdraw(7)
    controller.deposit(1000) # Would overflow the ATM, do not accept it
    if controller.ATM.available_cash != 45 or controller.get_balance() != 45:
        raise Exception("Was not able to complete a busy transaction successfully")

# Tests to make sure we can't overflow the ATM
def test_machine_storage_cap(controller: ATM_Controller):
    quick_initialization(controller, 7)
    controller.deposit(10)
    if controller.ATM.available_cash != 10 or controller.get_balance() != 10:
        raise Exception("Was not able to deposit successfully")
    
    controller.deposit(1)
    if controller.ATM.available_cash != 10 or controller.get_balance() != 10:
        raise Exception("Deposited when should not have been able to deposit")

# More comprehensive test following the suggested flow with a lot of operations over multiple accounts/deposits/withdrawls
def test_many_accounts_deposit_and_withdraw(controller: ATM_Controller):
    current_deposit = [0, 1, 1, 2, 3, 5, 8, 13] #include all but the 13
    for i in range(8, 16):
        quick_initialization(controller, i)
        controller.deposit(current_deposit[i - 8])

    expected_balances = [0, 1, 1, 2, 3, 5, 8, 0]
    for i in range(8, 16):
        quick_initialization(controller, i)
        if controller.get_balance() != expected_balances[i - 8]:
            raise Exception("Was not able to deposit successfully across many accounts")
    
    controller.logout()
    quick_initialization(controller, 14)
    controller.withdraw(7)
    expected_balances = [0, 1, 1, 2, 3, 5, 1, 0]
    for i in range(8, 16):
        quick_initialization(controller, i)
        if controller.get_balance() != expected_balances[i - 8]:
            raise Exception("Was not able to deposit successfully across many accounts")

    for i in range(8, 16):
        controller.logout()
        controller.insert_card(i)
        controller.insert_pin(0)
        controller.select_account("checking")
        if controller.get_balance() != 0:
            raise Exception("Got nonzero checking account balance")
        controller.deposit(1)

    expected_balances = [1, 1, 1, 1, 1, 1, 1, 0]
    for i in range(8, 16):
        controller.logout()
        controller.insert_card(i)
        controller.insert_pin(0)
        controller.select_account("checking")
        if controller.get_balance() != expected_balances[i - 8]:
            raise Exception("Was not able to deposit successfully across many accounts")

    expected_balances = [0, 1, 1, 2, 3, 5, 1, 0]
    for i in range(8, 16):
        quick_initialization(controller, i)
        if controller.get_balance() != expected_balances[i - 8]:
            raise Exception("Was not able to deposit successfully across many accounts")


        
# Run simple test cases, will raise an exception if it fails
make_valid_deposit(ATM_Controller(0, 100))
make_repeated_deposits(ATM_Controller(0, 100))
withdraw_from_empty_atm(ATM_Controller(0, 100))
deposit_in_savings_and_checking(ATM_Controller(0, 100))
different_users_depositing(ATM_Controller(0, 100))
valid_deposits_and_withdrawals(ATM_Controller(0, 100))
test_machine_storage_cap(ATM_Controller(0, 10))
test_many_accounts_deposit_and_withdraw(ATM_Controller(0, 20))
