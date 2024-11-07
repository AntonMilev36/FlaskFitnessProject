import re
from marshmallow import ValidationError
from password_strength import PasswordPolicy

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

password_requirements = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1,
    nonletters=1,
)

def validate_email(value):
    if not re.match(EMAIL_REGEX, value):
        raise ValidationError("Invalid email format.")

def password_validator(value):
    errors = password_requirements.test(value)
    if errors:
        raise ValidationError("Password is not strong enough, try another one")

def validate_name(value):
    try:
        first_name, last_name = value.split()
    except ValueError:
        raise ValidationError("Need to write first and last name")
    else:
        if len(first_name) < 2 and len(last_name) < 2:
            raise ValidationError("Both names need to be at least 2 characters")
        elif len(first_name) < 2:
            raise ValidationError("First name need to be at least 2 characters")
        elif len(last_name) < 2:
            raise ValidationError("Last name need to be at least 2 characters")
        elif len(first_name) > 100 and len(last_name) > 100:
            raise ValidationError("Both names need to be less than a 100 characters")
        elif len(first_name) > 100:
            raise ValidationError("First name need to be less than a 100 characters")
        elif len(last_name) > 100:
            raise ValidationError("Last name need to be less than a 100 characters")
