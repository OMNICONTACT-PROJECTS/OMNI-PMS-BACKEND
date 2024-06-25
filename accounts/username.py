from organisation.models import Organisation
from .models import User
from string import ascii_uppercase
from random import randint
from datetime import datetime


def get_username(organisation=None):
    while True:
        first_random_letter = ascii_uppercase[randint(0, len(ascii_uppercase) - 1)]
        year = str(datetime.now().year)[2:]
        last_random_letter = ascii_uppercase[randint(0, len(ascii_uppercase) - 1)]
        a = randint(0, 9)
        b = randint(0, 9)
        c = randint(0, 9)
        d = randint(0, 9)

        random_number = f'{a}{b}{c}{d}{d}'

        if organisation is None:
            username = f'{first_random_letter}{year}{random_number}{last_random_letter}-SU'
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            else:
                continue
        else:
            current_organisation = organisation.objects.get(pk=organisation)
            username = f'{current_organisation.organisation_code}{year}{random_number}{last_random_letter}'
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            else:
                continue






