import os

from tinydb import TinyDB

DB_FILE = "database.json"
DIRECTORY = "./database"


class Database:
    """
    The database Model.
    Creates and saves a new database director and
    file if they don't exist already.
    """
    def __init__(self):
        """Database constructor"""
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        self.database = TinyDB(f"{DIRECTORY}/{DB_FILE}")
        self.players_table = self.database.table("players")
        self.tournaments_table = self.database.table("tournaments")
