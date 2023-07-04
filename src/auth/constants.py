class AdditionalClaims:
    """
    Constants to indicate the type of action to perform (password reset, activate account)
    """

    RESET_PASSWORD = {
        "name": "reset_password",
        "description": "claim to indicate reset password",
    }
    
    ACTIVATE_ACCOUNT_PASSWORD = {
        "name": "activate_account_password",
        "description": "claim to indicate activate account with password",
    }
