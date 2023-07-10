class Role:
    """
    Constants for the various roles scoped in the application ecosystem
    """

    READ = {
        "name": "read",
        "description": "read-only access",
    }

    ADMIN = {
        "name": "admin",
        "description": "admin has all permissions",
    }

    EMAIL = {
        "name": "email",
        "description": "email-related functionalities",
    }

    USER = {
        "name": "user",
        "description": "user-specific data or resources",
    }
