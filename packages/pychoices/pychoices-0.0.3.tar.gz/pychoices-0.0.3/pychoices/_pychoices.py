from pynput import keyboard
from ._colors import Colors

import os

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


    def styled_print(self, i, text, color, selector):
        print(f"{color}{selector} {text}{Colors.ENDC}")

    def print_choices(self, choices, chosen, color):
        for index, choice in enumerate(choices):
            use_color = color if index == chosen else Colors.ENDC
            use_selector = ">" if index == chosen else " "
            self.styled_print(index, choice, use_color, use_selector)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def update(self):
        self.clear()

        if self.label:
            print(f"{Colors.BOLD}{self.label}{Colors.ENDC}")

        self.print_choices(self.choices, self.choice, self.main_color)