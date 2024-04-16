"""
This script will help install https://github.com/linuxmobile/hyprland-dots
on your Arch Linux."""

#---------------------------------IMPORTS-------------------------------------#
from sys import exit
from os import system
from __init__ import echo, run, yon, chaoticAUR
#-----------------------------------------------------------------------------#

#-------------------------------CONSTANTS----------------------------------#
pacman_dependencies = (
"hyprland waybar wayland dunst nwg-look wf-recorder wlsunset rsync "
"colord ffmpegthumbnailer gnome-keyring gtk-engine-murrine imagemagick kvantum pamixer playerctl " 
"polkit-kde-agent qt5-quickcontrols qt5-quickcontrols2 qt5-wayland qt6-wayland ttf-font-awesome tumbler ttf-jetbrains-mono "
"xdg-desktop-portal-hyprland xdotool cliphist qt5-imageformats qt5ct "
"btop neofetch noise-suppression-for-voice  rofi-emoji starship zsh viewnior "
"cava rofi-lbonn-wayland ocs-url hyprpicker wlogout grimblast swww ttf-icomoon-feather "
"brave-bin file-roller noto-fonts noto-fonts-cjk noto-fonts-emoji thunar thunar-archive-plugin "
"catppuccin-gtk-theme-macchiato catppuccin-gtk-theme-mocha papirus-icon-theme sddm swaylock-effects kvantum "
"pipewire pipewire-alsa pipewire-audio pipewire-pulse pipewire-jack wireplumber gst-plugin-pipewire pavucontrol"
)

green = "\033[0;32m"; red = "\033[0;31m"; blue = "\033[0;36m"; nocolor = "\e[m"
#--------------------------------------------------------------------------#

#-----------------------------Script Start---------------------------#

Welcome = f"""
This script will help you download and setup your Hyprland Window Manager.
The script will continue in the following steps:
{green}
1. It will add a repo Chaotic-AUR if needed.
2. It will install all the dependencies.
3. It will write the needed config for Hyprland.{nocolor}"""

echo(Welcome)

# Let's add a repo Chaotic-AUR.

chaoticAUR()

# Let's move on to installing dependencies.

echo(f"\n\n{blue}Installing Dependencies...")
echo(f"(you can edit the dependencies as you want in the arch_dotfiles/linuxmobile_hyprland-dots){nocolor}\n")

run(f"pacman -S --needed {pacman_dependencies}")

# Let's configure the dotfiles.

run('cd "$HOME"/Downloads/linuxmobile_hyprland-dots && '
    "rsync -avxHAXP --exclude '.git*' ./* ~/")

# The final words.

echo(f"""
{green}Everything is set up! Now, you can enjoy your Hyprland.
To quickly login to Hyprland, use the command {blue}Hyprland.
{green}I recommend you to configure {red}sddm{green}.{nocolor}"""
)

#-----------------------------Script End-----------------------------#
