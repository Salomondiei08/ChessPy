import os
import datetime

from chess_tournament_app.views import main_menu
from chess_tournament_app.views import player_menus
from chess_tournament_app.views import tournament_menus
from chess_tournament_app.controllers.database_operator import DatabaseOperator as Db


def print_logo():
    """Prints the ascii-logo"""
    logo = """
                              o   |\ ,'`. /||\ ,'`. /|    o     
      _   _   _   |\__      /\^/\ | `'`'`' || `'`'`' |  /\^/\   |\__     _   _   _ 
     | |_| |_| | /   o\__  |  /  ) \      /  \      /  |  /  ) /   o\__ | |_| |_| |
      \       / |    ___=' | /  /   |    |    |    |   | /  / |    ___=' \       / 
       |     |  |    \      Y  /    |    |    |    |    Y  /  |    \      |     |
       |     |   \    \     |  |    |    |    |    |    |  |   \    \     |     |  
       |     |    >    \    |  |    |    |    |    |    |  |    >    \    |     |  
      /       \  /      \  /    \  /      \  /      \  /    \  /      \  /       \ 
     |_________||________||______||________||________||______||________||_________|
         __         __       __       __        __       __       __         __   
        (  )       (  )     (  )     (  )      (  )     (  )     (  )       (  )  
         ><         ><       ><       ><        ><       ><       ><         ><   
        |  |       |  |     |  |     |  |      |  |     |  |     |  |       |  |  
       /    \     /    \   /    \   /    \    /    \   /    \   /    \     /    \ 
      |______|   |______| |______| |______|  |______| |______| |______|   |______|
   ____ _                     _____                                                 _   
  / ___| |__   ___  ___ ___  |_   _|__  _   _ _ __ _ __   __ _ _ __ ___   ___ _ __ | |_ 
 | |   | '_ \ / _ \/ __/ __|   | |/ _ \| | | | '__| '_ \ / _` | '_ ` _ \ / _ \ '_ \| __|
 | |___| | | |  __/\__ \__ \   | | (_) | |_| | |  | | | | (_| | | | | | |  __/ | | | |_ 
  \____|_| |_|\___||___/___/   |_|\___/ \__,_|_|  |_| |_|\__,_|_| |_| |_|\___|_| |_|\__|
                                                                                        
    """
    print(logo)


def cls():
    """Clears the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def date_today():
    """Returns current date in format: DD.MM.YYYY"""

    date = datetime.date.today().strftime("%d.%m.%Y")
    return date


def date_range(start_date, end_date):
    """Takes 2 dates and returns a list of all dates,
       from the start date to the end date"""

    s_date_obj = datetime.datetime.strptime(start_date, "%d.%m.%Y")
    e_date_obj = datetime.datetime.strptime(end_date, "%d.%m.%Y")

    delta = e_date_obj - s_date_obj

    days_list = []
    for date in range(delta.days + 1):
        day = s_date_obj + datetime.timedelta(days=date)
        days_list.append(datetime.datetime.strftime(day, "%d.%m.%Y"))
    return days_list


def valid_menu_choice(answer, opt_num):
    """Checks if the users choice is valid
       valid -> returns: True
       invalid -> returns: False"""

    try:
        if answer == "":
            return False
        elif int(answer) >= opt_num:
            return False
        else:
            return True
    except ValueError:
        print("     Enter the number of an option!")
        return False


def turn_back_to(current_class_name: str):
    """Turns back to the last Menu by calling the last Class before the current one.
       If current class = MainMenu -> it closes the Program"""

    if current_class_name == "MainMenu":
        cls()
        exit()
    elif current_class_name in ["PlayerMenu", "TournamentMenu"]:
        main_menu.MainMenu()

    elif current_class_name in [
        "AddNewPlayer",
        "ShowAllPlayers",
        "SearchPlayer",
    ]:
        player_menus.PlayerMenu()

    elif current_class_name in [
        "EditPlayer",
        "DeletePlayer",
        "EditOrDelete"
    ]:
        player_menus.SearchPlayer()

    elif current_class_name in [
        "NewTournament",
        "SelectPlayers",
        "ShowPlayers",
        "ShowTournaments",
        "SearchTournament",
        "PlayTournamentMenu",
        "DeleteTournament",
        "RunTournament"
    ]:
        tournament_menus.TournamentMenu()


def all_player_details(player):
    """Takes a player object and returns all
       (for the app user relevant) Details in a printable table"""

    player_details = (f"""
                     ID:          {player.doc_id}
                     First Name:  {player["first name"]}
                     Last Name :  {player["last name"]}
                     Birth Date:  {player["birth date"]}
                     Sex:         {player["sex"]}
                     Rating:      {player["rating"]}
        """)
    return player_details


def all_tournament_details(tournament):
    """Takes a tournament object and returns all
    relevant Details in a printable table"""

    ser_players = [Db().player_by_id(id_num) for id_num in tournament["players"]]
    player_name_list = [p["first name"] + " " + p["last name"] for p in ser_players]
    names = "\n"
    for name in player_name_list:
        names += f"                                    {name}\n"

    if len(tournament["date"]) > 1:
        dates = f'{tournament["date"][0]} - {tournament["date"][-1]}'
    else:
        dates = tournament["date"][0]

    if len(tournament["rounds"]) == 0:
        rounds = "No rounds played"

    else:
        rounds = ""
        for r in tournament["rounds"]:
            each_round = f"\n\n                         {r['name']}:\n"
            rounds += each_round
            for match in r["matches"]:
                each_match = f"""
                            {match[0][0]['first name'] + ' ' + match[0][0]['last name']
                            + ' vs ' + match[1][0]['first name'] + ' ' + match[1][0]['last name']
                            + ' | ' + str(match[0][1]) + ' : ' + str(match[1][1])}
            """
                rounds += each_match

    if not tournament["leaderboard"]:
        leaderboard = "No leader board available"
    else:
        leaderboard = readable_leaderboard(tournament["leaderboard"])

    tournament_details = (f"""
                     ID:            {tournament.doc_id}
                     Name:          {tournament["name"]}
                     Location:      {tournament["location"]}
                     Date(s):       {dates}
                     Nr. of Rounds: {tournament["number of rounds"]}
                     Time Control:  {tournament["time control"]}
                     Participants:  {names}
                     Description:   {tournament["description"]}\n
                     Rounds:        {rounds}
                     Leaderboard:   {leaderboard}
        """)

    return tournament_details


def readable_leaderboard(leaderboard: list):
    """Takes a sorted leaderboard and returns all
    players with their scores in a printable table

    Args:
        leaderboard: lists[player obj, score] in a list
    """

    spacer = "              "
    head = ["Pos.", "Name", "Score"]
    format_row = "{}{:<8}{:<20}{:<8}"
    format_head = format_row.format(spacer, *head)

    rows = []
    for (rank, ps) in enumerate(leaderboard, start=1):
        raw_row = [
            str(rank),
            f"{ps[0]['first name']} {ps[0]['last name']}",
            str(ps[1])
        ]
        rows.append(raw_row)

    format_rows = f"\n\n{spacer}{format_head}\n"
    for row in rows:
        f_row = spacer + format_row.format(spacer, *row)
        format_rows += f"\n{f_row}"

    return format_rows


def valid_date(date_text):
    """Checks if a date String is in a valid format and returns False or True"""

    try:
        datetime.datetime.strptime(date_text, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def valid_sex(sex_text):
    """Checks if a string is m or f and returns False or True"""

    if sex_text == "F" or sex_text == "M":
        return True
    else:
        return False


def valid_rating(number_string):
    """Checks if number is valid, not negative, int or float
       and returns False or True"""

    try:
        if int(number_string) >= 0:
            return True
        else:
            return False

    except ValueError:
        print("\n                     It has to be a 0 or positive number!")
        return False


def valid_int(number_string):
    """Checks if number is a valid id, int > 1
           and returns False or True"""

    try:
        if int(number_string) > 0:
            return True
        else:
            return False

    except ValueError:
        return False


def valid_player_number(player_num: str, number_of_rounds: int):
    """Checks if a number-string is valid for a number of players
    in a tournament"""
    available_players = len(Db().database.players_table)

    try:
        number = int(player_num)
        if number >= number_of_rounds + 1 and number % 2 == 0:
            return True

        elif number > available_players:
            print(f"\n                     Only {available_players} "
                  f"Players in database!")
            return False

        else:
            return False

    except ValueError:
        return False


def valid_tournament_id(tournament_id: str):
    """Takes an int - string and checks if it's a valid
    or existing doc_id for a tournament """
    all_tournament_ids = [
        t.doc_id for t in Db().database.tournaments_table.all()
        if not t["deleted"]
    ]

    try:
        number = int(tournament_id)
        if number in all_tournament_ids:
            return True

        else:
            return False

    except ValueError:
        return False
