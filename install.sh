## Hey, welcome! This is the start point of arch_dotfiles.

## Checking if the user is sudo. We don't want this script to be run with sudo.
if [[ $EUID -eq 0 ]]; then
    echo "This script should not be run with sudo."
    exit 1
fi

## Now it is the time to set one environment variable.
export username=$(whoami)

## Installing some basic dependencies.
sudo pacman -S --needed python3 git

## Changing to the directory where the file resides.
cd "$( dirname "${BASH_SOURCE[0]}" )"

## Starting the main script.
python3 script
