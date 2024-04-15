# Hey, welcome! This is the start-point of arch_dotfiles

## Checking if the user is sudo. We don't want this script to be run with sudo.
check_not_sudo() {
    if [[ $EUID -eq 0 ]]; then
        echo "This script should not be run with sudo."
        return 1
    fi
}

check_not_sudo 

## Now it is the time to set one environment variable.
export username=$(whoami)

## Installing some basic dependencies.
sudo pacman -S --needed python3 git

## Starting the main script.
python3 script
