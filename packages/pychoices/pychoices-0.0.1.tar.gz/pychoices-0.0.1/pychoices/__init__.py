import os
import time
import cursor

from pynput import keyboard

CONTROLLER = keyboard.Controller()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PyChoices(object):
    def __init__(self, choices, label, main_color):
        self.choices = choices
        self.label = label
        self.main_color = main_color
        self.choice = 0
        self.stop = False

        self.listener = keyboard.Listener(
            on_press=self._key_press,
            on_release=self._key_release
        )

        self.listener.start()

        self.update()

    def _key_press(self, key):
        if key == keyboard.Key.enter:
            self.listener.stop()
            self.stop = True
            return

        self.update()

    def _key_release(self, key):

        if key == keyboard.Key.up:
            self.choice -= 1
        elif key == keyboard.Key.down:
            self.choice += 1

        self.choice %= len(self.choices)

        self.update()


    def styled_print(self, i, text, color):
        print(f"{color}[{i}] {text}{Colors.ENDC} ")

    def print_choices(self, choices, chosen, color):
        for index, choice in enumerate(choices):
            use_color = color if index == chosen else Colors.ENDC
            self.styled_print(index, choice, use_color)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def update(self):
        self.clear()

        if self.label:
            print(self.label)

        self.print_choices(self.choices, self.choice, self.main_color)

def ask(*args, **kwargs):
    cursor.hide()

    pychoice = PyChoices(
        args,
        kwargs.get("label", None),
        kwargs.get("color", Colors.OKBLUE)
    )

    input()
    os.system('cls' if os.name == 'nt' else 'clear')

    cursor.show()

    return (pychoice.choice, pychoice.choices[pychoice.choice])

if __name__ == "__main__":
    food = ask("Pizza", "Hamburger", "Fries", label="Favorite Food")

    print(food)