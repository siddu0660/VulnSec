#!/bin/bash

if ! systemctl is-active --quiet clamav-daemon; then
    echo -e "\033[31;1m[Error]\033[0m ClamAV daemon (clamd) is not running!"
    echo "Start it using: sudo systemctl start clamav-daemon"
    exit 1
fi

read -p 'Enter the directory to scan: ' SCAN_DIR
SCAN_DIR=$(echo "$SCAN_DIR" | sed 's|^~|'"$HOME"'|')

if [[ ! -d "$SCAN_DIR" ]]; then
    echo -e "\033[31;1m[Error]\033[0m Directory does not exist: $SCAN_DIR"
    exit 1
fi

command="clamdscan"

while true; do
    echo -e "\nSelect scan categories (separate choices with spaces):"
    echo "1. General Scan Options"
    echo "2. File Handling Options"
    echo "3. Performance & Access Control"
    echo "4. Debugging & Logging"
    echo "5. Exit & Run Scan"

    read -p 'Enter choice: ' input
    choices=$(echo "$input" | tr ',' ' ')

    for choice in $choices; do
        case "$choice" in
            1)
                echo -e "\nGeneral Scan Options:"
                echo "1. Recursive Scan (-r)"
                echo "2. Show Only Infected Files (-i)"
                echo "3. Scan Symbolic Links (--follow-dir-symlinks)"
                echo "4. Reload ClamAV Database Before Scan (--reload)"
                echo "5. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) command+=" -r" ;;
                        2) command+=" -i" ;;
                        3) command+=" --follow-dir-symlinks" ;;
                        4) command+=" --reload" ;;
                        5) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            2)
                echo -e "\nFile Handling Options:"
                echo "1. Move Infected Files (--move=DIR)"
                echo "2. Copy Infected Files (--copy=DIR)"
                echo "3. Exclude Files (--exclude=PATTERN)"
                echo "4. Exclude Directories (--exclude-dir=PATTERN)"
                echo "5. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) 
                            read -p 'Enter directory to move infected files: ' move_dir
                            move_dir=$(realpath "$move_dir")
                            command+=" --move=$move_dir" ;;
                        2)
                            read -p 'Enter directory to copy infected files: ' copy_dir
                            copy_dir=$(realpath "$copy_dir")
                            command+=" --copy=$copy_dir" ;;
                        3)
                            read -p 'Enter file pattern to exclude: ' exclude_pattern
                            command+=" --exclude=$exclude_pattern" ;;
                        4)
                            read -p 'Enter directory pattern to exclude: ' exclude_dir
                            command+=" --exclude-dir=$exclude_dir" ;;
                        5) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            3)
                echo -e "\nPerformance & Access Control:"
                echo "1. Pass File Descriptor to Clamd (--fdpass)"
                echo "2. Disable Verbose Output (--no-summary)"
                echo "3. Max File Size (--max-filesize=SIZE)"
                echo "4. Max Scan Size (--max-scansize=SIZE)"
                echo "5. Max Recursion Depth (--max-recursion=NUMBER)"
                echo "6. Max Number of Files (--max-files=NUMBER)"
                echo "7. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) command+=" --fdpass" ;;
                        2) command+=" --no-summary" ;;
                        3) 
                            read -p 'Enter maximum file size (e.g., 10M): ' max_filesize
                            command+=" --max-filesize=$max_filesize" ;;
                        4)
                            read -p 'Enter maximum scan size (e.g., 100M): ' max_scansize
                            command+=" --max-scansize=$max_scansize" ;;
                        5)
                            read -p 'Enter max recursion depth: ' max_recursion
                            command+=" --max-recursion=$max_recursion" ;;
                        6)
                            read -p 'Enter max number of files to scan: ' max_files
                            command+=" --max-files=$max_files" ;;
                        7) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            4)
                echo -e "\nDebugging & Logging:"
                echo "1. Enable Debug Mode (--debug)"
                echo "2. Enable Heuristic Alerts (--heuristic-alerts)"
                echo "3. Detect Potentially Unwanted Apps (--detect-pua)"
                echo "4. Log Output to a File (--log=FILE)"
                echo "5. Back to Main Menu"
                read -p 'Enter choice: ' sub_input
                sub_choices=$(echo "$sub_input" | tr ',' ' ')
                for sub_choice in $sub_choices; do
                    case "$sub_choice" in
                        1) command+=" --debug" ;;
                        2) command+=" --heuristic-alerts" ;;
                        3) command+=" --detect-pua" ;;
                        4) 
                            read -p 'Enter log file path: ' log_file
                            log_file=$(realpath "$log_file")
                            command+=" --log=$log_file" ;;
                        5) break ;;
                        *) echo "Invalid choice: $sub_choice" ;;
                    esac
                done
                ;;

            5)
                echo -e "\nExecuting ClamDScan with options:"
                echo "$command \"$SCAN_DIR\""
                eval "$command \"$SCAN_DIR\""
                exit 0
                ;;

            *) echo "Invalid choice: $choice" ;;
        esac
    done
done
