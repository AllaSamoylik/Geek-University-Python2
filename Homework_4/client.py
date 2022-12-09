import json
import socket
from ipaddress import ip_address
from sys import argv
from socket import *
from datetime import datetime
from server import DEFAULT_ADDR, DEFAULT_PORT


def set_addr_port(cur_argv):
    try:
        if len(cur_argv) <= 3:
            if len(cur_argv) > 1:
                addr = check_ip(cur_argv[1])
                if len(cur_argv) > 2:
                    port = check_port(int(cur_argv[2]))
                else:
                    port = DEFAULT_PORT
            else:
                addr = DEFAULT_ADDR
                port = DEFAULT_PORT
        else:
            raise ValueError('максимальное количество параметров - 2: <addr> [<port>]')
    except ValueError as err:
        print(err)
        exit(1)
    return addr, port


def check_ip(addr):
    if addr != ('localhost' or ip_address(addr)):
        raise ValueError('некорректный IP-адрес сервера')
    return addr


def check_port(port):
    if not 1024 <= port <= 65535:
        raise ValueError('некорректный tcp-порт')
    return port


def answer_parsing(answer_from_server):
    if answer_from_server['response'] < 300:
        return 'ОК'
    return f'! {answer_from_server["error"]} !'


def msg_creating(account_name='alla'):
    msg = {
        'action': 'presence',
        'time': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'user': {
            'account_name': account_name,
            'status': 'online'
        }
    }
    return msg


def msg_conversion(msg):
    if isinstance(msg, bytes):
        converted_message = json.loads(msg.decode('utf-8'))
    else:
        converted_message = json.dumps(msg).encode('utf-8')
    return converted_message


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((set_addr_port(argv)))

    msg = msg_creating()
    sock.send(msg_conversion(msg))

    answer = sock.recv(1024)
    decode_answer = msg_conversion(answer)
    print('Ответ сервера: ', answer_parsing(decode_answer))


if __name__ == '__main__':
    main()
