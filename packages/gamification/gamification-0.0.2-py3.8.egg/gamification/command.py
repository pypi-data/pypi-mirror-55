from gamification.game.tic_tac_toe import TicTacToe
from gamification.game.hangman import Hangman

GAMES = {
    TicTacToe: ["tic_tac_toe", "ttc", "Tic-Tac-Toe", "tic-tac-toe"],
    Hangman: ["hangman", "hn", "Hangman"],
}


def exec(game):
    global GAMES

    new_game = None
    for cls_, names in GAMES.items():
        if game in names:
            new_game = cls_()
            break

    if not new_game:
        raise ValueError("Game with name '{}'' doesn't exist. Possible options are: '{}'".format(game, ", ".join([game[0] for game in GAMES.values()])))

    new_game.play()
    answer = input("Do you want another game? [yN] ")
    while answer.lower() in ["y", "yes"]:
        new_game.reset()
        new_game.play()
        answer = input("Do you want another game? [yN] ")
