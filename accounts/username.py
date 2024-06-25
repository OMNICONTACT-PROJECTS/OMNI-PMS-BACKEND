from organisations.models import Organisation
from .models import User
from string import ascii_uppercase, digits
from random import randint, choice
from datetime import datetime


def get_username(instance):
    if instance.organisation_id is None:
        first_name = instance.first_name.upper()
        last_name = instance.last_name.upper()
        role = "DEV"
        user_id = str(instance.id)
        random_numbers = "".join(choice(digits) for _ in range(2))
        username = f"{first_name}.{last_name}-{user_id}{random_numbers}{role}"
    else:
        first_name = instance.first_name.upper()
        last_name = instance.last_name.upper()
        role = instance.role[:3].upper()
        user_id = str(instance.id)
        random_numbers = "".join(choice(digits) for _ in range(2))
        username = f"{first_name}.{last_name}-{user_id}{random_numbers}{role}"

    return username
