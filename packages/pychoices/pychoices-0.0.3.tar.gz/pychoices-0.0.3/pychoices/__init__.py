import os
import time
import cursor
from ._colors import Colors
from ._pychoices import PyChoices

from pynput import keyboard

CONTROLLER = keyboard.Controller()

def ask(*args, **kwargs):
    """Returns a tuple (index, value) from the selected option between the provided
    choices.
    Arguments:
        The choices available.
    Keyword Arguments:
        label -- a string to be printed along the form
        color -- the color of the current selected option
    """
    cursor.hide()

    pychoice = PyChoices(
        args,
        kwargs.get("label", None),
        kwargs.get("color", Colors.OKGREEN)
    )

    input()
    os.system('cls' if os.name == 'nt' else 'clear')

    cursor.show()

    return (pychoice.choice, pychoice.choices[pychoice.choice])

if __name__ == "__main__":
    food = ask("Pizza", "Hamburger", "Fries", label="Favorite Food")

    print(food)