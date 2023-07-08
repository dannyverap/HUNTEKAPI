class AdditionalClaims:
    """
    Constants to indicate the type of action to perform (password reset, activate account)
    """

    ACCOUNT_ACTIVATION_ADMIN = {
        "name": "activate_account_admin",
        "description": "claim to indicate activate account for the admin",
    }

    ACCOUNT_ACTIVATION_USER = {
        "name": "activate_account_user",
        "description": "claim to indicate activate account for the user",
    }
