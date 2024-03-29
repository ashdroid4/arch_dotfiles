"""
This is just a helper for me to quickly setup my minimalistic Arch.
This will automatically install dotfiles for few Window Managers.
You can use it too. I have added a few dotfiles, you can choose any."""

#---------------------------------IMPORTS-------------------------------------#
from sys import exit
#-----------------------------------------------------------------------------#


#-------------------------------CONSTANTS----------------------------------#
repoList = { 
"linuxmobile_hyprland-dots":"https://github.com/linuxmobile/hyprland-dots"
}
#--------------------------------------------------------------------------#


#-----------------------------Script Start---------------------------#

print("Welcome! This will help you setup your Window Manager for your Arch Linux.\n"
      "PS: You can always abort the script by using Ctrl + C")

# This function will determine the input as True or False.
def yon(arg):
    return True if "y" in arg else False

archInstalled = yon(input("\nHave you installed base package for Arch Linux and set it up?\n"
                          "Yes or No: "))

if not archInstalled: 
    print("\nSorry, this script will not help setup the base Arch Linux.\n"
          "Come back after setting up Arch.")
    exit()

# This function will help choose which repo to go for.
def repoChoose():
    n=1; print("\nCool. Now, tell me which one do you choose?")
    for i in repoList:
        print(f"\n{n}. {i}({repoChoose[i]})"); n+=1
        
    while True:
        repoChoose = input("\nSo, which one do you choose to install? Say in numbers: ")
        if not repoChoose.isdigit(): print("Please, type a number.")
        if 0 < int(repoChoose) > n: print("Please put a valid number.")
        break

    templist = [i for i in repoList]
    repoChoose = repoList[repoChoose - 1]

    print("Cool, so you choose ", repoChoose)

#-----------------------------Script End-----------------------------#
