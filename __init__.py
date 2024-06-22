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

green = "\033[0;32m"; red = "\033[31;49;1m"; blue = "\033[0;36m"; nocolor = "\\e[m"
#-----------------------------------------------------------------------------#

#-------------------------------Functions-------------------------------------#
# This function will echo the messages in the terminal.
def echo(arg: str):
    system(f'echo -e "{arg}"')


# This function will determine the input as True or False or InstallForAll or SkipForAll.
def yon(arg:str, assume=True, simple=True, default=False) -> bool:
    response = input(arg)

    if default and response == "": return True

    if simple: 
        if "y" in response: return True
        elif "n" in response: return False
        else:
            if assume:
                print("Couldn't understand, so assuming No.")
                return False
            else: yon(arg, assume=assume, simple=simple, default=default)
            # I don't want to make this recursive, but well, I won't use this much.

    if response == "iall": return "iall"

    elif response == "sall": return "sall"

    elif response == "skip" or response == "s": return False

    elif response == "install" or response == "i": return True

    else:
        if assume:
            print("Couldn't understand, so assuming No.")
            return False
        else: yon(arg, assume=assume, simple=simple, default=default)
        # Read line 39
    
# This function will verify if the user is correct.
def checkUser(warning=True, boolean=False) -> str:
    global home; global username
    if warning:
        echo(f"\nI found that your username is {green}{username}{nocolor}.\n" + 
             f"Note: It shouldn't be {red}root{nocolor}.\n"
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
def run(arg:str, possible_warning=""): #NOTES: MAKE AN REPEAT OPTION
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
pacman-key --recv-key 3056513887B78AEB 
pacman-key --lsign-key 3056513887B78AEB
pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'"""

chaoticRepo = """\n
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist"""


# This function will install ChaoticAUR (https://aur.chaotic.cx/) in pacman.
def chaoticAUR(check=False) -> bool:
    with open("/etc/pacman.conf", "r") as c: pacman_conf = c.read()

    if "chaotic-aur" in pacman_conf: return True

    if check: return False

    echo(f"{blue}\nInstalling Chaotic-AUR on your system.\n{nocolor}")

    run(chaoticScript)
    with open("/etc/pacman.conf", "w") as c: c.write(pacman_conf + chaoticRepo)

    system("pacman -Sy")


yayScript = f"""
git clone https://aur.archlinux.org/yay.git {dotPath}/yay
cd yay && makepkg -sirc
cd .. && rm -rf yay
"""

# This function will install an AUR helper, Yay (https://github.com/Jguer/yay), on the system.
def Yay(check=False) -> bool:
    yay = installPackage("yay", cache=False, check=True)

    if yay: return True

    if check: return False

    echo(f"\n{green}Installing Yay...\n{nocolor}")

    run("pacman -S base-devel")

    try:
        foo("pacman -Si yay", check=True, shell=True, capture_output=True)
        run("pacman -S yay")
    except: 
        run(yayScript)

    run("yay -Y --gendb")

# This is a helper to install dependencies.
def resolveDependency(dependency:str, check=False, method="pacman", needed=True): #Note: make an cache option
    if method == "pacman":
        return run(f"pacman -S {'--needed' if needed else ''} {dependency}")

    elif method == "yay":
        return run(f"yay -S {'--needed' if needed else ''} {dependency}")

    chaotic = chaoticAUR(check=True)
    yay = Yay(check=True)

    if chaotic and not yay:
        echo(f"\n{green}Found Chaotic-AUR on your system.")

        chaotic = yon(
            "Do you want to use Chaotic-AUR to install dependencies?(yes/no): ",
            assume=False
        )

        echo(f"{nocolor}")

        if chaotic: 
            if check: return "Chaotic-AUR"
            return run(f"pacman -S {'--needed' if needed else ''} {dependency}")

        else:
            echo(f"\n{green}Do you want to install Yay then?")
            yay = yon("Yes or No: ")
            echo(f"{nocolor}")

            if yay: 
                Yay() 
                if check: return "Yay"
                return run(f"yay -S {'--needed' if needed else ''} {dependency}")

            else:
                echo(f"\n{red}This script cannot proceed without Yay and Chaotic-AUR. So, aborting...{nocolor}")
                exit()
    
    if yay and not chaotic:
        echo(f"\n{green}Found Yay on your system.")

        yay = yon(
            "Do you want to use Yay to install dependencies?(yes/no): ",
            assume=False
        )

        echo(f"{nocolor}")

        if yay: return run(f"yay -S {'--needed' if needed else ''} {dependency}")

        else:
            echo(f"\n{green}Do you want to install Chaotic-AUR then?")
            chaotic = yon("Yes or No: ")
            echo(f"{nocolor}")

            if chaotic:
                chaoticAUR()
                return run(f"pacman -S {'--needed' if needed else ''} {dependency}")

            else:
                echo(f"\n{red}This script cannot proceed without Yay and Chaotic-AUR. So, aborting...{nocolor}")
                exit()
    
    if not chaotic and not yay:
        echo(
            f"\n{green}Look, I need to install some AUR packages.\n"
            "So, to install these packages I either need to add "
            "Chaotic-AUR repo in pacman mirrorlist or install yay on your system.\n"
            "Here's a quick comparision:\n    "
            "1. Chaotic-AUR method is very fast. "
            "Yay will take a lot of time to compile so many packages.\n    "
            "2. Which is reliable? Well, honestly I have never been fully successful with Yay\n"
        )

        variable = (input("So, which one would it be? Chaotic-AUR/Yay/Nothing: ")).lower()

        if "chaotic" in variable:
            chaoticAUR()
            if check: return "Chaotic-AUR"
            return run(f"pacman -S {'--needed' if needed else ''} {dependency}")
        
        if "yay" in variable:
            Yay()
            if check: return "Yay"
            return run(f"yay -S {'--needed' if needed else ''} {dependency}")
        
        if "nothing" in variable:
            echo(f"\n{red}Aborting...!{nocolor}\n")
            exit()


# This functions checks if the package is installed. If not, it will ask to install it.
def installPackage(package_name:str, cache=True, check=False) -> bool: # Seriously, I don't need this function.
    if cache:
        cachePath = Path(f"{home}/cache/{package_name}")
        if cachePath.exists(): 
            with open(f"{home}/cache/{package_name}") as package: 
                package = package.read()
                if "NO" in package: return False

    try: 
        foo("pacman -Qi {}".format(package_name), check=True, shell=True, capture_output=True)
        package = False
    except: 
        package = True

    if check: return not package
    
    if not package: return False
    
    package = yon(f"\n\nDo you want to install {package_name}?\nYes or No: ")
    if package:
        run(f"pacman -S {package_name}")
        return True
    else:
        if cache:
            print(f"Alright. Skipping {package_name}. Won't ask you again.")
            if not cachePath: (cachePath.parent).mkdir(parents=True, exist_ok=True)
            with open(f"{home}/cache/{package_name}", "w") as package: package.write("NO")


#-----------------------------------------------------------------------------#
