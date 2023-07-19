class Order:
    """
    Constants for the orders in the tokens table
    """

    ACCOUNT_ACTIVATION = {
        "name": "account_activation",
        "description": "code for the activation of the user",
    }

    RESET_PASSWORD = {
        "name": "reset_password",
        "description": "code for the reset password of the user",
    }


    
    VAlLID_ORDER_NAMES =[ACCOUNT_ACTIVATION["name"], RESET_PASSWORD["name"]]
   