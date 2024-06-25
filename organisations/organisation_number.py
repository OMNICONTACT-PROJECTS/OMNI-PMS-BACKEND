import random
import string

def generate_organisation_number(organisation_identifier, db_number, sequence_number_length, alphanumeric_length):
    sequential_number = str(random.randint(1, 10 ** sequence_number_length)).zfill(sequence_number_length)

    alphanumeric_code = ''.join(
    random.choices(string.ascii_uppercase + string.digits, k=alphanumeric_length))
    organisation_number = f"{organisation_identifier}{db_number}-{sequential_number}-{alphanumeric_code}"

    return organisation_number