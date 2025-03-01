#!/bin/bash

main_menu() {
    while true; do
        clear
        echo "======================================="
        echo "       🔥 Linux Firewall Manager 🔥     "
        echo "======================================="
        echo "1. Configure iptables"
        echo "2. Configure nftables"
        echo "3. Configure firewalld"
        echo "4. Configure UFW"
        echo "5. Remove a Firewall Layer"
        echo "6. Show Active Firewall Rules"
        echo "7. Exit"
        echo "======================================="
        read -p "Select an option (1-7): " choice

        case $choice in
            1) iptables_menu ;;
            2) nftables_menu ;;
            3) firewalld_menu ;;
            4) ufw_menu ;;
            5) remove_firewall ;;
            6) show_rules ;;
            7) exit 0 ;;
            *) echo "Invalid option! Try again." && sleep 1 ;;
        esac
    done
}

add_firewall_rule() {
    local firewall_type=$1

    echo "-------------------------------------"
    echo "Adding a rule to $firewall_type"
    echo "-------------------------------------"
    
    read -p "Allow or Block traffic? (allow/block): " action
    rule_action="ACCEPT"
    [ "$action" == "block" ] && rule_action="DROP"

    read -p "Enter IP Address (or press Enter for any): " ip
    [ -z "$ip" ] && ip="0.0.0.0/0"

    read -p "Enter Port Number (or press Enter for any): " port
    port_rule=""
    [ -n "$port" ] && port_rule="--dport $port"

    echo "Select Protocol:"
    echo "1. TCP"
    echo "2. UDP"
    echo "3. ICMP"
    echo "4. All"
    read -p "Choose (1-4): " proto_choice

    case $proto_choice in
        1) protocol="tcp" ;;
        2) protocol="udp" ;;
        3) protocol="icmp" ;;
        4) protocol="all" ;;
        *) echo "Invalid choice, defaulting to TCP." && protocol="tcp" ;;
    esac

    echo "Select Direction:"
    echo "1. Incoming"
    echo "2. Outgoing"
    read -p "Choose (1-2): " direction_choice

    case $direction_choice in
        1) direction="INPUT" ;;
        2) direction="OUTPUT" ;;
        *) echo "Invalid choice, defaulting to Incoming." && direction="INPUT" ;;
    esac

    echo "Adding rule: $action $protocol $port for IP $ip on $direction"

    case $firewall_type in
        "iptables")
            sudo iptables -A "$direction" -p "$protocol" -s "$ip" $port_rule -j "$rule_action"
            ;;
        "nftables")
            sudo nft add rule inet filter "$direction" ip saddr "$ip" "$protocol" dport "$port" "$rule_action"
            ;;
        "firewalld")
            sudo firewall-cmd --permanent --add-rich-rule="rule family='ipv4' source address='$ip' port port='$port' protocol='$protocol' accept"
            sudo firewall-cmd --reload
            ;;
        "ufw")
            rule_type="allow"
            [ "$action" == "block" ] && rule_type="deny"
            sudo ufw "$rule_type" from "$ip" to any port "$port" proto "$protocol"
            ;;
    esac
    echo "Rule added successfully!"
    sleep 2
}

iptables_menu() {
    while true; do
        clear
        echo "====== 🛡 IPTABLES CONFIGURATION ======"
        echo "1. Add Rule"
        echo "2. Delete Rule"
        echo "3. List Rules"
        echo "4. Back to Main Menu"
        echo "======================================="
        read -p "Select an option (1-4): " choice

        case $choice in
            1) add_firewall_rule "iptables" ;;
            2) sudo iptables -F && echo "All iptables rules cleared." && sleep 1 ;;
            3) sudo iptables -L -v -n && read -p "Press Enter to continue...";;
            4) return ;;
            *) echo "Invalid choice! Try again." && sleep 1 ;;
        esac
    done
}

nftables_menu() {
    while true; do
        clear
        echo "====== 🔥 NFTABLES CONFIGURATION 🔥 ======"
        echo "1. Add Rule"
        echo "2. Delete All Rules"
        echo "3. List Rules"
        echo "4. Back to Main Menu"
        echo "=========================================="
        read -p "Select an option (1-4): " choice

        case $choice in
            1) add_firewall_rule "nftables" ;;
            2) sudo nft flush ruleset && echo "All nftables rules cleared." && sleep 1 ;;
            3) sudo nft list ruleset && read -p "Press Enter to continue...";;
            4) return ;;
            *) echo "Invalid choice! Try again." && sleep 1 ;;
        esac
    done
}

firewalld_menu() {
    while true; do
        clear
        echo "====== 🔥 FIREWALLD CONFIGURATION 🔥 ======"
        echo "1. Add Rule"
        echo "2. Remove All Rules"
        echo "3. List Active Rules"
        echo "4. Back to Main Menu"
        echo "=========================================="
        read -p "Select an option (1-4): " choice

        case $choice in
            1) add_firewall_rule "firewalld" ;;
            2) sudo firewall-cmd --reload && echo "All firewalld rules cleared." && sleep 1 ;;
            3) sudo firewall-cmd --list-all && read -p "Press Enter to continue...";;
            4) return ;;
            *) echo "Invalid choice! Try again." && sleep 1 ;;
        esac
    done
}

ufw_menu() {
    while true; do
        clear
        echo "====== 🔥 UFW CONFIGURATION 🔥 ======"
        echo "1. Add Rule"
        echo "2. Reset UFW Rules"
        echo "3. List Rules"
        echo "4. Back to Main Menu"
        echo "====================================="
        read -p "Select an option (1-4): " choice

        case $choice in
            1) add_firewall_rule "ufw" ;;
            2) sudo ufw reset && echo "UFW rules reset." && sleep 1 ;;
            3) sudo ufw status numbered && read -p "Press Enter to continue...";;
            4) return ;;
            *) echo "Invalid choice! Try again." && sleep 1 ;;
        esac
    done
}

show_rules() {
    while true; do
        clear
        echo "====== 🔍 VIEW ACTIVE FIREWALL RULES 🔍 ======"
        echo "1. iptables"
        echo "2. nftables"
        echo "3. firewalld"
        echo "4. UFW"
        echo "5. Back to Main Menu"
        echo "============================================"
        read -p "Select an option (1-5): " choice

        case $choice in
            1) sudo iptables -L -v -n && read -p "Press Enter to continue..." ;;
            2) sudo nft list ruleset && read -p "Press Enter to continue..." ;;
            3) sudo firewall-cmd --list-all && read -p "Press Enter to continue..." ;;
            4) sudo ufw status numbered && read -p "Press Enter to continue..." ;;
            5) return ;;
            *) echo "Invalid choice! Try again." && sleep 1 ;;
        esac
    done
}

remove_firewall() {
    echo "Which firewall layer do you want to remove a rule from?"
    echo "1. iptables"
    echo "2. nftables"
    echo "3. firewalld"
    echo "4. UFW"
    echo "5. Cancel"
    read -p "Choose an option (1-5): " choice

    case $choice in
        1) 
            sudo iptables -L --line-numbers
            read -p "Enter rule number to delete (or press Enter to cancel): " rule
            [ -n "$rule" ] && sudo iptables -D INPUT "$rule"
            ;;
        2)
            sudo nft list ruleset
            read -p "Enter the rule number (or press Enter to cancel): " rule
            [ -n "$rule" ] && sudo nft delete rule inet filter INPUT "$rule"
            ;;
        3)
            sudo firewall-cmd --list-all
            read -p "Enter the rule to remove (or press Enter to cancel): " rule
            [ -n "$rule" ] && sudo firewall-cmd --permanent --remove-rich-rule="$rule" && sudo firewall-cmd --reload
            ;;
        4)
            sudo ufw status numbered
            read -p "Enter rule number to delete (or press Enter to cancel): " rule
            [ -n "$rule" ] && sudo ufw delete "$rule"
            ;;
        5) return ;;
        *) echo "Invalid option! Returning to main menu." && sleep 1 ;;
    esac
    echo "Rule removed successfully!"
    sleep 2
}

main_menu