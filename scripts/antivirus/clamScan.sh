#!/bin/bash

read -p 'Enter the directory to scan: ' SCAN_DIR
SCAN_DIR=$(echo "$SCAN_DIR" | sed 's|^~|'"$HOME"'|')

if [[ ! -d "$SCAN_DIR" ]]; then
    echo -e "\033[31;1m[Error]\033[0m Directory does not exist: $SCAN_DIR"
    exit 1
fi

command="clamscan"

while true; do
    echo -e "\nSelect scan categories (separate choices with spaces):"
    echo "1. General Scan Options"
    echo "2. File Handling Options"
    echo "3. Performance & Limits"
    echo "4. Heuristics & Security"
    echo "5. Exit & Run Scan"

    read -p 'Enter choice: ' input
    choices=$(echo "$input" | tr ',' ' ')

    for choice in $choices; do
        case "$choice" in
            1)
                echo -e "\nGeneral Scan Options:"
                echo "1. Recursive Scan (-r)"
                echo "2. Show Only Infected Files (-i)"
                echo "3. Scan Archives (--scan-archive)"
                echo "4. Scan Emails (--scan-mail)"
                echo "5. Scan PDFs (--scan-pdf)"
                echo "6. Scan HTML (--scan-html)"
                echo "7. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) command+=" -r" ;;
                        2) command+=" -i" ;;
                        3) command+=" --scan-archive" ;;
                        4) command+=" --scan-mail" ;;
                        5) command+=" --scan-pdf" ;;
                        6) command+=" --scan-html" ;;
                        7) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;
            
            2)
                echo -e "\nFile Handling Options:"
                echo "1. Delete Infected Files (--remove)"
                echo "2. Move Infected Files (--move=DIR)"
                echo "3. Copy Infected Files (--copy=DIR)"
                echo "4. Exclude Files (--exclude=PATTERN)"
                echo "5. Exclude Directories (--exclude-dir=PATTERN)"
                echo "6. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) command+=" --remove" ;;
                        2) 
                            read -p 'Enter directory to move infected files: ' move_dir
                            move_dir=$(realpath "$move_dir")
                            command+=" --move=$move_dir" ;;
                        3)
                            read -p 'Enter directory to copy infected files: ' copy_dir
                            copy_dir=$(realpath "$copy_dir")
                            command+=" --copy=$copy_dir" ;;
                        4)
                            read -p 'Enter file pattern to exclude: ' exclude_pattern
                            command+=" --exclude=$exclude_pattern" ;;
                        5)
                            read -p 'Enter directory pattern to exclude: ' exclude_dir
                            command+=" --exclude-dir=$exclude_dir" ;;
                        6) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            3)
                echo -e "\nPerformance & Limits:"
                echo "1. Max File Size (--max-filesize=SIZE)"
                echo "2. Max Scan Size (--max-scansize=SIZE)"
                echo "3. Max Recursion Depth (--max-recursion=NUMBER)"
                echo "4. Max Number of Files (--max-files=NUMBER)"
                echo "5. Quiet Mode (--quiet)"
                echo "6. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) 
                            read -p 'Enter maximum file size (e.g., 10M): ' max_filesize
                            command+=" --max-filesize=$max_filesize" ;;
                        2)
                            read -p 'Enter maximum scan size (e.g., 100M): ' max_scansize
                            command+=" --max-scansize=$max_scansize" ;;
                        3)
                            read -p 'Enter max recursion depth: ' max_recursion
                            command+=" --max-recursion=$max_recursion" ;;
                        4)
                            read -p 'Enter max number of files to scan: ' max_files
                            command+=" --max-files=$max_files" ;;
                        5) command+=" --quiet" ;;
                        6) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            4)
                echo -e "\nHeuristics & Security:"
                echo "1. Enable Heuristic Alerts (--heuristic-alerts)"
                echo "2. Detect Potentially Unwanted Apps (--detect-pua)"
                echo "3. Detect Phishing (--phishing-sigs)"
                echo "4. Detect Phishing via SSL (--phishing-ssl)"
                echo "5. Detect Phishing Cloaks (--phishing-cloak)"
                echo "6. Block Encrypted Archives (--block-encrypted)"
                echo "7. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) command+=" --heuristic-alerts" ;;
                        2) command+=" --detect-pua" ;;
                        3) command+=" --phishing-sigs" ;;
                        4) command+=" --phishing-ssl" ;;
                        5) command+=" --phishing-cloak" ;;
                        6) command+=" --block-encrypted" ;;
                        7) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            5)
                echo -e "\nExecuting ClamAV scan with options:"
                echo "$command \"$SCAN_DIR\""
                eval "$command \"$SCAN_DIR\""
                exit 0
                ;;

            *) echo "Invalid choice: $choice" ;;
        esac
    done
done
