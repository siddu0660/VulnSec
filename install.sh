#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

declare -A tools_check_commands
tools_check_commands=(
    [Git]="git --version"
    [Node.js]="node -v"
    [npm]="npm -v"
    [Python]="python3 --version"
    [pip]="pip3 --version"
    [Docker]="docker --version"
    [Curl]="curl --version"
    [Wget]="wget --version"
)

declare -A tools_install_commands
tools_install_commands=(
    [Git]="sudo apt-get install git -y"
    [Node.js]="curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - && sudo apt-get install -y nodejs"
    [npm]="sudo apt-get install -y npm"
    [Python]="sudo apt-get install -y python3"
    [pip]="sudo apt-get install -y python3-pip"
    [Docker]="sudo apt-get install -y docker.io"
    [Curl]="sudo apt-get install -y curl"
    [Wget]="sudo apt-get install -y wget"
)

declare -A tools_status

check_tools() {
    for tool in "${!tools_check_commands[@]}"; do
        if ${tools_check_commands[$tool]} &>/dev/null; then
            tools_status[$tool]=true
        else
            tools_status[$tool]=false
        fi
    done
}

print_line() {
    echo -e "${CYAN}=========================================${RESET}"
}

display_checklist() {
    clear
    print_line
    echo -e "${GREEN}Dependency Installer Checklist${RESET}"
    print_line
    for tool in "${!tools_status[@]}"; do
        if [ "${tools_status[$tool]}" = true ]; then
            echo -e "[${GREEN}✔${RESET}] $tool"
        else
            echo -e "[${RED}✘${RESET}] $tool"
        fi
    done
    print_line
}

prompt_multiple_choices() {
    echo -e "${YELLOW}Select the tools you want to install (separate numbers with spaces):${RESET}"
    local options=()
    local i=1
    for tool in "${!tools_status[@]}"; do
        options+=("$tool")
        echo "$i. $tool"
        ((i++))
    done
    echo "$i. Quit"

    read -p "Enter your choices: " -a choices
    for choice in "${choices[@]}"; do
        if ((choice > 0 && choice <= ${#options[@]})); then
            tool="${options[choice-1]}"
            if [ "${tools_status[$tool]}" = false ]; then
                echo -e "${BLUE}Installing $tool...${RESET}"
                eval "${tools_install_commands[$tool]}"
                tools_status[$tool]=true
                echo -e "${GREEN}$tool has been installed successfully!${RESET}"
            else
                echo -e "${YELLOW}$tool is already installed. Skipping.${RESET}"
            fi
        elif ((choice == i)); then
            echo -e "${YELLOW}Exiting the script. Goodbye!${RESET}"
            exit 0
        else
            echo -e "${RED}Invalid choice: $choice${RESET}"
        fi
    done
}

check_tools
while true; do
    display_checklist
    prompt_multiple_choices
    echo -e "${GREEN}Installation round complete!${RESET}"
    read -p "Press Enter to return to the checklist or type 'q' to quit: " response
    if [ "$response" = "q" ]; then
        echo -e "${YELLOW}Exiting the script. Goodbye!${RESET}"
        break
    fi
done
