from chess_tournament_app.controllers.utils import valid_menu_choice, turn_back_to


class MenuScreen:
    """Creates the menu incl. Title, available options
    and causes an action after the user choice

    Args:
         title = str
         options = dict of options(str): classes(obj)
         current_site = self.__class__.__name__
         (returns the name of the class that called it)

         If no current_site is given it will show the option to close the program.
         If no title is given, it will show no title.
         If no options are given, it will not show options.
         """

    def __init__(
            self,
            title: str = None,
            options: dict = None,
            current_site: str = None):
        """Constructor for MenuScreen"""
        self.title = title
        self.options = options
        self.current_site = current_site

        self.title_size = "---------------------"
        self.menu_spacer = "                     "
        self.dashes = int((len(self.title_size) - len(title)) / 2) * "-"
        self.title_layout = f"{self.menu_spacer}{self.dashes}" \
                            f"{self.title}{self.dashes}"
        self.opt_num = 1
        self.option_rows = ""
        self.option_keys = []

    def print_menu(self, title_only: bool = False, options_only: bool = False):
        """Prints the menu and adds the option numbers automatically
            If title_only = True, only the title will be printed!
            If options_only = True, only the Options will be printed!

            Args:
                    title_only: bool (default set to False)
                    options_only: bool (default set to False)
        """

        if not self.options:
            self.options = {}

        turn_back_option = ""

        if not self.current_site:
            turn_back_option = "Return"

        elif self.current_site == "MainMenu":
            turn_back_option = "Close Program"

        elif self.current_site in [
            "PlayerMenu",
            "TournamentMenu"
        ]:
            turn_back_option = "Return Home"

        elif self.current_site in [
            "AddNewPlayer",
            "ShowAllPlayers",
            "SearchPlayer",
        ]:
            turn_back_option = "Return to Player Menu"

        elif self.current_site in [
            "EditPlayer",
            "DeletePlayer",
            "EditOrDelete"
        ]:
            turn_back_option = "Return to Search Player Menu"

        elif self.current_site in [
            "NewTournament",
            "ShowTournaments",
            "SearchTournament",
            "PlayTournamentMenu",
            "DeleteTournament",
            "EditTournament",
            "Run Tournament"
        ]:
            turn_back_option = "Return to Tournament Menu"

        elif self.current_site in ["SelectPlayers", "ShowPlayers"]:
            turn_back_option = "Cancel tournament creation -> " \
                               "return to Tournament Menu"

        if len(self.options) == 0 or title_only:
            menu = f"\n{self.title_layout}\n"
            print(menu)

        else:
            if type(self.options) is list:
                if not self.option_keys:
                    for option in self.options:
                        self.option_rows += f"{self.menu_spacer}" \
                                            f"[{self.opt_num}] {option}\n\n"
                        self.option_keys.append(option)
                        self.opt_num += 1

            else:
                if not self.option_keys:
                    for option, command in self.options.items():
                        self.option_rows += f"{self.menu_spacer}" \
                                            f"[{self.opt_num}] {option}\n\n"
                        self.option_keys.append(option)
                        self.opt_num += 1

            if not self.title or options_only:
                menu = f"\n{self.option_rows}\n\n{self.menu_spacer}[0] " \
                       f"{turn_back_option}\n\n"

            else:
                menu = f"\n{self.title_layout}\n\n{self.option_rows}\n\n" \
                       f"{self.menu_spacer}[0] {turn_back_option}\n\n\n"

            print(menu)

    def user_action(self):
        """Asks the user for the next action and executes it"""
        answer = ""

        while not valid_menu_choice(answer, self.opt_num):
            answer = input(
                f"\033[F{self.menu_spacer}What would you like to do? ")

        if int(answer) == 0:
            turn_back_to(self.current_site)

        else:
            self.options.get(self.option_keys[int(answer)-1])()
