import unittest

from distributed_schedule.server import main


class TestShow(unittest.TestCase):

    def test_server(self):
        print("test show")
        main()


if __name__ == '__main__':
    unittest.main()