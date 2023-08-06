import threading
import random


from distributed_schedule.server import *

logger = logging.getLogger()

HEAD_DELIMITER = Application.HEAD_DELIMITER
BODY_DELIMITER = Application.BODY_DELIMITER


class Client(object):

    def __init__(self, name, ip=None, port=None, cond=None):
        self.ip = ip or "127.0.0.1"
        self.port = port or 4546
        self.client_name = name
        self.cond_result = None
        self.sock = None
        self.running = False
        self.recv_buffer = ""
        self.write_buffer = b""
        self.selector = selectors.DefaultSelector()
        self.handlers = {}              # handle
        self.init()

    def set_async_result(self, async_result):
        self.cond_result = async_result

    def register(self, msg_type, callback):
        self.handlers[msg_type] = callback

    def init(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.ip, self.port))
            self.sock.setblocking(False)
            self.selector.register(self.sock, selectors.EVENT_READ, self.read)
            self.running = True
        except Exception as e:
            logger.exception(e)
            time.sleep(5)
            self.init()
            # self.stop()
            # os._exit(10)

    def handle_execute(self, msg_type, msg_content):
        params = parse_body_params(msg_content, application.PARAMS_DELIMITER)

        # 如果是客户端则直接返回数据
        if self.cond_result:
            self.cond_result.set((msg_type, msg_content))
            self.cond_result = None
            return

        if msg_type not in self.handlers:
            logger.info("not found handle for {0}".format(msg_type))
            return
        try:
            if isinstance(params, dict):
                params.update({"client": self})
            self.handlers[msg_type](params)
        except Exception as e:
            logger.exception("handles  execute error {0}".format(e))
            return

    def read(self, conn, mask):
        data = conn.recv(1000)
        if data:
            logger.info("client recv data :  {0}".format(repr(data)))
            self.recv_buffer += data.decode("utf-8")
            while True:
                loc = self.recv_buffer.find(HEAD_DELIMITER)
                logger.info("loc index : {0}   recv buffer  {1}".format(loc, self.recv_buffer))
                if loc != -1:
                    length = int(self.recv_buffer[:loc])
                    cur_recv_buffer = self.recv_buffer[(loc+len(HEAD_DELIMITER)):]
                    if length <= len(cur_recv_buffer):
                        self.recv_buffer = cur_recv_buffer
                        data = self.recv_buffer[:length]
                        body_loc = data.find(BODY_DELIMITER)
                        if body_loc != -1:
                            msg_type = data[:body_loc]
                            msg_content = data[(body_loc+len(BODY_DELIMITER)):]
                            logger.info("parse from server  {0}    {1}  ".format(msg_type, msg_content))
                            self.handle_execute(msg_type, msg_content)
                        self.recv_buffer = self.recv_buffer[length:]
                    else:
                        break
                else:
                    break
        else:
            self.close()

    def close(self):
        logger.info("client close")
        self.selector.unregister(self.sock)
        self.sock.close()

        if self.running:
            time.sleep(5)
            self.init()

    def handle_send(self):
        while self.write_buffer:
            try:
                size = self.sock.send(self.write_buffer)
            except socket.error as e:
                if e.errno in (socket.EWOULDBLOCK, socket.EAGAIN):
                    logger.error("send error : {0}".format(e))
                    break
                else:
                    logger.error("handle write close error : {0}".format(e))
                    return
            else:
                self.write_buffer = self.write_buffer[size:]

    def write_result(self, data):
        if self.sock:
            logger.info("send   {0}".format(repr(data)))
            if isinstance(data, str):
                data = data.encode("utf-8")
            while data:
                try:
                    size = self.sock.send(data)
                except socket.error as e:
                    if e.errno in (socket.EWOULDBLOCK, socket.EAGAIN):
                        logger.error("send error : {0}".format(e))
                        break
                    else:
                        logger.error("handle write close error : {0}".format(e))
                        return
                else:
                    logger.info("send  size  {0}".format(size))
                    data = data[size:]

    def stop(self):
        if self.running:
            self.running = False

    def start(self, bolck=True):
        t = threading.Thread(target=self.worker)
        t.setDaemon(bolck)
        t.start()

    def worker(self):
        while self.running:
            events = self.selector.select(timeout=1)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
            self.handle_send()


def broadclient_callback(params):
    from distributed_schedule.tasks import queue
    if isinstance(params, dict):
        queue.put(params)


def taskmsgs_callback(params):
    task = params["tasks"]
    record = params["record"]
    tasks_val = json.loads(task)
    for k in tasks_val:
        print(" \ntask_id : {0}  clients : {1}".format(k, tasks_val[k]))

    record_val = json.loads(record)
    for k in record_val:
        print("\n uuid : {0}  detail :  {1}".format(k, record_val[k]))


def callback_suc(params):
    logger.info("callback : {0}".format(params))
    if "status" in params and params["status"] == "200":
        print("response ok")


class CommandExecute(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class TaskCommand(CommandExecute):

    def do_start(self, args, kwargs):
        if len(args) == 0:
            return
        post_params = {}

        task_id = args[0]
        if not task_id:
            return
        post_params["task_id"] = task_id
        params = {}
        for val in args[1:]:
            if "=" in val:
                vals = val.split("=")
                if len(vals) != 2:
                    continue
                params[vals[0]] = vals[1]
        if "shard" in params:
            if params["shard"].isdigit():
                post_params["shard"] = params["shard"]
        if "mode" in params:
            if params["mode"] in ("all", "once"):
                post_params["mode"] = params["mode"]
        else:
            post_params["mode"] = "all"
        post_params.update(kwargs)
        return BroadHandler().deserialize(post_params)

    def __call__(self, args, kwargs):
        if not args:
            return
        subcommand = args[0]
        if subcommand == "list":
            return TaskMsgs().deserialize(kwargs)
        if subcommand == "start":
            return self.do_start(args[1:], kwargs)


class Command(object):

    def __init__(self, client):
        self.client = client
        self.post_data = {"client_id": self.client.client_name}
        self.commands = {}

    def register_command(self, name, command: CommandExecute):
        self.commands[name] = command

    def write(self, data):
        self.client.write_result(data)

    def parse_commands(self):
        data = input(">").strip()
        while self.client.running:
            args = data.split(" ")
            if not args:
                continue
            while True:
                if "" in args:
                    args.remove("")
                else:
                    break
            command = args[0]
            if command in self.commands:
                result = self.commands[command](args[1:], {"client_id": self.client.client_name})
                self.write(result)
            data = input(">").strip()


class TaskClient(object):

    class AsyncResult(object):

        def __init__(self):
            self._condition = threading.Condition()
            self.value = None

        def get(self, block=True, timeout=None):
            with self._condition:
                if block:
                    self._condition.wait(timeout=timeout)

        def set(self, value):
            with self._condition:
                self.value = value
                self._condition.notifyAll()

    def __init__(self, client):
        self.client = client
        self.post_params = {}
        self.cond = threading.Condition()
        self.client.cond = self.cond

    def get_all(self):
        res = TaskMsgs().deserialize({"client_id": self.client.client_name})
        self.client.write_result(res)
        result = self.AsyncResult()
        self.client.set_async_result(result)
        result.get()
        return result.value

    def submit(self, task_id=None, mode="all", shard=None, timeout=None):
        if not task_id:
            return

        self.post_params = {}
        self.post_params["task_id"] = task_id
        if shard is not None:
            self.post_params["shard"] = shard

        if mode in ("all", "once"):
            self.post_params["mode"] = mode

        res = BroadHandler().deserialize(self.post_params)
        self.client.write_result(res)
        result = self.AsyncResult()
        self.client.set_async_result(result)
        result.get()
        return result.value


@click.command()
@click.option('--name', default=str(random.randint(1, 1000)), help="must unique client id")
@click.option('--role', default="client", help="client or worker")
@click.option('--loglevel', default=logging.ERROR, help="default logger level")
@click.option('--ip', default="127.0.0.1", help="default ip")
@click.option('--port', default=4546, help="default port")
def main(name, role, loglevel, ip, port):
    run(name, role, loglevel, ip, port)


def run(name, role, loglevel, ip, port):
    c = Client(name, ip, port)
    c.register("broadclient", broadclient_callback)
    c.register("register_client", callback_suc)
    c.register("test", callback_suc)
    c.register("broad", callback_suc)
    c.register("taskmsgs", taskmsgs_callback)
    c.start(False)
    set_logging_level(loglevel)

    com = Command(c)
    com.register_command("task", TaskCommand("task"))

    post_data = {"client_id": name}

    c.write_result(Test().deserialize({"key": "value", "key1": "value"}))
    c.write_result(RegisterHandler().deserialize(post_data))
    if role == "client":
        c.write_result(BroadHandler().deserialize({"task_id": "task_1", "shard": 10}))
        com.parse_commands()

    else:
        from distributed_schedule.tasks import tasks as default_tasks
        tasks = default_tasks
        logger.info(tasks)

        for task in tasks:
            post_data.update({"task_id": task.task_name})
            c.write_result(RegisterTask().deserialize(post_data))


if __name__ == '__main__':
    main()


