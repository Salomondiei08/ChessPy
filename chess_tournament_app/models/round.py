
class Round:
    """The round model"""
    def __init__(self,
                 round_name: str,
                 matches: list,
                 start_date_time: str,
                 end_date_time: str
                 ):
        """Constructor for Round

        Args:
            round_name: str - name of the current round in the Tournament
            matches: list - list of match instances
            start_date_time: str - the start datetime-object
            end_date_time: str - the end datetime-object
        """
        self.name = round_name
        self.matches = matches
        self.start_time = start_date_time
        self.end_time = end_date_time

    def create(self):
        """Creates and returns a new Round"""
        ser_round = {
                "name": self.name,
                "matches": self.matches,
                "start time": self.start_time,
                "end time": self.end_time
                 }

        return ser_round
