"""
This is just a helper for me to quickly setup my minimalistic Arch.
This will automatically install dotfiles for few Window Managers.
You can use it too. I have added a few dotfiles, you can choose any."""

#---------------------------------IMPORTS-------------------------------------#
from sys import exit
#-----------------------------------------------------------------------------#


#-------------------------------CONSTANTS----------------------------------#
repoList = """
1. linuxmobile_hyprland-dotfiles"""
#--------------------------------------------------------------------------#


#-----------------------------Script---------------------------#


# This function will determine the input as True or False.
def yon(arg):
    return True if "y" in arg else False

print("Welcome! This will help you setup your Window Manager for your Arch Linux.\n"
      "PS: You can always abort the script by using Ctrl + C")

archInstalled = yon(input("\nHave you installed base package for Arch Linux and set it up?\n"
                          "Yes or No: "))

if not archInstalled: 
    print("\nSorry, this script will not help setup the base Arch Linux.\n"
          "Come back after setting up Arch.")
    exit()

print("\nCool. Now, tell me which one do you choose?")
repoChoice = input(repoList)
