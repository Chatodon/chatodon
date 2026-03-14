from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r"^[a-z](?:[a-z0-9]|_(?!_)){3,30}[a-z0-9]$",
    message=(
        "Username must be 5–32 characters long, start with a letter, "
        "contain only lowercase latin letters, numbers and single underscores, "
        "and end with a letter or number."
    ),
)
