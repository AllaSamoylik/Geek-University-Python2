import unittest
from client import *


class TestClient(unittest.TestCase):
    def test_check_ip_localhost(self):
        self.assertEqual(check_ip('localhost'), 'localhost')

    def test_check_ip_incorrect(self):
        with self.assertRaises(ValueError) as e:
            check_ip('1270.0.0.1')
        the_exception = str(e.exception)
        self.assertEqual(the_exception, 'некорректный IP-адрес сервера')

    def test_check_port_correct(self):
        self.assertEqual(check_port(10000), 10000)

    def test_check_port_big(self):
        with self.assertRaises(ValueError) as e:
            check_port(99999)
        the_exception = str(e.exception)
        self.assertEqual(the_exception, 'некорректный tcp-порт')

    def test_answer_parsing_2xx(self):
        self.assertEqual(answer_parsing({'response': 200}), 'ОК')

    def test_answer_parsing_4xx(self):
        self.assertEqual(answer_parsing({'response': 403, 'error': 'forbidden'}), '! forbidden !')

    def test_msg_creating_name(self):
        self.assertEqual(msg_creating('max'),
                         {
                             'action': 'presence',
                             'time': datetime.now().strftime("%d-%m-%Y %H:%M"),
                             'user': {
                                 'account_name': 'max',
                                 'status': 'online'
                             }
                         })

    def test_msg_creating_noname(self):
        self.assertEqual(msg_creating(),
                         {
                             'action': 'presence',
                             'time': datetime.now().strftime("%d-%m-%Y %H:%M"),
                             'user': {
                                 'account_name': 'alla',
                                 'status': 'online'
                             }
                         })

    def test_msg_conversion_dict(self):
        self.assertEqual(msg_conversion({'action': 'presence'}), b'{"action": "presence"}')

    def test_msg_conversion_bytes(self):
        self.assertEqual(msg_conversion(b'{"action": "presence"}'), {'action': 'presence'})

    def test_set_addr_port_all(self):
        self.assertEqual(set_addr_port(['client.py', 'localhost', '10000']), ('localhost', 10000))

    def test_set_addr_port_addr(self):
        self.assertEqual(set_addr_port(['client.py', 'localhost']), ('localhost', 7777))

    def test_set_addr_port_empty(self):
        self.assertEqual(set_addr_port(['client.py']), ('localhost', 7777))

    def test_set_addr_port_over(self):
        with self.assertRaises(SystemExit):
            set_addr_port(['client.py', 'localhost', '10000', 'test'])


if __name__ == '__main__':
    unittest.main()
