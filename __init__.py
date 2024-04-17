"""
This is init file for arch_dotfiles"""

#---------------------------------IMPORTS-------------------------------------#
import typing
from pathlib import Path
from os import system, getenv
from subprocess import run as foo
#-----------------------------------------------------------------------------#

#-------------------------------CONSTANTS-------------------------------------#
dotPath = Path.cwd()
username = getenv("username")
home = Path(f'/home/{username}')

green = "\033[0;32m"; red = "\033[31;49;1m"; blue = "\033[0;36m"; nocolor = "\e[m"
#-----------------------------------------------------------------------------#

#-------------------------------Functions-------------------------------------#
# This function will echo the print the messages in the terminal.
def echo(arg: str):
    system(f'echo -e "{arg}"')


# This function will determine the input as True or False or YesForAll.
def yon(arg:str, simple=True, default=False) -> bool:
    response = input(arg)

    if default and response == "": return True

    if simple: 
        if "y" in response: return True
        elif "n" in response: return False
        else:
            print("Couldn't understand, so assuming No.")
            return False

    if response == "iall": return "iall"

    elif response == "sall": return "sall"

    elif response == "skip" or response == "s": return False

    elif response == "install" or response == "i": return True

    else:
        print("Couldn't understand, so assuming No.")
        return False
    
# This function will verify if the user is correct.
def checkUser(warning=True, boolean=False) -> str:
    global home; global username
    if warning:
        echo(f"\nI found that your username is {green}{username}{nocolor}.\n" + 
             f"Note: It shouldn't be {green}root{nocolor}.\n"
        )

    checkUser =  yon("Is the username correct? Yes or No(default=Yes): ", default=True)

    if not checkUser:
        while True:
            username = (input("Please enter your username: ")).strip()
            if username:
                checkUser =  yon(f"Is the username, '{username}', correct? Yes or No: ", default=True)
                if checkUser:
                    from __init__ import Path
                    home = Path(f'/home/{username}')
                    hyprlandConfPath = home.joinpath('.config', 'hypr', 'hyprland.conf')
                    break
                else: print("Everyone makes mistakes.")
            else: print("The input was empty.")
        if boolean: return home, username, False
    if boolean: return home, username, True

    return home, username


# Just modifying the subprocess.run() to give desired outputs.
def run(arg:str, possible_warning=""):
    try: 
        print(f"\n\nExecuting [{arg}]\n")
        foo(arg, shell=True, check=True) # This foo is subprocess.run()
    except Exception:
        echo(f"\n\n{red}While executing the command {nocolor}'{arg}'{red}, the above error occured.{nocolor}")
        proceed = (
                "\nWell, I can't possibly know what error you enountered. #"
                "If you don't want to proceed, the script will abort.\n"
                "Do you want to proceed? Yes or No: "
            )
        
        warning = f"But maybe... {possible_warning}. "
        proceed = proceed.replace("#", warning) if possible_warning else proceed.replace("#", possible_warning)

        proceed = yon(proceed)

        if not proceed: 
            print("Okay, aborted!")
            exit()

chaoticScript = """
pacman-key --init
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'"""

chaoticRepo = """\n
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist"""


# This function will install ChaoticAUR (https://aur.chaotic.cx/) in pacman 
def chaoticAUR():
    with open("/etc/pacman.conf", "r") as c: pacman_conf = c.read()

    if "chaotic-aur" in pacman_conf: return

    echo(f"\n\n{blue}Now, I have to install all the dependencies. To do this, I have to add another repo called Chaotic-Aur.\n"
         f"I am very lazy so you have to say yes or the installation will abort.{nocolor}")

    ChaoticAUR = yon("\nDo you want to add Chaotic-Aur? "
                     "Yes or No: ")

    if not ChaoticAUR: exit()

    run(chaoticScript)
    with open("/etc/pacman.conf", "w") as c: c.write(pacman_conf + chaoticRepo)

    system("pacman -Sy")

#-----------------------------------------------------------------------------#
