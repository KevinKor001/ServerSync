import os


def clear():
    os.subprocess('cls' if os.name == 'nt' else 'clear')


