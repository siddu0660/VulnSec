#!/bin/bash

get_input() {
    local prompt=$1
    local default=$2
    read -p "$prompt [$default]: " input
    echo "${input:-$default}"
}

clear
echo "==========================================="
echo "     🔥 OpenVPN Configuration Generator 🔥"
echo "==========================================="
echo "This script will generate a server.conf file."
echo

PROTO=$(get_input "Enter protocol (udp/tcp)" "udp")
PORT=$(get_input "Enter OpenVPN port" "1194")
DNS1=$(get_input "Enter primary DNS server" "1.1.1.1")
DNS2=$(get_input "Enter secondary DNS server" "8.8.8.8")
COMPRESS=$(get_input "Enable compression? (yes/no)" "no")
CLIENT_TO_CLIENT=$(get_input "Enable client-to-client communication? (yes/no)" "yes")
LOGGING=$(get_input "Enable logging? (yes/no)" "yes")

if [[ "$COMPRESS" == "yes" ]]; then
    COMPRESS_OPTION="compress lz4"
else
    COMPRESS_OPTION=""
fi

if [[ "$CLIENT_TO_CLIENT" == "yes" ]]; then
    CLIENT_TO_CLIENT_OPTION="client-to-client"
else
    CLIENT_TO_CLIENT_OPTION="# client-to-client (disabled)"
fi

if [[ "$LOGGING" == "yes" ]]; then
    LOG_OPTIONS="log /var/log/openvpn.log
status /var/log/openvpn-status.log
verb 3"
else
    LOG_OPTIONS="verb 0"
fi

CONFIG_FILE="server.conf"
cat > $CONFIG_FILE <<EOF
port $PORT
proto $PROTO
dev tun

ca /etc/openvpn/ca.crt
cert /etc/openvpn/server.crt
key /etc/openvpn/server.key
dh /etc/openvpn/dh.pem

server 10.8.0.0 255.255.255.0
ifconfig-pool-persist /var/log/openvpn/ipp.txt

push "dhcp-option DNS $DNS1"
push "dhcp-option DNS $DNS2"

keepalive 10 120
$COMPRESS_OPTION
$CLIENT_TO_CLIENT_OPTION

persist-key
persist-tun

$LOG_OPTIONS

tls-auth /etc/openvpn/ta.key 0
cipher AES-256-CBC
auth SHA256

user nobody
group nogroup

explicit-exit-notify 1
EOF

echo
echo "✅ OpenVPN configuration file 'server.conf' has been generated successfully!"
