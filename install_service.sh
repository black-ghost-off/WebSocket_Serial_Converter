if [ -z "$1" ]
  then
    echo "No argument supplied\ninstall_service.sh %PORT%"
    exit 1
fi

if ! hash python; then
    echo "python is not installed"
else
    ret=`python -c 'import sys; print("%i" % (sys.hexversion<0x030711f0))'`
    if [ $ret -eq 0 ]; then
        echo "greet"
        echo "pwd     : $($USER)"
        rm -f /etc/systemd/system/WebSocket_Serial_Converter.service

        python -m pip install -r $(pwd)/requirements.txt

cat >/etc/systemd/system/WebSocket_Serial_Converter.service <<EOL
[Unit]
Description=WebSocket Serial Converter
[Service]
ExecStart=$(which python) $(pwd)/main.py --port $1 
[Install]
WantedBy=multi-user.target
EOL

        GREEN='\033[0;32m'

        echo "\n\n${GREEN}Install success\n\n"

    else 
        echo "python version above 3.7 required"
        exit 1    
    fi
fi

