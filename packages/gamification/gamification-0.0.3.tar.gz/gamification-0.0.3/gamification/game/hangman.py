from random import randint
import pkg_resources
import os
import sys


class Hangman:
    def __init__(self):
        self._word = None
        self._hidden = None

    def play(self):
        self._random()
        self._hide()

        win = False
        left = self._hidden.count("_")
        used = set()

        self.clear()
        print("HANGMAN")
        print("-" * 20)
        while "_" in self._hidden:
            print(
                "Word: {}\nUsed: {}\nLeft: {}".format(
                    " ".join(list(self._hidden)), ", ".join(used), left
                )
            )
            ch = input(
                "\nGuess a char: (!w if you want to enter the whole word) "
            ).strip()
            if ch == "!w":
                word = input("Enter the word: ")
                if word != self._word:
                    break

            ch = ch.upper()
            if ch in self._word and not ch in self._hidden:
                self._hidden = "".join(
                    [
                        self._word[i]
                        if (i == 0 or i == len(self._word) - 1)
                        or self._word[i] == ch
                        or self._hidden[i] != "_"
                        else "_"
                        for i in range(len(self._word))
                    ]
                )
            elif ch in self._hidden:
                continue
            else:
                used.add(ch.upper())
                left -= 1

            if left == 0:
                break

            if self._hidden == self._word:
                win = True
                break

        if not win:
            print("Sorry, you loose!")
        else:
            print("Congrats!")

    def reset(self):
        self._random()
        self._hide()

    def _random(self):

        words = []
        path = "/files/words.txt"
        content = pkg_resources.resource_string(__name__, path)
        words.extend(content.decode("utf-8").split("\n"))

        self._word = words[randint(0, len(words) - 1)].strip().upper()

    def _hide(self):
        self._hidden = "".join(
            [
                ch if ch == self._word[0] or ch == self._word[-1] else "_"
                for ch in self._word
            ]
        )

    def clear(self):
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
