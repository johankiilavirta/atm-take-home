from atm_controller import ATM_Controller
TEST_CARD_1 = "0000-0000-0000-0000"
TEST_PIN_1 = "0000"


def withdraw_from_empty_atm(controller : ATM_Controller):
    controller.insert_card(TEST_CARD_1)
    controller.insert_pin(TEST_PIN_1)
    controller.select_account("savings")

    try:
        controller.withdraw(1)
    except:
        return True
    
    return False

results = []
results.append(withdraw_from_empty_atm(ATM_Controller(0, 100)))
    
print(results)
