import chess_tournament_app.views.menu_creator
import chess_tournament_app.controllers.utils as tools

from chess_tournament_app.views.player_menus import PlayerMenu
from chess_tournament_app.views.tournament_menus import TournamentMenu


class MainMenu:
    """The Start Page of the chess club app,
    displays the two options for player or tournament
    related menus"""
    def __init__(self):
        """MainMenu Constructor"""

        self.title = "Home"
        self.options = {
            "Player Menu": PlayerMenu,
            "Tournament Menu": TournamentMenu
        }
        self.show_main_menu()

    def show_main_menu(self):
        """Displays the Main Menu"""
        tools.cls()
        tools.print_logo()
        menu = chess_tournament_app.views.menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__)
        menu.print_menu()
        menu.user_action()
