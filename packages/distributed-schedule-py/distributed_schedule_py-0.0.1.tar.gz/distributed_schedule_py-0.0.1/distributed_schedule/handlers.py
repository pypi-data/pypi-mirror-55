import json
from uuid import uuid4

from distributed_schedule.times_handlers import *


NOTFOUND = "404"
ERRORHANDLER = "500"


"""
协议格式如下：
28\r\ntest\nwrite1\tdata\tstatus\t200\t

28：为消息体长度
\r\n：为头部解析位置
test: 为消息的类型，类似与web中的uri，资源定位符
write1 : data  为键值内容
status : 200 为消息的响应体
|消息长度|\r\n|消息类型|\nkey1\tvalue1\tkey2\tvalue2\t

长度为28     类型为 test  输入值为 {"write1": "data", "key2": "value2"}
"""


class Application(object):
    HEAD_DELIMITER = "\r\n"
    BODY_DELIMITER = "\n"
    PARAMS_DELIMITER = "\t"

    def __init__(self):
        self.handlers = {}

    def register_handler(self, handler):
        if not issubclass(handler, BaseHandler):
            raise Exception("handler {0} must be subclass of BaseHandler".format(handler))
        if hasattr(handler, "type"):
            self.handlers[handler.type] = handler

    def __call__(self, type, content, **kwargs):
        if type in self.handlers:
            handler = self.handlers[type]
        else:
            handler = self.handlers[NOTFOUND]

        try:
            response = handler(request_data=content).serilizer(**kwargs)
        except Exception as e:
            logger.exception("error   :   {0}".format(e))
            response = ErrorHandler().serilizer()

        return response


def parse_body_params(body_params: str, params_delimiter: str) -> dict:
    """

    :param body_params:   传入的body内容
    :param params_delimiter: 解析的分割符
    :return:
    """
    res = {}
    while True:
        loc = body_params.find(params_delimiter)
        if loc != -1:
            key = body_params[:loc]
            body_params = body_params[(loc + len(params_delimiter)):]
            loc_v = body_params.find(params_delimiter)
            if loc_v != -1:
                value = body_params[:loc_v]
                body_params = body_params[(loc_v + len(params_delimiter)):]

            res[key] = value
        else:
            return res


class BaseHandler(object):
    type = "base"
    head_delimiter = Application.HEAD_DELIMITER
    body_delimiter = Application.BODY_DELIMITER
    params_delimiter = Application.PARAMS_DELIMITER
    body = "error"

    def __init__(self, request_data=None):
        self.request_data = request_data
        self.data = {}
        self.response_params = {}
        self.parse_params()

    def serilizer(self, **kwargs):
        raise NotImplementedError

    def parse_params(self):
        if not self.request_data:
            return
        self.data = parse_body_params(self.request_data, self.params_delimiter)

    def write_params(self, key, value):
        self.response_params[key] = value

    def serilizer_params(self, data):
        content = ''
        for key in data:
            content += "{0}{1}{2}{3}".format(key, self.params_delimiter, data[key], self.params_delimiter)
        return content

    def get_response(self, response, is_write=True):
        body = ''
        if is_write:
            self.response_params.update(response)
            body += self.serilizer_params(self.response_params)
        else:
            self.data.update(response)
            body += self.serilizer_params(self.data)
        length = len(self.body_delimiter) + len(self.type) + len(body)
        return "{0}{1}{2}{3}{4}".format(length, self.head_delimiter, self.type, self.body_delimiter, body)

    def finish(self, data):
        if not isinstance(data, dict):
            raise Exception(" data  :  {0}   must be dict  ".format(data))
        content = self.get_response(data)
        return content

    def deserialize(self, data):
        return self.get_response(data, is_write=False)


class NotFoundHandler(BaseHandler):
    type = NOTFOUND

    def serilizer(self, **kwargs):
        return self.finish({"status": "404"})


class ErrorHandler(BaseHandler):
    type = ERRORHANDLER

    def serilizer(self, **kwargs):
        return self.finish({"status": "500"})


class Test(BaseHandler):
    type = "test"

    def serilizer(self, **kwargs):
        return self.finish({"status": "200"})


# 数据存储层应该考虑在store层面设计
"""
Clients like  {
    "client_1": Iostream,
    "client_2": Iostream,
}
"""
Clients = {}
"""
Tasks like {
    "task_1": ["client_1", "client_2"],
    "task_2": ["client_1",]
}
"""
Tasks = {}
"""
Record like {
    "uuid1": {
        "client_id": {
            "client_event_id": "client_event_id",
            "task_id": "task_id",
            "status": "doing"
        }
    }
}
"""
Record = {}


def remove_callback(*args, **kwargs):
    client_id = kwargs.get("client_id")
    if client_id in Clients:
        Clients.pop(client_id)
    for key in Tasks:
        if client_id in Tasks[key]:
            Tasks[key].remove(client_id)
    # clear Tasks
    keys = [key for key in Tasks]
    for key in keys:
        if not Tasks[key]:
            Tasks.pop(key)


class RegisterHandler(BaseHandler):
    type = "register_client"

    def serilizer(self, **kwargs):
        """注册新进来连接 如果连接断开则删除该连接信息"""
        client_id = self.data["client_id"]
        protocl = kwargs.get("protocl")
        Clients[client_id] = protocl
        protocl.register_clear_func(remove_callback, **{"client_id": client_id})

        return self.finish({"status": "200"})


class BroadHandler(BaseHandler):
    """
    广播当前任务可以执行
    """
    type = "broad"

    def serilizer(self, **kwargs):
        task_id = self.data.get("task_id")
        if not task_id or (not task_id in Tasks):
            return self.finish({"status": "400"})

        mode = self.data.get("mode", "all")
        if mode == "all":
            is_once = False
        else:
            is_once = True
        shard = int(self.data.get("shard", 0))

        workers = len(Tasks[task_id])

        shard_list = []
        if shard:
            shard_list = div_shard(shard, workers)

        # 开始分布式广播接收数据
        event_id = str(uuid4())

        Record[event_id] = {}

        j = 0
        for client_id in Tasks[task_id]:
            # 通知客户端可以执行任务
            if client_id in Clients:
                res = {"task_id": task_id, "event_id": event_id, "status": "doing"}
                Record[event_id].update({client_id: res})
                client_event_id = str(uuid4())
                res.update({"client_event_id": client_event_id})
                if shard_list:
                    for item in shard_list[j]:
                        res.update({"item": item})
                        result = ClientNotifyHandler().deserialize(res)
                        Clients[client_id].write_result(result)
                    j += 1
                    continue
                else:
                    result = ClientNotifyHandler().deserialize(res)
                    Clients[client_id].write_result(result)
                    if is_once:
                        break
        return self.finish({"status": "200"})


class ClientNotifyHandler(BaseHandler):
    """
    通知客户端执行任务
    """
    type = "broadclient"


class RegisterTask(BaseHandler):
    """
    客户端向服务端注册任务
    """
    type = "registertask"

    def serilizer(self, **kwargs):
        task_id = self.data["task_id"]
        client_id = self.data["client_id"]
        if task_id not in Tasks:
            Tasks[task_id] = [client_id]
        else:
            if client_id not in Tasks[task_id]:
                Tasks[task_id].append(client_id)
                # node = TimeNode()

                # TimeHandler.insert(TimeNode().call_later(10))
        logger.info("cur tasks :  {0}".format(Tasks))
        return self.finish({"status": "200"})


class TaskMsgs(BaseHandler):
    type = "taskmsgs"

    def serilizer(self, **kwargs):
        result = {
            "tasks": json.dumps(Tasks),
            "record": json.dumps(Record)
        }
        return self.finish(result)


class NotifyTaskStatue(BaseHandler):
    """
    汇报任务执行的结果
    """
    type = "notifytaskstatus"

    def serilizer(self, **kwargs):
        client_id = self.data.get("client_id")
        task_id = self.data.get("task_id")
        status = self.data.get("status")
        event_id = self.data.get("event_id")
        client_event_id = self.data.get("client_event_id")
        print("self data   :   {0}".format(self.data))
        print("client_id : {0} task_id : {1}  status : {2}  event_id : {3} client_event_id : {4}".format(client_id, task_id, status, event_id, client_event_id))
        if event_id not in Record:
            return self.finish({"status": "400"})
        client_event = Record[event_id]
        if client_id not in client_event:
            return self.finish({"status": "400"})
        client = client_event[client_id]
        if client["task_id"] == task_id and client["client_event_id"] == client_event_id:
            client["status"] = status
            return self.finish({"status": "200"})
        return self.finish({"status": "400"})


handles = [
    Test, NotFoundHandler, ErrorHandler, RegisterHandler,
    RegisterTask, BroadHandler, TaskMsgs, NotifyTaskStatue
]

application = Application()

for handle in handles:
    application.register_handler(handle)





