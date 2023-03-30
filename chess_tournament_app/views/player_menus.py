from time import sleep

from chess_tournament_app.views import menu_creator
from chess_tournament_app.controllers import utils
from chess_tournament_app.controllers.database_operator import DatabaseOperator


class PlayerMenu:
    """Displays options for player related operations"""
    def __init__(self):
        """ PlayerMenu Constructor"""
        self.title = "Player Menu"
        self.options = {
            "Add a new player": AddNewPlayer,
            "Show all players": ShowAllPlayers,
            "Search Player": SearchPlayer
        }
        self.player_main_menu()

    def player_main_menu(self):
        """Shows the player main menu"""
        utils.cls()
        utils.print_logo()
        menu = menu_creator.MenuScreen(
            self.title,
            self.options,
            self.__class__.__name__
        )
        menu.print_menu()
        menu.user_action()


class AddNewPlayer:
    """New player creator"""
    def __init__(self):
        """New player constructor"""

        self.spacer = "\n                     "
        self.title = "Create new Player"

        self.first_name = ""
        self.last_name = ""
        self.birth_date = ""
        self.sex = ""
        self.rating = -1

        self.menu = menu_creator.MenuScreen(
            title=self.title,
            current_site=self.__class__.__name__
        )
        self.enter_player_details()
        self.check_details()

    def enter_player_details(self):
        """ask user for the details of the new player"""
        utils.cls()
        utils.print_logo()
        self.menu.print_menu()

        while len(self.first_name) < 2:
            self.first_name = input(
                f"{self.spacer}What´s the players first name?: ").capitalize()

        while len(self.last_name) < 2:
            self.last_name = input(
                f"{self.spacer}What´s the players last name?: ").capitalize()

        while not utils.valid_date(self.birth_date):
            self.birth_date = input(
                f"{self.spacer}What´s the players birth date? (DD.MM.YYYY)?: ")

        while not utils.valid_sex(self.sex):
            self.sex = input(
                f"{self.spacer}What´s the players sex? (M/F): ").upper()

        while not utils.valid_rating(self.rating):
            self.rating = input(
                f"{self.spacer}What´s the players current rating?: ")
            self.rating = int(self.rating)

    def check_details(self):
        """
        1. Displays the all the players details
        2. Asks user if it's all correct
        3. If user answers 'yes' the player gets saved.
           If if user answers 'no' the player doesn't get saved.
        """
        utils.cls()
        utils.print_logo()
        menu = menu_creator.MenuScreen("Check and Approve")
        menu.print_menu()

        print(f"""
                     Name:             {self.first_name} {self.last_name}
                     Date of Birth:    {self.birth_date}
                     Sex:              {self.sex}
                     Rating:           {self.rating}
        """)

        if input(f"{self.spacer}"
                 f"Are all details of the new player correct? (Y/N) "
                 ).lower() or "y" == "y":
            self.save_player()
            print(f"{self.spacer}{self.first_name} {self.last_name} "
                  f"added to the Database")
            sleep(3)
            PlayerMenu()
        else:
            PlayerMenu()

    def save_player(self):
        """Saves new Player in the database"""
        DatabaseOperator().save_player(
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            sex=self.sex,
            rating=self.rating
        )


class ShowAllPlayers:
    """Displays all players incl. table of their information,
       sorted by a detail of the users choice"""
    def __init__(self):
        self.title = "Show all Players"
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

        self.title_2 = "All Players"
        self.options_2 = {
            "Add a new player": AddNewPlayer,
            "Edit Player": SearchPlayer
        }
        self.menu_2 = menu_creator.MenuScreen(
            self.title_2, self.options_2, self.__class__.__name__)

        self.all_players = DatabaseOperator().load_all_players()

        utils.cls()
        utils.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

        utils.cls()
        utils.print_logo()
        self.menu_2.print_menu(title_only=True)
        self.show_all()

        self.menu_2.print_menu(options_only=True)
        self.menu_2.user_action()

    def sort_by_id(self):
        """Does nothing, because the list is already sorted by ID"""
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

    def show_all(self):
        """Displays all players and a table of their details"""
        if len(self.all_players) == 0:
            print("\n                     No Players in Database!")

        else:
            for player in self.all_players:
                print(utils.all_player_details(player))


class SearchPlayer:
    """ 1. Search for a player by asking the user for a key
        2. If more than one match: displays all players with a match
           and asks the user to pick a player
        3. Chosen Player gets displayed and the User gets
           to pick witch detail he wants to change.
        """

    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Search Player"
        self.options = {
            "Search for a First Name": self.search_first_name,
            "Search for a Last Name": self.search_last_name,
            "Search for a Birthdate": self.search_birth_date,
            "Search for a Rating": self.search_rating,
            "Search for a Sex": self.search_sex,
            "Get player directly by ID": self.get_by_id
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)
        self.show_options()

    def show_options(self):
        """Displays the available Options and lets the user pick one"""
        utils.cls()
        utils.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def search_first_name(self):
        self.search_for("first name")

    def search_last_name(self):
        self.search_for("last name")

    def search_birth_date(self):
        self.search_for("birth date")

    def search_rating(self):
        self.search_for("rating")

    def search_sex(self):
        self.search_for("sex")

    def get_by_id(self):
        self.search_for("doc_id")

    def search_for(self, dict_key: str):
        """
        Takes a dict_key - string, asks the user for a new value,
        updates and saves the value of the player in the Database
        """
        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)
        wanted_value = input(
            f"{self.spacer}The wanted {dict_key.title()}: ")

        if dict_key == "doc_id":
            player_found = DatabaseOperator().player_by_id(int(wanted_value))
            if player_found:
                EditOrDelete(player_found)
            else:
                print(f"{self.spacer}No Player with that ID found!")
                sleep(3)
                SearchPlayer()

        else:
            matches = DatabaseOperator().search_player(
                dict_key, wanted_value.capitalize())

            if len(matches) == 0:
                print(f"{self.spacer}"
                      f"No Player with that {dict_key.title()} found!")
                sleep(3)
                SearchPlayer()

            elif len(matches) > 1:
                for player in matches:
                    print(utils.all_player_details(player))

                id_num = ""
                while not id_num.isnumeric():
                    id_num = input(
                        f"{self.spacer}"
                        f"Several matches found! Pick a player by ID!  ")
                EditOrDelete(matches[int(id_num) - 1])

            else:
                EditOrDelete(matches[0])


class EditOrDelete:
    """Takes a player object and ask´s the
       user if he wants to edit or delete it"""
    def __init__(self, player_obj):
        self.spacer = "\n                     "
        self.title = "Edit or Delete"
        self.options = {
            "Edit Player": self.edit,
            "Delete Player": self.delete,
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)
        self.player_obj = player_obj

        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)
        print(utils.all_player_details(self.player_obj))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def edit(self):
        """Calls the player editor"""
        EditPlayer(self.player_obj)

    def delete(self):
        """Calls Delete Player"""
        DeletePlayer(self.player_obj)


class EditPlayer:
    """
    Takes a player object and ask´s the user which
    Detail of the player is supposed to be changed
    """
    def __init__(self, player_object):
        """The Constructor of EditPlayer"""
        self.spacer = "\n                     "
        self.title = "Player Editor"
        self.options = {
            "Change First Name": self.update_first_name,
            "Change Last Name": self.update_lastname,
            "Change Birthdate": self.update_birth_date,
            "Change Sex": self.update_sex,
            "Change Rating": self.update_rating,
            "Delete the Player": self.open_delete_player
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)
        self.player_object = player_object

        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)
        print(utils.all_player_details(self.player_object))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def update_first_name(self):
        """Asks the user for a new first name, updates it in the database
        and displays a confirmation."""
        new_first_name = ""
        while len(new_first_name) < 2:
            new_first_name = input(
                f"{self.spacer}New First Name:  ").capitalize()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="first name",
            new_value=new_first_name)
        print(f"{self.spacer}{self.player_object['first name']}´s "
              f"First Name successfully updated to {new_first_name}!")
        sleep(2)
        SearchPlayer()

    def update_lastname(self):
        """Asks the user for a new last name, updates it in the database
        and displays a confirmation."""
        new_last_name = ""
        while len(new_last_name) < 2:
            new_last_name = input(
                f"{self.spacer}New Last Name:  ").capitalize()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="last name",
            new_value=new_last_name)
        print(f"{self.spacer}{self.player_object['first name']}´s "
              f"Last Name successfully updated to {new_last_name}!")
        sleep(2)
        SearchPlayer()

    def update_birth_date(self):
        """Asks the user for a new birth date, updates it in the database
        and displays a confirmation."""
        new_birth_date = ""
        while not utils.valid_date(new_birth_date):
            new_birth_date = input(
                f"{self.spacer}New Birth Date:  ").capitalize()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="birth date",
            new_value=new_birth_date)
        print(f"{self.spacer}{self.player_object['first name']}´s "
              f"Birth Date successfully updated to {new_birth_date}!")
        sleep(2)
        SearchPlayer()

    def update_sex(self):
        """Asks the user for a new value for sex, updates it in the database
        and displays a confirmation."""
        new_sex = ""
        while not utils.valid_sex(new_sex):
            new_sex = input(f"{self.spacer}New Sex:  ").upper()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="sex",
            new_value=new_sex)
        print(f"{self.spacer}{self.player_object['first name']}´s "
              f"Sex successfully updated to {new_sex}!")
        sleep(2)
        SearchPlayer()

    def update_rating(self):
        """Asks the user for a new rating, updates it in the database
        and displays a confirmation."""
        new_rating = -1
        while not utils.valid_rating(new_rating):
            new_rating = input(f"{self.spacer}New Rating:  ")
        new_rating = int(new_rating)
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="rating",
            new_value=new_rating)
        print(f"{self.spacer}{self.player_object['first name']}´s "
              f"Rating successfully updated to {new_rating}!")
        sleep(2)
        SearchPlayer()

    def open_delete_player(self):
        """Opens the delete player menu"""
        DeletePlayer(self.player_object).delete()


class DeletePlayer:
    """Player gets displayed and the User has to confirm
       that he wants to delete the player from the database."""

    def __init__(self, player_object):
        """The constructor for DeletePlayer"""
        self.spacer = "\n                     "
        self.title = "Delete Player"
        self.options = {
            f"Please confirm: Delete the player {player_object['first name']} "
            f"{player_object['last name']} from the database!": self.delete
        }
        self.menu = menu_creator.MenuScreen(
            self.title, self.options, self.__class__.__name__)
        self.player_object = player_object

        utils.cls()
        utils.print_logo()
        self.menu.print_menu(title_only=True)
        print(utils.all_player_details(self.player_object))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def delete(self):
        """Deletes the Player, prints confirmation and
           turns back to the search player menu."""
        DatabaseOperator().delete_player(self.player_object.doc_id)
        print(f"{self.spacer}The player: {self.player_object['first name']} "
              f"{self.player_object['last name']} was deleted!")
        sleep(2)
        SearchPlayer()
