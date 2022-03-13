import re
import functools
from database.database import PlayerDB, database

from database.database import TournamentDB
from database.serializer import PlayerSerializer, TournamentSerializer


def table_factory(table: str):
    if table == 'tournaments':
        tournament_serializer = TournamentSerializer()
        return TournamentDB(database, tournament_serializer)
    elif table == 'players':
        player_serializer = PlayerSerializer()
        return PlayerDB(database, player_serializer)
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
    return wrapper


def menu_title(title: str):
    def decorator(func):
        """
        Decorator for the title of each menu.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('=' * 30)
            print(title.upper().center(30))
            print('=' * 30)
            return func(*args, **kwargs)

        return wrapper
    return decorator
