from time import sleep

from chess_tournament_app.views import menu_creator
from chess_tournament_app.controllers import utils
from chess_tournament_app.controllers.tournament_operator import TournamentOperator
from chess_tournament_app.controllers.database_operator import DatabaseOperator as Db

DEFAULT_ROUNDS = 4


class TournamentMenu:
    """
    Displays the tournament main menu with the 3 main options to:
    - Create a new Tournament
    - Show existing tournaments
    - Play tournaments (that are new or unfinished)
    """

    def __init__(self):
        """TournamentMenu constructor"""

        self.title = "Tournament Menu"
        self.options = {
             "Create New Tournament": NewTournament,
             "Show Tournaments": ShowTournaments,
             "Play Tournament": PlayTournamentMenu
        }
        utils.cls()
        utils.print_logo()
        menu = menu_creator.MenuScreen(
            self.title,
            self.options,
            self.__class__.__name__
        )
        menu.print_menu()
        menu.user_action()


class NewTournament:
    """Let's user create and save a new tournament"""

    def __init__(self):
        """Constructor for NewTournament"""
        self.spacer = "\n                     "
        self.title = "New Tournament"

        self.menu = menu_creator.MenuScreen(
            title=self.title,
            current_site=self.__class__.__name__
        )

        self.name = ""
        self.location = ""
        self.date = []
        self.number_of_rounds = ""
        self.rounds = []
        self.players = []
        self.time_control = ""
        self.description = ""
        self.leaderboard = []

        self.saved_players = len(Db().load_all_players())

        self.enter_data()
        self.confirm()

    def enter_data(self):
        """prompts the user to enter all required tournament data"""
        utils.cls()
        utils.print_logo()
        self.menu.print_menu()

        # ----------------------------Enter Name-------------------------------

        while len(self.name) < 3:
            self.name = input(
                f"{self.spacer}What´s the name of the Tournament?: ").title()

        # ----------------------------Enter Location---------------------------

        while len(self.location) < 5:
            self.location = input(
                f"\n{self.spacer}What´s the location of the Tournament?: ").title()

        # ----------------------------Enter Date-------------------------------

        date = ""
        while not utils.valid_date(date):
            date = input(
                f"\n{self.spacer}"
                f"What´s the start date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(If it´s today you can type 'today'): ")
            if date == "today":
                date = utils.date_today()

        self.date.append(date)

        # ----------------------------Enter Time Control-----------------------

        while self.time_control not in ["bullet", "blitz", "rapid"]:
            self.time_control = input(
                f"\n{self.spacer}"
                f"Time control? (bullet / blitz / rapid): ").lower()

        # ----------------------------Enter Description------------------------

        while len(self.description) < 1:
            self.description = input(
                f"\n{self.spacer}Enter a Description: ").capitalize()

        # ----------------------------Enter Number of Rounds-------------------

        while not utils.valid_int(self.number_of_rounds, ):
            self.number_of_rounds = input(
                f"\n{self.spacer}Number of rounds to play "
                f"(default is {DEFAULT_ROUNDS}): ") or DEFAULT_ROUNDS
        self.number_of_rounds = int(self.number_of_rounds)

        # ------------------------------Select Players-------------------------

        number_of_players = ""
        while not utils.valid_player_number(
                number_of_players, self.number_of_rounds):
            number_of_players = input(
                f"\n{self.spacer}Number of participants "
                f"(min. {self.number_of_rounds + 2}): ")
        number_of_players = int(number_of_players)

        self.players = SelectPlayers(number_of_players).selection()

    def confirm(self):
        """
        1. Displays the all tournament details
        2. Asks user if it's all correct
        3. If user answers 'yes' the tournament gets saved.
        4. If if user answers 'no' the tournament doesn't get saved.
        """
        ser_players = [Db().player_by_id(id_num) for id_num in self.players]
        player_name_list = [
            p["first name"] + " " + p["last name"] for p in ser_players]
        names = "\n"
        for name in player_name_list:
            names += f"                                         {name}\n\n"

        utils.cls()
        utils.print_logo()
        menu = menu_creator.MenuScreen("Confirm")
        menu.print_menu()

        print(f"""
                     Tournament Name:    {self.name}\n
                     Location:           {self.location}\n
                     Date(s):            {self.date[0]}\n
                     Nr. of Rounds:      {self.number_of_rounds}\n
                     Time Control:       {self.time_control}\n
                     Participants:       {names}\n
                     Description:        {self.description}\n
                """)

        if input(f"{self.spacer}"
                 f"Are details about the new tournament correct? (Y/N) "
                 ).lower() == "y":
            self.save_tournament()
            print(f"{self.spacer}{self.name} - got saved in the Database")
            sleep(3)
            TournamentMenu()
        else:
            TournamentMenu()

    def save_tournament(self):
        """Saves new Tournament in the database"""
        Db().save_tournament(
            name=self.name,
            location=self.location,
            date=self.date,
            number_of_rounds=self.number_of_rounds,
            rounds=self.rounds,
            players=self.players,
            time_control=self.time_control,
            description=self.description,
            leaderboard=self.leaderboard
        )


class SelectPlayers:
    """
    Takes an int that represents a the number of players
    that is supposed to participate on the Tournament.
    Lets the user select players
    (with a minimal amount of players to fit the number of rounds)
    and returns them in a list.
    (works by using the class: ShowPlayers,
    to display the available players to the user)
    """
    def __init__(self, number_of_players: int):
        """Select Players Constructor"""
        self.spacer = "\n                     "

        self.player_ids = []
        self.number_of_participants = number_of_players

        self.show_players = ShowPlayers()
        self.show_players.order()

    def selection(self):
        """
        Displays all available PLayers from Database and lets the user pick
        one after the other to add them to the list of participants.
        """
        available_ids = [p.doc_id for p in Db().load_all_players()]

        while len(self.player_ids) < self.number_of_participants:

            picked = "0"
            while not utils.valid_int(picked) or picked in self.player_ids:
                self.show_players.show_all(not_show=self.player_ids)
                print(f"{self.spacer}Players in Tournament "
                      f"{len(self.player_ids)} / "
                      f"{self.number_of_participants}")
                picked = input(f"{self.spacer}Add to tournament (Enter ID): ")
            picked = int(picked)

            if picked not in self.player_ids and picked in available_ids:
                self.player_ids.append(picked)

        return self.player_ids


class ShowPlayers:
    """
    Displays all players incl. a table of their information,
    sorted by a detail of the users choice.
    Players that are already added to the tournament
    will not be displayed anymore.
    """
    def __init__(self):
        self.title = "Pick Participants"
        self.options = {
            "Show all players sort by ID": self.sort_by_id,
            "Show all players sort by first name": self.sort_by_first_name,
            "Show all players sort by last name": self.sort_by_last_name,
            "Show all players sort by birth date": self.sort_by_birth_date,
            "Show all players sort by sex": self.sort_by_sex,
            "Show all players sort by rating": self.sort_by_rating,
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)

        self.all_players = Db().load_all_players()

    def order(self):
        """lets the pick the order the players are supposed to be sorted by"""
        utils.cls()
        utils.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def sort_by_id(self):
        """Does nothing, because the players are already sorted by id"""
        pass

    def sort_by_first_name(self):
        """sort´s all players by first name"""
        self.all_players = sorted(
            self.all_players, key=lambda x: x.get('first name'))

    def sort_by_last_name(self):
        """sort´s all players by last name"""
        self.all_players = sorted(
            self.all_players, key=lambda x: x.get('last name'))

    def sort_by_birth_date(self):
        """sort´s all players by birth date"""
        self.all_players = sorted(
            self.all_players, key=lambda x: x.get('birth date'))

    def sort_by_sex(self):
        """sort´s all players by sex"""
        self.all_players = sorted(
            self.all_players, key=lambda x: x.get('sex'))

    def sort_by_rating(self):
        """sort´s all players by rating from highest to lowest"""
        self.all_players = sorted(
            self.all_players, key=lambda x: x.get('rating'), reverse=True)

    def show_all(self, not_show: list):
        """Displays all the available players to the user,
        also shows if player database is empty it will"""
        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)

        if len(self.all_players) == 0:
            print("\n                     No Players in Database!")
            sleep(2)
            TournamentMenu()

        for player in self.all_players:
            if player.doc_id not in not_show:
                print(utils.all_player_details(player))


class ShowTournaments:
    """
    Displays a menu with the options:
    - show a list of all finished tournaments
    (incl. a table of all their information)
    - show a list of all unfinished tournaments
    (incl. a table of all their information)
    - search for a tournament by using a specific value
    """
    def __init__(self):
        """Constructor for ShowTournaments"""
        self.spacer = "\n                     "
        self.title = "Show Tournaments"
        self.options = {
            "Show all Finished Tournaments": self.show_all_finished,
            "Show all Unfinished Tournaments": self.show_all_unfinished,
            "Search for a Tournament": SearchTournament
        }

        self.menu = menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__
        )

        self.all_tournaments_serialized = Db().load_all_tournaments()

        utils.cls()
        utils.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def show_all_unfinished(self):
        """Displays all unfinished Tournaments
        incl. a table of their information"""
        unfinished_tournaments = [
            t for t in self.all_tournaments_serialized
            if len(t["rounds"]) < t["number of rounds"]
        ]

        menu = menu_creator.MenuScreen(
            title="Unfinished Tournaments",
            options={
                "Play a Tournament": PlayTournamentMenu,
                "Edit a Tournament": EditTournament,
                "Delete a Tournament": DeleteTournament
            },
            current_site=self.__class__.__name__
        )

        utils.cls()
        utils.print_logo()
        menu.print_menu(title_only=True)

        if len(unfinished_tournaments) == 0:
            print(f"{self.spacer}No Unfinished Tournaments in Database!")
            sleep(3)
            ShowTournaments()

        else:
            for tournament in unfinished_tournaments:
                print(utils.all_tournament_details(tournament))

            menu.print_menu(options_only=True)
            menu.user_action()

    def show_all_finished(self):
        """Displays all finished Tournaments
        incl. a table of their information"""
        finished_tournaments = [
            t for t in self.all_tournaments_serialized
            if len(t["rounds"]) == t["number of rounds"]]

        menu = menu_creator.MenuScreen(
            title="Finished Tournaments",
            options={
                "Edit a Tournament": EditTournament,
                "Delete a Tournament": DeleteTournament
            },
            current_site=self.__class__.__name__
        )

        utils.cls()
        utils.print_logo()
        menu.print_menu(title_only=True)

        if len(finished_tournaments) == 0:
            print(f"{self.spacer}No Finished Tournaments in Database!")
            sleep(3)
            ShowTournaments()

        else:
            for tournament in finished_tournaments:
                print(utils.all_tournament_details(tournament))

        menu.print_menu(options_only=True)
        menu.user_action()


class SearchTournament:
    """
    1. Search for a tournaments by asking the user for a key
    2. If more than one match: displays all tournaments with a match
    """
    def __init__(self):
        """Constructor for SearchTournaments"""
        self.spacer = "\n                     "
        self.title = "Search for a Tournament"
        self.options = {
            "Search for a Name": self.search_name,
            "Search for a range of Dates": self.search_date,
            "Search for a Location": self.search_location,
            "Search for a time control (bullet, blitz, rapid)":
                self.search_time_control,
            "Get a Tournament by ID": self.get_by_id
        }
        self.menu = menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__
        )
        utils.cls()
        utils.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def search_name(self):
        """
        Asks the user for a name he wants to search for
        and calls self.search_for with the right key and value
        """
        name = ""
        while len(name) < 3:
            name = input(f"{self.spacer}What name do you want to search for? ")
        self.search_for("name", name)

    def search_date(self):
        """
        Asks the user for a span of dates he wants to search for
        and calls self.search_for with the right key and value
        """
        date_1 = ""
        while not utils.valid_date(date_1):
            date_1 = input(
                f"{self.spacer}From which date you want to search? ")
        date_2 = ""
        while not utils.valid_date(date_2):
            date_2 = input(
                f"{self.spacer}Until which date on should you search? ")
        dates = utils.date_range(date_1, date_2)
        self.search_for("date", dates)

    def search_location(self):
        """
        Asks the user for a location he wants to search for
        and calls self.search_for with the right key and value
        """
        location = ""
        while len(location) < 3:
            location = input(
                f"{self.spacer}What name do you want to search for? ")
        self.search_for("location", location)

    def search_time_control(self):
        """
        Asks the user for a time control he wants to search for
        and calls self.search_for with the right key and value
        """
        t_control = ""
        while len(t_control) < 3:
            t_control = input(
                f"{self.spacer}What name do you want to search for? ")
        self.search_for("time control", t_control)

    def get_by_id(self):
        """
        Asks the user for a ID he wants to directly load and see
        and calls self.search_for with the right key and value
        """
        t_id = ""
        while not utils.valid_int(t_id):
            t_id = input(f"{self.spacer}What ID do you want to search for? ")
        t_id = int(t_id)
        self.search_for("doc_id", t_id)

    def search_for(self, dict_key: str, dict_value: any):
        """
        Takes a dict_key and dict_value.
        Searches for matches in tournaments with the key,
        value pair the user gave it

        Args:
            dict_key (str): a key of that occurs in all tournament objects
            dict_value (any): a value to search for under the given key
        """
        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)
        db = Db()

        if dict_key == "doc_id":
            t_found = [db.tournament_by_id(dict_value)]

        elif dict_key == "date":
            all_tournaments = db.load_all_tournaments()
            t_found = []
            for t in all_tournaments:
                for date in t["date"]:
                    if date in dict_value:
                        t_found.append(t)

        else:
            t_found = db.search_tournament(
                filter_by=dict_key,
                key_word=dict_value
            )

        if not t_found or t_found == [None]:
            print(f"{self.spacer}No Tournament with that "
                  f"{dict_key.capitalize()} found!")
            sleep(3)
            SearchTournament()
        else:
            for t in t_found:
                print(utils.all_tournament_details(t))

        self.menu.print_menu(options_only=True)
        self.menu.user_action()


class PlayTournamentMenu:
    """
    Asks the user in which order the available Tournaments
    (unfinished Tournaments)
    are supposed to be displayed, display's them
    and lets the user pick one that is going to be played.
    """
    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Play Tournament"
        self.options = {
            "show Tournaments sort by ID": self.sort_by_id,
            "Show Tournaments sort by date (latest -> oldest)":
                self.sort_by_date
        }

        self.tournaments_serialized = Db().database.tournaments_table
        self.unfinished_tournaments = [
            t for t in self.tournaments_serialized
            if len(t["rounds"]) < t["number of rounds"]
        ]

        self.menu = menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__
        )

        utils.cls()
        utils.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)
        self.show_all()
        self.user_choice()

    def sort_by_id(self):
        """Does nothing, because the tournaments are already sorted by ID."""
        pass

    def sort_by_date(self):
        """sort´s all unfinished tournaments by date"""
        self.unfinished_tournaments = sorted(
            self.unfinished_tournaments,
            key=lambda x: x.get('date'[0]), reverse=True
        )

    def show_all(self):
        """Displays all unfinished tournaments in the chosen order"""
        if len(self.unfinished_tournaments) == 0:
            print("\n                     "
                  "No Tournaments found. Add a new Tournament first!")
            sleep(3)
            TournamentMenu()

        else:
            for tournament in self.unfinished_tournaments:
                print(utils.all_tournament_details(tournament))

    def user_choice(self):
        """User has to pick a tournament by ID"""
        available_ids = [str(t.doc_id) for t in self.unfinished_tournaments]

        tournament_id = ""
        while not utils.valid_int(tournament_id) or tournament_id not in available_ids:
            tournament_id = input(
                f"{self.spacer}"
                f"Which tournament do you want to start? (Enter ID): ")

        RunTournament(int(tournament_id))


class RunTournament:
    """
    Takes a Tournament ID, loads the tournament, and runs it from the beginning
    or if it was started already, it will continue
    wherever it has stopped last time.
    """
    def __init__(self, tournament_id: int):
        """The Constructor for RunTournament"""
        self.tournament = TournamentOperator(tournament_id)

        self.spacer = "\n                     "
        self.play_rounds()
        self.show_leaderboard()

    def play_rounds(self):
        """
        Checks which round is the current one to be played and continues
        playing them until all rounds are completed
        """
        while self.tournament.get_completed_rounds_nr() \
                < self.tournament.rounds_to_play:
            title = f"Playing Round " \
                    f"{self.tournament.get_current_round_number()}"
            menu = menu_creator.MenuScreen(title)
            utils.cls()
            utils.print_logo()
            menu.print_menu()

            self.current_round()
            self.tournament.update_scores()
            self.tournament.save_finished_round()

    def current_round(self):
        """
        Continues playing the current round at the point it was saved last
        time, loads the right list of pairings depending on the amount of
        finished rounds (that get created by first_pairing or next_pairing
        automatic) and saves every match in the database after it is finished.
        """
        if self.tournament.get_current_round_number() == 1:
            pairs = self.tournament.first_pairing()
        else:
            pairs = self.tournament.next_pairing()

        for pair in pairs:
            p1 = pair[0][0]
            p2 = pair[1][0]

            print(f"{self.spacer}---Match "
                  f"{self.tournament.get_current_match_number()}---")
            print(f"{self.spacer}{p1['first name']} {p1['last name']} vs "
                  f"{p2['first name']} {p2['last name']}")

            result = ""
            while result not in ["0", "1", "2"]:
                result = input(
                    f"{self.spacer}Winner? (P1 = 1, P2 = 2, Tie = 0): ")

            self.tournament.save_match(
                player_1=p1,
                player_2=p2,
                winner=int(result)
            )

    def show_leaderboard(self):
        """Displays the leaderboard"""

        title = "Results"
        options = {
            "Return to Tournament Menu": TournamentMenu,
            "Show Tournaments": ShowTournaments
        }
        menu = menu_creator.MenuScreen(
            title=title,
            options=options,
            current_site="MainMenu"
        )

        leaderboard = self.tournament.get_leaderboard()

        utils.cls()
        utils.print_logo()
        menu.print_menu(title_only=True)

        print(utils.readable_leaderboard(leaderboard))

        menu.print_menu(options_only=True)
        menu.user_action()


class EditTournament:
    """
    Lets the user pick a tournament and a value of it that
    is supposed to be changed.
    The value will be updated and saved in the database.
    Displays a confirmation afterwards and returns to TournamentMenus.
    """
    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Tournament Editor"
        self.options = {
            "Change Name": self.update_name,
            "Change Location": self.update_location,
            "Change Start Date": self.update_start_date,
            "Change Description": self.update_description,
            "Change Time Control": self.update_time_control
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)
        self.db = Db()

        print("\n\n")
        self.menu.print_menu(title_only=True)

        tournament_id = ""
        while not utils.valid_tournament_id(tournament_id):
            tournament_id = input(f"\n{self.spacer}Enter ID:  ")
        self.tournament_id = int(tournament_id)

        self.menu.print_menu(options_only=True)
        self.menu.user_action()

        TournamentMenu()

    def update_name(self):
        """Asks the user for a new name and updates it."""
        new_name = ""
        while len(new_name) < 3:
            new_name = input(
                f"{self.spacer}New Tournament Name:  ").capitalize()
        self.db.update_tournament(
            tournament_id=self.tournament_id,
            key="name",
            new_value=new_name
        )
        print(f"{self.spacer}"
              f"The Tournaments name has been changed to {new_name}!")
        sleep(2)

    def update_location(self):
        """Asks the user for a new location and updates it."""
        new_location = ""
        while len(new_location) < 3:
            new_location = input(
                f"{self.spacer}New Tournament Name:  ").title()
        self.db.update_tournament(
            tournament_id=self.tournament_id,
            key="location",
            new_value=new_location
        )
        print(f"{self.spacer}"
              f"The Tournaments location has been changed to {new_location}!")
        sleep(2)

    def update_start_date(self):
        """Asks the user for a new start date and updates it."""
        new_start_date = ""
        while not utils.valid_date(new_start_date):
            new_start_date = input(
                f"{self.spacer}New Start Date (DD.MM.YYYY):  ")
        dates = self.db.tournament_by_id(self.tournament_id)["date"]
        old_end_date = dates[-1]

        if new_start_date != old_end_date:
            new_dates = utils.date_range(new_start_date, old_end_date)
        else:
            new_dates = [new_start_date]

        self.db.update_tournament(
            tournament_id=self.tournament_id,
            key="date",
            new_value=new_dates
        )
        print(f"{self.spacer}The Tournaments Start Date has been changed to "
              f"{new_start_date}!")
        sleep(2)

    def update_description(self):
        """Asks the user for a new description and updates it."""
        new_description = ""
        while len(new_description) < 3:
            new_description = input(
                f"{self.spacer}New Description:  ").capitalize()
        self.db.update_tournament(
            tournament_id=self.tournament_id,
            key="description",
            new_value=new_description
        )
        print(f"{self.spacer}The Tournaments description has been changed to "
              f"{new_description}!")
        sleep(2)

    def update_time_control(self):
        """Asks the user for a new time control and updates it."""
        new_tc = ""
        while new_tc not in ["bullet", "blitz", "rapid"]:
            new_tc = input(f"{self.spacer}New Time Control "
                           f"(bullet, blitz, rapid):  ").lower()
        self.db.update_tournament(
            tournament_id=self.tournament_id,
            key="time control",
            new_value=new_tc
        )
        print(f"{self.spacer}The Tournaments time control has been changed to "
              f"{new_tc}!")
        sleep(2)


class DeleteTournament:
    """
    The user has to pick a Tournament by ID and has to confirm
    that he wants to delete it from the database.
    """

    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Delete Tournament"
        self.options = {
            "Delete Tournament": self.delete
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)

        print("\n\n")
        self.menu.print_menu(title_only=True)

        tournament_id = ""
        while not utils.valid_tournament_id(tournament_id):
            tournament_id = input(f"\n{self.spacer}Enter ID:  ")
        self.tournament_id = int(tournament_id)

        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def delete(self):
        """Deletes the Tournament (soft delete), prints confirmation and
           turns back to the search player menu."""
        Db().delete_tournament(self.tournament_id)
        print(f"{self.spacer}The Tournament: "
              f"{Db().tournament_by_id(self.tournament_id)['name']} "
              f"was deleted!")
        sleep(2)
        TournamentMenu()
