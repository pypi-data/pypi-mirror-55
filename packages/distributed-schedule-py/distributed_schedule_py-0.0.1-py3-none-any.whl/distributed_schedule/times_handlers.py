import time
from distributed_schedule.config import *


logger = logging.getLogger(__name__)


class BasicNodeHandler(object):

    def __init__(self, time=None, next=None):
        self.time = time
        self.next = next

    def execute(self):
        raise NotImplementedError

    def __str__(self):
        return " time : {0} next : {1}".format(self.time, self.next)


class TimeNode(BasicNodeHandler):

    def __init__(self, time=None, next=None, callback=None, **kwargs):
        super().__init__(time, next)
        self.callback = callback
        self.kwargs = kwargs

    def call_later(self, seconds=0):
        self.time = time.time() + seconds

    def execute(self):
        logger.info("excute {0}".format(self.time))
        if not self.callback:
            return
        try:
            self.callback(**self.kwargs)
        except Exception as e:
            logger.exception("execute error {0}".format(e))


class TimeHandler(object):

    def __init__(self, head=None):
        self.head = head

    def show(self):
        node = self.head
        while node:
            logger.info("first : {0} ".format(node.time))
            node = node.next

    def insert(self, node):
        if not self.head:
            self.head = node
            return

        if self.head.time >= node.time:
            node.next = self.head
            self.head = node
            return

        cur_node = self.head
        while True:
            next = cur_node.next
            if not next:
                cur_node.next = node
                return

            if next.time < node.time:
                cur_node = next
            else:
                cur_node.next = node
                node.next = next
                return

    def __call__(self, *args, **kwargs):
        now = time.time()

        if not self.head:
            return

        node = self.head
        if not node:
            return
        while now >= node.time:
            try:
                node.execute()
            except Exception as e:
                logger.exception("node execute error  node  : {0}  error :  {1}".format(node, e))
            if not node.next:
                node = None
                break
            else:
                node = node.next

        self.head = node


t_node = TimeNode()
t_node.call_later(20)
t_node2 = TimeNode()
t_node2.call_later(15)
t_node3 = TimeNode()
t_node3.call_later(30)
time_handler = TimeHandler()
time_handler.insert(t_node2)
time_handler.insert(t_node3)
time_handler.insert(t_node)


if __name__ == '__main__':
    t_node = TimeNode()
    t_node.call_later(10)

    t = TimeHandler(t_node)
    t.show()

    t_node = TimeNode()
    t_node.call_later(20)
    t.insert(t_node)
    t.show()

    t_node = TimeNode()
    t_node.call_later(20)
    t.insert(t_node)
    t.show()

    t_node = TimeNode()
    t_node.call_later(1)
    t.insert(t_node)
    t.show()

    t_node = TimeNode()
    t_node.call_later(30)
    t.insert(t_node)
    t.show()




