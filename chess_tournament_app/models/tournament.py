
class Tournament:
    """The Model for Tournament"""
    def __init__(
            self,
            name: str,
            location: str,
            date: list,
            number_of_rounds: int,
            rounds: list,
            players: list,
            time_control: str,
            description: str,
            leaderboard: list
            ):
        """Tournament Constructor

            Args:
                name (str): name of the tournament
                location (str): location of the tournaments
                date (str): date or range of dates of the tournament
                number of rounds (int): rounds to play
                rounds (list): list of round instances
                players (list): list of participants
                time_control (str): bullet, blitz, or rapid
                description (str): description of the tournament
                leaderboard (list): a list of lists, with a player obj
                and a score in each sub lists
        """
        self.name = name
        self.location = location
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description
        self.leaderboard = leaderboard
        self.deleted = False

    def create(self):
        """Creates and returns a new tournament"""
        tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "number of rounds": self.number_of_rounds,
            "rounds": self.rounds,
            "players": self.players,
            "time control": self.time_control,
            "description": self.description,
            "leaderboard": self.leaderboard,
            "deleted": self.deleted
        }
        return tournament
