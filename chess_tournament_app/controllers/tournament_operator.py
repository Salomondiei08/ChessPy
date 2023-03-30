from datetime import datetime

from chess_tournament_app.controllers import utils
from chess_tournament_app.controllers.database_operator import DatabaseOperator as Db
from chess_tournament_app.models.round import Round
from chess_tournament_app.models.match import Match

ROUND_NAME = "Round"


class TournamentOperator:
    """The Tournament Operator, gets a Tournament object by doc_id and play's
    all the rounds and matches no matter if the Tournament is new or if a
    number of rounds or matches was played already.
    It will pair the players according to the swiss tournament system and
    allows no pairing to occur twice.

    Args:
        tournament_id (int): doc_id of the tournament object that is supposed
        to be played
    """
    def __init__(self, tournament_id: int):
        """Constructor for the Tournament operator"""

        self.tournament_id = tournament_id
        self.tournament = Db().tournament_by_id(self.tournament_id)

        self.rounds = self.tournament["rounds"]
        ser_players = [
            Db().player_by_id(id_num) for id_num in self.tournament["players"]]
        self.players = sorted(
            ser_players, key=lambda x: x.get('rating'), reverse=True)

        if self.tournament["leaderboard"]:
            self.leaderboard = self.tournament["leaderboard"]
        else:
            self.leaderboard = [[p, 0] for p in self.players]

        self.matches_per_round = len(self.players) // 2

        if not self.rounds:
            self.rounds.append(self.new_round())

        if len(self.rounds[-1]["matches"]) == self.matches_per_round:
            self.rounds.append(self.new_round())

        self.rounds_to_play = self.tournament["number of rounds"]

    def get_current_round_number(self):
        """Returns the current match number"""

        current_round_number = len(self.rounds)

        return current_round_number

    def get_completed_rounds_nr(self):
        """Returns the number of all completed rounds"""

        completed_rounds_nr = 0
        for r in self.rounds:
            if len(r["matches"]) == self.matches_per_round:
                completed_rounds_nr += 1

        return completed_rounds_nr

    def get_completed_rounds(self):
        """Returns the number of all completed rounds"""

        completed_rounds = []
        for r in self.rounds:
            if len(r["matches"]) == self.matches_per_round:
                completed_rounds.append(r)

        return completed_rounds

    def get_current_match_number(self):
        """Returns the number of the current match"""

        current_match_number = len(self.rounds[-1]["matches"]) + 1

        return current_match_number

    def first_pairing(self):
        """Takes the sorted list 'players_with_score' sorted by rating,
        splits it in upper and lower half
        and best player in the upper half is paired with the best player in
        the lower half, and so on"""

        upper_half = self.leaderboard[:len(self.leaderboard) // 2]
        lower_half = self.leaderboard[len(self.leaderboard) // 2:]

        played_already = []
        if self.rounds[-1]["matches"]:
            for match in self.rounds[-1]["matches"]:
                for ps in match:
                    played_already.append(ps[0])

        pairing = [[upper_half[m], lower_half[m]] for m
                   in range(self.matches_per_round)
                   if upper_half[m][0] not in played_already]

        return pairing

    def next_pairing(self):
        """
        Takes the list 'players_with_score' that is sorted by score and rank.
        Player 1 vs. Player 2, Player 3 vs. player 4,... except two players had
        a match in that tournament already.
        In that case a player gets matched with the next one in the order that
        didn't had a match with him already.
        If a match was already saved in that round earlier it will get skipped!
        """

        # Creates a list of all pairings that have
        # already occurred in this tournament.
        pairings_before = []
        for finished_round in self.rounds:
            for match in finished_round["matches"]:
                pairings_before.append([match[0][0], match[1][0]])

        # Creates a list of all players who have already
        # played a match in the current round.
        played_current_round = []
        if self.rounds[-1]["matches"]:
            for match in self.rounds[-1]["matches"]:
                for ps in match:
                    played_current_round.append(ps[0])

        # Creates a list of new pairings from the sorted list
        # (players_with_score)
        # but if a pairing occurred already (in pairings_before)
        # it takes the next possible player
        # that hasn't matched with the first one already.
        sorted_players = self.leaderboard.copy()
        new_pairings = []
        count = 0
        tries = -1

        while len(sorted_players) > 0:
            try:
                for i in range(1, len(sorted_players)):
                    player_a = sorted_players[0][0]
                    player_b = sorted_players[i][0]

                    if [player_a, player_b] not in pairings_before and \
                            [player_b, player_a] not in pairings_before:
                        pair = [sorted_players.pop(0), sorted_players.pop(i-1)]
                        new_pairings.append(pair)
                        break

                # If the first loop couldn't find any more new pairings,
                # The sorted_players list resets and
                # switch two players with each new attempt
                # by switching first the last two
                # and then always one position earlier in the list.
                if count > len(self.leaderboard):
                    tries -= 1
                    count = 0
                    new_pairings = []
                    sorted_players = self.leaderboard.copy()
                    sorted_players[tries], sorted_players[tries - 2] = \
                        sorted_players[tries - 2], sorted_players[tries]

                count += 1

            # If the second step still couldn't find a
            # player and caused an IndexError,
            # Tries will be negated and the sorted_players list resets,
            # so players will switched from the beginning of the list instead
            except IndexError:
                sorted_players = self.leaderboard.copy()
                new_pairings = []
                count = 0
                tries *= -1

        # Adds only the pairs to the current round matches
        # that wasn't done playing already
        pairings_current_round = [[pair[0], pair[1]] for pair in new_pairings
                                  if pair[0][0] not in played_current_round]

        return pairings_current_round

    def update_scores(self):
        """Gets the player-Score-lists from the current and (if there is one)
        the previous Rounds.
        The Score of each player gets updated by adding the score of the
        current Round.
        The updated list will be sorted by the score, if multiple players have
        the same score they will get sorted according to rank."""

        last_leaderboard = []
        for match in self.rounds[-1]["matches"]:
            for ps in match:
                last_leaderboard.append(ps)

        for ps_old in self.leaderboard:
            for ps_new in last_leaderboard:
                if ps_old[0] == ps_new[0]:
                    ps_old[1] += ps_new[1]

        self.leaderboard = sorted(
            self.leaderboard,
            key=lambda x: (x[1], x[0].get('rating')),
            reverse=True
        )

    def save_match(self, player_1, player_2, winner):
        """Takes two players and a winner and creates a match object by using
        the match model
        and saves it in the current tournament by using the update tournament
        method

        Args:
            player_1: player object
            player_2: player object
            winner: int - 1(p1 won), 2(p2 won), 0(tie)
        """

        match = Match(
            player_1=player_1,
            player_2=player_2,
            winner=winner
        ).create()

        self.rounds[-1]["matches"].append(match)
        Db().update_tournament(
            tournament_id=self.tournament_id,
            key="rounds",
            new_value=self.rounds
        )

    def save_finished_round(self):
        """Adds an End time to the current round
        and saves it in the Database. """

        self.rounds[-1]["end time"] = datetime.now().strftime(
            "%d.%m.%Y, %H:%M:%S"
        )
        Db().update_tournament(
            tournament_id=self.tournament_id,
            key="rounds",
            new_value=self.rounds
        )

        Db().update_tournament(
            tournament_id=self.tournament_id,
            key="leaderboard",
            new_value=self.leaderboard
        )

        if self.get_completed_rounds_nr() < self.rounds_to_play:
            self.rounds.append(self.new_round())
        else:
            t_start_date = self.tournament["date"][0]
            t_end_date = datetime.today().strftime("%d.%m.%Y")
            if t_start_date != t_end_date:
                date = utils.date_range(t_start_date, t_end_date)

                Db().update_tournament(
                    tournament_id=self.tournament_id,
                    key="date",
                    new_value=date
                )

    def new_round(self):
        """Creates a new Round with an empty list of matches
        and an empty end datetime string"""
        new_round = Round(
            round_name=f"{ROUND_NAME} {self.get_current_round_number() + 1}",
            matches=[],
            start_date_time=datetime.now().strftime("%d.%m.%Y, %H:%M:%S"),
            end_date_time=""
        ).create()
        return new_round

    def get_leaderboard(self):
        """Returns the leaderboard"""

        return self.leaderboard
