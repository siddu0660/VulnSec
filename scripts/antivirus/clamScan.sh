#!/bin/bash

read -p 'Enter the directory to scan: ' directory

directory=$(echo $directory | sed 's|^~|'"$HOME"'|')

if [[ ! -d "$directory" ]]; then
    echo -e "\033[31;1m[Error]\033[0m Directory does not exist: $directory"
    exit 1
fi

echo "Please select options for ClamAV scan (type numbers separated by space):"
echo "1. -h or --help"
echo "2. -r or --recursive"
echo "3. -i or --infected"
echo "4. --remove"
echo "5. --move=DIR"
echo "6. --copy=DIR"
echo "7. --exclude=PATTERN"
echo "8. --exclude-dir=PATTERN"
echo "9. --log=FILE"
echo "10. --max-filesize=SIZE"
echo "11. --max-scansize=SIZE"
echo "12. --max-recursion=NUMBER"
echo "13. --max-files=NUMBER"
echo "14. --include=PATTERN"
echo "15. --quiet"
echo "16. --no-summary"
echo "17. --stdout"
echo "18. --debug"
echo "19. --leave-temps"
echo "20. --config-file=FILE"
echo "21. --datadir=DIR"
echo "22. --reload"
echo "23. --bell"
echo "24. --scan-mail"
echo "25. --scan-archive"
echo "26. --scan-pdf"
echo "27. --scan-html"

read -p 'Enter your choices: ' choices

command="clamscan"

if [[ "$choices" == *"1"* ]]; then
    $command -h
    exit 0
fi

for choice in $choices; do
    case $choice in
        2) command="$command -r" ;;
        3) command="$command -i" ;;
        4) command="$command --remove" ;;
        5) 
            read -p 'Enter the directory to move infected files: ' move_dir
            move_dir=$(realpath "$move_dir")
            command="$command --move=$move_dir" ;;
        6)
            read -p 'Enter the directory to copy infected files: ' copy_dir
            copy_dir=$(realpath "$copy_dir")
            command="$command --copy=$copy_dir" ;;
        7)
            read -p 'Enter the pattern to exclude files: ' exclude_pattern
            command="$command --exclude=$exclude_pattern" ;;
        8)
            read -p 'Enter the directory pattern to exclude: ' exclude_dir
            command="$command --exclude-dir=$exclude_dir" ;;
        9)
            read -p 'Enter the log file path: ' log_file
            log_file=$(realpath "$log_file")
            command="$command --log=$log_file" ;;
        10)
            read -p 'Enter the maximum file size (e.g., 10M): ' max_filesize
            command="$command --max-filesize=$max_filesize" ;;
        11)
            read -p 'Enter the maximum scan size (e.g., 100M): ' max_scansize
            command="$command --max-scansize=$max_scansize" ;;
        12)
            read -p 'Enter the maximum recursion level: ' max_recursion
            command="$command --max-recursion=$max_recursion" ;;
        13)
            read -p 'Enter the maximum number of files to scan: ' max_files
            command="$command --max-files=$max_files" ;;
        14)
            read -p 'Enter the pattern to include files: ' include_pattern
            command="$command --include=$include_pattern" ;;
        15) command="$command --quiet" ;;
        16) command="$command --no-summary" ;;
        17) command="$command --stdout" ;;
        18) command="$command --debug" ;;
        19) command="$command --leave-temps" ;;
        20)
            read -p 'Enter the custom configuration file path: ' config_file
            config_file=$(realpath "$config_file")
            command="$command --config-file=$config_file" ;;
        21)
            read -p 'Enter the custom virus database directory: ' datadir
            datadir=$(realpath "$datadir")
            command="$command --datadir=$datadir" ;;
        22) command="$command --reload" ;;
        23) command="$command --bell" ;;
        24) command="$command --scan-mail" ;;
        25) command="$command --scan-archive" ;;
        26) command="$command --scan-pdf" ;;
        27) command="$command --scan-html" ;;
        *)
            echo "Invalid choice: $choice"
            ;;
    esac
done

echo -e "\nExecuting ClamAV scan on $directory with the following options:"
echo $command $directory
$command $directory