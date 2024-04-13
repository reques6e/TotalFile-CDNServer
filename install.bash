#!/bin/bash
update_config() {
    read -p "$1: " value
    sed -i "s/\"$2\": .*/\"$2\": \"$value\",/" data/config.json
}

setup_ssl() {
    if [ ! -f "/etc/ssl/certs/mycert.pem" ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/mykey.pem -out /etc/ssl/certs/mycert.pem
    fi
}

update_config "Введите почту администратора" "mail"
update_config "Введите домен" "domain"
update_config "Введите порт" "port"

read -p "Использовать SSL? (да/нет): (В РАЗРАБОТКЕ, НЕ ИСПОЛЬЗУЙТЕ) " use_ssl
if [ "$use_ssl" == "да" ]; then
    sed -i "s/\"protocol\": .*/\"protocol\": \"https\",/" data/config.json
    setup_ssl
else
    sed -i "s/\"protocol\": .*/\"protocol\": \"http\",/" data/config.json
fi

chmod +x main.py
sudo apt install python3-pip
pip3 install -r requirements.txt

cat > /etc/systemd/system/manager_cdn_server.service <<EOF
[Unit]
Description=Flask App
After=network.target

[Service]
User=root
WorkingDirectory=$(pwd)
ExecStart=$(which python) main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable manager_cdn_server
systemctl start manager_cdn_server

echo "Установка завершена."
