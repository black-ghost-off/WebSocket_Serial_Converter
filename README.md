# WebSocket / Serial Converter
A small utility for transferring data from/to a Serial port (for example, Arduino) using the WebSocket protocol.
## Launch: 
#### 1 way
``` bash
$ python -m pip install -r requirements.txt
$ python main.py --port %PORT%
```
#### 2 way
Linux only
``` bash
$ sudo sh install_service.sh %PORT%

$ sudo systemctl daemon-reload
$ sudo systemctl enable WebSocket_Serial_Converter.service
$ sudo systemctl start WebSocket_Serial_Converter.service

$ sudo systemctl status WebSocket_Serial_Converter.service
```
#### 3 way
Build docker image
``` bash
$ sudo docker build .
$ sudo docker run -d -v /dev:/dev -p %PORT%:8800 --privileged %docker ID%
```

#### 4 way
Build docker image
``` bash
$ sudo docker-compose up -d
```

