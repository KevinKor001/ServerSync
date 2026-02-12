import lib.questionary as qs
import os


def clear():
    os.subprocess('cls' if os.name == 'nt' else 'clear')


class setupMenu:
    @staticmethod
    def main():
        
        print("Welcome... Setup Global Config:")
        sel = qs.select("Add Server", "Save Global Config")






def initialSetup():
    setupMenu.main() 

