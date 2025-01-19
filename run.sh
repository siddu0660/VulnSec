#!/bin/bash

# clear
# mkdir vulsec
clear 
echo -e '\033[31;1m 
██╗   ██╗██╗   ██╗██╗     ███████╗███████╗ ██████╗
██║   ██║██║   ██║██║     ██╔════╝██╔════╝██╔════╝
██║   ██║██║   ██║██║     ███████╗█████╗  ██║     
╚██╗ ██╔╝██║   ██║██║     ╚════██║██╔══╝  ██║     
 ╚████╔╝ ╚██████╔╝███████╗███████║███████╗╚██████╗
  ╚═══╝   ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝

\033[33;4mCTRL+C:\033[0m exit \n'

if [[ $EUID -ne 0 ]]; then
    echo "This script should be executed as root! Exiting......."
    exit 1
fi

read -p $'Have you already run \033[33;1minstall.sh\033[0m ? (yes/no) : ' confirm
if [[ "$confirm" != "yes" && "$confirm" != "y" ]]; then
    echo -e "\033[31;1m[Exiting]\033[0m Please run 'install.sh' before executing this script."
    exit 1
fi

echo "Exiting......."