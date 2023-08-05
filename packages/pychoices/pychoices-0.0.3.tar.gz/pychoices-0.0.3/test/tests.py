from unittest import TestCase, main
from pychoices import ask
from pynput import keyboard

class PyChoicesTestCase(TestCase):
    def test_must_accept_integers(self):
        cont = keyboard.Controller()
        cont.press(keyboard.Key.enter)
        result = ask(1, 2, 3)
        cont.release(keyboard.Key.enter)

        self.assertEquals(result[0], 0)

    def test_must_accept_string(self):
        cont = keyboard.Controller()
        cont.press(keyboard.Key.enter)
        result = ask("1", "2", "3")
        cont.release(keyboard.Key.enter)

        self.assertEquals(result[0], 0)

    def test_must_return_tuple(self):
        cont = keyboard.Controller()
        cont.press(keyboard.Key.enter)
        result = ask(1, 2, 3)
        cont.release(keyboard.Key.enter)

        self.assertIsInstance(result, tuple)

if __name__ == "__main__":
    main()