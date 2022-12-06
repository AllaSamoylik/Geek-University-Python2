import unittest
from server import *


class TestServer(unittest.TestCase):
    def test_check_ip_localhost(self):
        self.assertEqual(check_ip('localhost'), 'localhost')

    def test_check_ip_incorrect(self):
        with self.assertRaises(ValueError) as e:
            check_ip('127.1000.0.1')
        the_exception = str(e.exception)
        self.assertEqual(the_exception, 'некорректный IP-адрес сервера')

    def test_check_port_correct(self):
        self.assertEqual(check_port(12000), 12000)

    def test_check_port_big(self):
        with self.assertRaises(ValueError) as e:
            check_port(65999)
        the_exception = str(e.exception)
        self.assertEqual(the_exception, 'некорректный tcp-порт')

    def test_msg_processing_correct(self):
        msg = {
            'action': 'presence',
            'time': '06-12-2022 12:00',
            'user': {
                'account_name': 'alla',
                'status': 'online'
            }
        }
        self.assertEqual(msg_processing(msg), {'response': 200})

    def test_msg_processing_missing_field(self):
        msg = {
            'action': 'presence',
            'user': {
                'account_name': 'alla',
                'status': 'online'
            }
        }
        self.assertEqual(msg_processing(msg), {'response': 400, 'error': 'bad request'})

    def test_msg_conversion_dict(self):
        self.assertEqual(msg_conversion({'user': {'account_name': 'alla', 'status': 'online'}}),
                         b'{"user": {"account_name": "alla", "status": "online"}}')

    def test_msg_conversion_bytes(self):
        self.assertEqual(msg_conversion(b'{"user": {"account_name": "alla", "status": "online"}}'),
                         {'user': {'account_name': 'alla', 'status': 'online'}})

    def test_set_addr_port_all(self):
        test_argv = ['server.py', '-a', 'localhost', '-p', '8888']
        test_argv_change = ['server.py', '-p', '8888', '-a', 'localhost']
        self.assertEqual(set_addr_port(test_argv), ('localhost', 8888))
        self.assertEqual(set_addr_port(test_argv_change), ('localhost', 8888))

    def test_set_addr_port_incorrect_param(self):
        with self.assertRaises(SystemExit):
            test_argv = ['server.py', '-a', 'localhost', '-p']
            set_addr_port(test_argv)
        with self.assertRaises(SystemExit):
            test_argv = ['server.py', '-p', 'test', '-a', 'localhost']
            set_addr_port(test_argv)
        with self.assertRaises(SystemExit):
            test_argv = ['server.py', '-p', '333333', '-a', 'localhost']
            set_addr_port(test_argv)


if __name__ == '__main__':
    unittest.main()
