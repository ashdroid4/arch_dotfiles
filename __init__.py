import typing
from os import system
from subprocess import run as foo

green = "\033[0;32m"; red = "\033[0;31m"; blue = "\033[0;36m"; nocolor = "\e[m"

# This function will echo the print the messages in the terminal.
def echo(arg: str):
    system(f'echo -e "{arg}"')


# This function will determine the input as True or False or YesForAll.
def yon(arg:str, simple=True) -> bool:
    response = input(arg)

    if simple: return True if "y" in response else False

    if "yes" or "y" in response: return "true"

    if response == "skip" or response == "s": return "false"

    if "all" in response: return "all"


# Just modifying the subprocess.run() to give desired outputs.
def run(arg:str):
    try: 
        print(f"\n\nExecuting [{arg}]\n")
        foo(arg, shell=True, check=True) # This foo is subprocess.run()
    except Exception:
        echo(f"\n\n{red}While executing the command {nocolor}'{arg}'{red}, the above error occured.{nocolor}")
        proceed = yon(
                "\nWell, I can't possibly know what error you enountered. "
                "If you don't want to proceed, the script will abort.\n"
                "Do you want to proceed? Yes or No: "
            )
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
