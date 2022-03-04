import re


def is_date_format(input_date) -> bool:
    """
    This function check that the input is a date so we
    can use datetime on the input.
    """
    date_pattern = re.compile(r'^(\d{2})\/(\d{2})\/(\d{4})$')

    good_date = date_pattern.fullmatch(input_date)
    if good_date:
        day, month, year = [int(group) for group in good_date.groups()]
        if 0 < day < 32 and 0 < month < 13 and 1900 < year < 2025:
            return True
    return False
