#!/bin/bash

declare -A TOOL_GROUPS=(
    ["Web_Security"]="Nikto Sucridata"
    ["Network_Security"]="OpenVAS Zeek Snort"
    ["VPN_Analysis"]="Snort Zeek"
)

run_nikto() {
    echo "🔍 Running Nikto Web Server Scan..."
    nikto -h http://localhost
}

run_sucridata() {
    echo "🔍 Running Sucridata Security Scan..."
    # Example command (modify based on installation)
    sucridata --scan http://localhost
}

run_openvas() {
    echo "🔍 Running OpenVAS Vulnerability Scan..."
    greenbone-nvt-sync && openvas-start
}

run_zeek() {
    echo "🔍 Running Zeek Network Traffic Analysis..."
    zeek -r /var/log/pcap/*.pcap
}

run_snort() {
    echo "🔍 Running Snort Intrusion Detection..."
    snort -c /etc/snort/snort.conf -A console
}

show_menu() {
    clear
    echo "============================================="
    echo "🔥 NETWORK SECURITY SCAN MENU 🔥"
    echo "============================================="
    echo "1️⃣ Web Security Scan (Nikto + Sucridata)"
    echo "2️⃣ Full Network Security Audit (OpenVAS + Zeek + Snort)"
    echo "3️⃣ VPN & Firewall Analysis (Snort + Zeek)"
    echo "4️⃣ Custom Selection"
    echo "5️⃣ Exit"
    echo "============================================="
    read -p "👉 Choose an option (1-5): " CHOICE

    case $CHOICE in
        1) RUN_TOOLS=${TOOL_GROUPS["Web_Security"]} ;;
        2) RUN_TOOLS=${TOOL_GROUPS["Network_Security"]} ;;
        3) RUN_TOOLS=${TOOL_GROUPS["VPN_Analysis"]} ;;
        4) custom_selection ;;
        5) exit 0 ;;
        *) echo "❌ Invalid choice!"; sleep 1; show_menu ;;
    esac

    run_selected_tools "$RUN_TOOLS"
}

custom_selection() {
    clear
    echo "🔹 Select tools manually (space-separated):"
    echo "Available tools: Nikto Sucridata OpenVAS Zeek Snort"
    read -p "👉 Enter your choice: " CUSTOM_TOOLS
    run_selected_tools "$CUSTOM_TOOLS"
}

run_selected_tools() {
    echo "============================================="
    echo "🚀 Starting Security Scan with: $1"
    echo "============================================="
    for tool in $1; do
        case $tool in
            "Nikto") run_nikto ;;
            "Sucridata") run_sucridata ;;
            "OpenVAS") run_openvas ;;
            "Zeek") run_zeek ;;
            "Snort") run_snort ;;
            *) echo "⚠️ Unknown tool: $tool" ;;
        esac
    done
    echo "✅ Scan Completed!"
}

show_menu
