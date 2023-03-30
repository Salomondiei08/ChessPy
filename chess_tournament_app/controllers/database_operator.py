from tinydb import Query

from chess_tournament_app.models.player import Player
from chess_tournament_app.models.tournament import Tournament
from chess_tournament_app.models.database import Database


class DatabaseOperator:
    """Database operators"""

    def __init__(self):
        """DatabaseOperator constructor"""

        self.database = Database()
        self.query = Query()

    def save_player(self, first_name, last_name, birth_date, sex, rating):
        """Player gets serialized and saved in database"""

        serialized_player = Player(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            sex=sex,
            rating=rating,
        ).create()

        self.database.players_table.insert(serialized_player)

    def load_all_players(self):
        """Loads all players and returns them in a list"""
        all_players_serialized = [p for p in self.database.players_table.all() if not p["deleted"]]

        return all_players_serialized

    def search_player(self, filter_by, key_word):
        """Loads all players matching a given key
           and returns a dict of all matches"""

        results = self.database.players_table.search(self.query[filter_by] == key_word)
        return results

    def player_by_id(self, player_id: int):
        """Takes a player ID and returns
           the matching Player as a player object"""

        player = self.database.players_table.get(doc_id=player_id)
        return player

    def update_player(self, player_id, key: str, new_value):
        """Update the value of a given key in the database """

        self.database.players_table.update(
            {key: new_value},
            doc_ids=[player_id]
        )

    def update_all_matching_players(self, key: str, old_value: str, new_value: str):
        """Updates all matching entries in the player table"""

        self.database.players_table.update(
            {key: new_value},
            self.query[key] == old_value
        )

    def hard_delete_player(self, player_id: int):
        """Player Object gets really deleted from the database"""
        self.database.players_table.remove(doc_ids=[player_id])

    def delete_player(self, player_id: int):
        """Changes the value >is_deleted< of a player object in the database to True"""
        self.database.players_table.update(
            {"deleted": True},
            doc_ids=[player_id]
        )

    # ----------------------------------Tournament Operations--------------------------------------

    def save_tournament(self,
                        name,
                        location,
                        date,
                        number_of_rounds,
                        rounds,
                        players,
                        time_control,
                        description,
                        leaderboard
                        ):
        """Tournament gets serialized and saved in database"""

        serialized_tournament = Tournament(
            name=name,
            location=location,
            date=date,
            number_of_rounds=number_of_rounds,
            rounds=rounds,
            players=players,
            time_control=time_control,
            description=description,
            leaderboard=leaderboard
        ).create()

        self.database.tournaments_table.insert(serialized_tournament)

    def load_all_tournaments(self):
        """Loads all players and returns them in a list"""
        all_tournaments_serialized = [
            t for t in self.database.tournaments_table.all() if not t["deleted"]]

        return all_tournaments_serialized

    def search_tournament(self, filter_by: str, key_word):
        """Loads all tournaments matching a given key
           and returns a list of all matches"""
        results = self.database.tournaments_table.search(self.query[filter_by] == key_word)
        return results

    def update_tournament(self, tournament_id, key: str, new_value):
        """Update the value of a given key inside a tournament in the database

        Args:
            tournament_id: int - ID of the tournament
            key: str - key that is supposed to be updated
            new_value: any valid value for the given key to be updated
        """
        self.database.tournaments_table.update(
            {key: new_value},
            doc_ids=[tournament_id]
        )

    def tournament_by_id(self, tournament_id: int):
        """Takes a player ID and returns
           the matching Player as a player object"""
        tournament = self.database.tournaments_table.get(doc_id=tournament_id)
        return tournament

    def hard_delete_tournament(self, tournament_id):
        """Tournament Object gets really deleted from the database"""
        self.database.tournaments_table.remove(doc_ids=[tournament_id])

    def delete_tournament(self, tournament_id: int):
        """Changes the value >is_deleted< of a tournament object in the database to True"""
        self.database.tournaments_table.update(
            {"deleted": True},
            doc_ids=[tournament_id]
        )
