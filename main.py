import sys
import glob
import serial
import tornado.ioloop
import tornado.web
import tornado.websocket
import argparse
import json
from datetime import datetime, timezone, timedelta


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    conn = None

    datafilter = "None"

    def open(self):
        print("open success")
        if(self.request.path != "/" and (self.conn == None or not(self.conn.is_open))):
            arguments = self.request.path.split("/", 4)
            print(arguments)
            if(arguments[4][0:3] == "dev"):
                arguments[4] = "/" + arguments[4]
            self.conn = serial.Serial(arguments[4], baudrate = int(arguments[3]), parity = arguments[2])
            self.datafilter = arguments[1]
        # timer that sends data to the front end once per second
        self.timer = tornado.ioloop.PeriodicCallback(self.send_data, 1)
        self.timer.start()
        if(self.request.path == "/"):
            self.write_message(str(serial_ports()))
            self.close()

        return
        
    def on_close(self):
        print("close")
        self.timer.stop()
        if(self.conn != None):
            self.conn.close()
        self.conn = None

    def send_data(self):
        if(self.conn != None and self.conn.is_open and self.conn.in_waiting):
            readed_line = self.conn.readline()
            if(self.datafilter == "None"):
                self.write_message(readed_line.decode("utf-8"))
            elif(self.datafilter == "grafana"):
                try:
                    json_parsed = json.loads(readed_line.decode("utf-8").replace("'", '"'))
                    now = datetime.now(timezone.utc)
                    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc) # use POSIX epoch
                    posix_timestamp_millis = (now - epoch) // timedelta(milliseconds=1)
                    json_parsed["timestamp"] = posix_timestamp_millis
                    self.write_message(str(json_parsed).replace("'", '"'))
                except AssertionError as error:
                    pass
            else:
                pass

    def on_message(self, message):
        print(message)
        if(self.request.path != "/" and (self.conn == None or not(self.conn.is_open))):
            arguments = self.request.path.split("/", 3)
            if(arguments[3][0:3] == "dev"):
                arguments[3] = "/" + arguments[3]
            self.conn.write(message)


application = tornado.web.Application([
    (r'/.*', WebSocketHandler),
])

if __name__ == '__main__':
    parser = argparse.ArgumentParser("WS Server")
    parser.add_argument("--port", help="An port where will be start WS server.", type=int)
    args = parser.parse_args()
    print("SERIAL <=> WS SERVER LISTENED ON " + str(args.port))
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()