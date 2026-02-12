from typing import NamedTuple
import lib.questionary as questionary 
from pathlib import Path
import re
import json
from lib.questionary.prompts import text
class NodeResult(NamedTuple):
    found: bool
    path: str | None
    matches: list | None


def save_config(data, filename=".SyncNode.config"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Config saved to {filename}")
class menu:
    @staticmethod
    def run_setup_wizard():
    
        answers = questionary.form(
            protocol=questionary.select(
                "Select a protocol:",
                choices=["FTP"],
            ),
            
            ip=questionary.text(
                    "Enter Server IP:", validate=lambda text: True if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", text) else "Enter a Vaid IP"
                ),
            port=questionary.text(
                    "Enter Server Port:",
                    ),
            user=questionary.text(
                    "Enter Server user:",
                    ),
            password=questionary.text(
                    "Enter user password:",
                    ),

            directory=questionary.text("Enter Server Directory Target")





        ).ask()

        save_config(answers)

        print("Writing to .SyncNode.config")



    def main():
        print("Checking for existing SyncNode Config")
        result = checkForNode(".")
        match result:
            case NodeResult(found=True):
                if result.matches and len(result.matches) > 1:
                    print("Warning , more than 1 instances of SyncNode configs were found!")
                            
                    for path in result.matches:
                        print("Config @",path)
                    print(" ")
                    print("Fix configs or run ServerSync -fix-config <dir>")
                    exit()

                else:
                    print("Found a existing SyncNode Configuration!")
                    print("Run ServerSync config")
                    exit()


            case NodeResult(found=False):
                print("Clean Dir, Moving on...")
                menu.run_setup_wizard()











def checkForNode(path):
    search = list(Path(path).rglob(".SyncNode.config"))
    if search:
         #   print(NodeResult(True, path, search))

        return NodeResult(True, path, search)
    else:

          #  print(NodeResult(False, None, None))


        return NodeResult(False, None, None)





def begin():
    menu.main()



