import selectors
import socket

import click

from distributed_schedule.config import *
from distributed_schedule.handlers import *
# from times_handlers import time_handler


logger = logging.getLogger(__name__)


class CooProtocl(object):

    def __init__(self, stream, request_callback):
        self.stream = stream
        self.request_callback = request_callback
        self._read_delimiter = request_callback.HEAD_DELIMITER
        self._body_delimiter = request_callback.BODY_DELIMITER
        self.stream.read_util(self._read_delimiter, self.parse_length)

    def register_clear_func(self, func, *args, **kwargs):
        self.stream.register_close_callback(func, *args, **kwargs)

    def parse_length(self, data):
        body_length = data[:-len(self._read_delimiter)]
        if body_length.isdigit():
            self.stream.read_nums_util(int(body_length), self.parse_body)

    def write_result(self, data):
        if data:
            self.stream.write(data)
            self.stream.update_io_state(selectors.EVENT_WRITE)

    def parse_body(self, data):
        loc = data.find(self._body_delimiter)
        msg_type = data[:loc]
        msg_content = data[(loc+len(self._body_delimiter)):]
        logger.info("{0}   {1}".format(msg_type, msg_content))
        try:
            response = self.request_callback(msg_type, msg_content, **{"protocl": self})
            logger.info("callback response   :  {0}".format(response))
            self.write_result(response)
        except Exception as e:
            logger.exception("error {0}".format(e))
        self.stream.read_util(self._read_delimiter, self.parse_length)


class Stream(object):

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.addr = addr
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
        self.conn.setblocking(False)
        self.recv_buffer = ""
        self.write_buffer = b""
        self._read_delimiter = None
        self._read_callback = None
        self._read_length = None
        self._read_nums_callback = None
        self.server = server
        self.state = selectors.EVENT_READ
        self.close_callback = {}
        self.server.selector.register(self.conn, self.state, self.handle_event)

    def _consume(self, loc):
        data = self.recv_buffer[:loc]
        self.recv_buffer = self.recv_buffer[loc:]
        return data

    def update_io_state(self, mask):
        self.state = mask
        self.server.modify(self.conn, mask, self.handle_event)

    def read_util(self, delimiter, callback):
        loc = self.recv_buffer.find(delimiter)
        if loc != -1:
            callback(self._consume(loc+len(delimiter)))
            return
        # 如果没有解析对的格式则表示还需要等待数据输入
        self._read_delimiter = delimiter
        self._read_callback = callback
        self.update_io_state(selectors.EVENT_READ)

    def read_nums_util(self, read_length, callback):
        if len(self.recv_buffer) >= read_length:
            callback(self._consume(read_length))
            return
        self._read_length = read_length
        self._read_nums_callback = callback
        self.update_io_state(selectors.EVENT_READ)

    def register_close_callback(self, func, *args, **kwargs):
        self.close_callback[func] = {"args": args, "kwargs": kwargs}

    def close_callback_execute(self):
        for func in self.close_callback:
            try:
                # logger.info("close callback execute   :  {0}   {1}   ".format(func, self.close_callback[func]))
                func(*self.close_callback[func]["args"], **self.close_callback[func]["kwargs"])
            except Exception as e:
                logger.exception(" close callback error  :   {0}".format(e))

    def close(self):
        if self.state != -1:
            self.state = -1
            self.close_callback_execute()
            self.server.modify(self.conn, self.state)

    def handle_read(self):
        try:
            data = self.conn.recv(1)
        except socket.error as e:
            if e.errno in (socket.EAGAIN, socket.EWOULDBLOCK):
                logger.exception("connectreset error : {0}".format(e))
                return
            else:
                logger.exception("handler read error : {0}".format(e))
                self.close()
                return

        if not data:
            self.close()
            return

        self.recv_buffer += data.decode("utf-8")

        if self._read_delimiter:
            loc = self.recv_buffer.find(self._read_delimiter)
            if loc != -1:
                callback = self._read_callback
                data = self._consume(loc+len(self._read_delimiter))
                self._read_delimiter = None
                self._read_callback = None
                callback(data)
        elif self._read_length:
            if len(self.recv_buffer) >= self._read_length:
                callback = self._read_nums_callback
                data = self._consume(self._read_length)
                self._read_length = None
                self._read_nums_callback = None
                callback(data)

    def write(self, data):
        self.write_buffer += data.encode("utf-8")

    def handle_write(self):
        while self.write_buffer:
            try:
                size = self.conn.send(self.write_buffer)
            except socket.error as e:
                if e.errno in (socket.EWOULDBLOCK, socket.EAGAIN):
                    logger.error("send error : {0}".format(e))
                    break
                else:
                    self.close()
                    logger.error("handle write close error : {0}".format(e))
                    return
            else:
                self.write_buffer = self.write_buffer[size:]
            logger.info("left data :    {0}".format(self.write_buffer))

    def handle_event(self, conn, mask):
        if mask == selectors.EVENT_READ:
            self.handle_read()
        elif mask == selectors.EVENT_WRITE:
            self.handle_write()

        if self.state == -1:
            return

        state = 0
        if self._read_length or self._read_delimiter:
            state = selectors.EVENT_READ | state
        if self.write_buffer:
            state = selectors.EVENT_WRITE | state
        if state != self.state:
            logger.info("{0}   {1}".format(state, self.state))
            self.state = state
            self.update_io_state(state)


class Server(object):

    def __init__(self, ip=None, port=None, application=None):
        self.ip = ip or "127.0.0.1"
        self.port = port or 4546
        self.sock = None
        self.running = False
        self.request_callback = application
        self.selector = selectors.DefaultSelector()
        self.init()

    def init(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, self.accept)

    def modify(self, conn, mask, callback=None):
        logger.info("modify  {0}   {1}   {2}".format(conn, mask, callback))
        if mask != -1:
            self.selector.modify(conn, mask, callback)
        else:
            self.selector.unregister(conn)

    def accept(self, conn, mask):
        conn, addr = conn.accept()
        logger.info("recv conn    {0}".format(conn))
        s = Stream(conn, addr, self)
        CooProtocl(s, self.request_callback)

    def start(self):
        if not self.running:
            self.running = True
        while self.running:
            events = self.selector.select(timeout=1)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
            # 暂时不使用定时任务
            # time_handler()

    def stop(self):
        if self.running:
            self.running = False


@click.command()
@click.option('--ip', default="127.0.0.1", help="default ip")
@click.option('--port', default=4546, help="default port")
@click.option('--loglevel', default=logging.ERROR, help="default logger level")
def main(ip, port, loglevel):
    server_run(ip, port, loglevel)


def server_run(ip, port, loglevel):
    print("server start listen at {0}:{1}".format(ip, port))
    set_logging_level(loglevel)
    s = Server(application=application, ip=ip, port=port)
    s.start()


if __name__ == '__main__':
    main()