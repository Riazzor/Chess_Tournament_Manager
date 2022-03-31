import re
import functools
from database.database import PlayerDB, databases

from database.database import TournamentDB
from database.serializer import PlayerSerializer, TournamentSerializer


def table_factory(table: str):
    player_serializer = PlayerSerializer()
    player_database = PlayerDB(databases['player_database'], player_serializer)
    if table == 'tournaments':
        tournament_serializer = TournamentSerializer()
        return TournamentDB(databases, tournament_serializer, player_database)
    elif table == 'players':
        return player_database
    raise ValueError(f'{table} is not a valid value')


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


def is_positive_number(input_number: str) -> bool:
    if not input_number.isdigit():
        return False
    if int(input_number) <= 0:
        return False
    return True


def sub_menu(func):
    """
    Decorator for menu functions. Allows navigation back
    to previous menu.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        quit = False
        while not quit:
            choice = func(*args, **kwargs)
            if choice == 'q':
                quit = True
        return choice
    return wrapper


def menu_title(title: str):
    """
    Decorator for the title of each menu.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('=' * 50)
            print(title.upper().center(50))
            print('=' * 50)
            return func(*args, **kwargs)

        return wrapper
    return decorator
