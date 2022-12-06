import json
import socket
from sys import argv
from socket import *
from datetime import datetime
from server import DEFAULT_ADDR, DEFAULT_PORT


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


def answer_parsing(answer_from_server):
    if answer_from_server['response'] == 200:
        return 'ОК'
    return f'> {answer_from_server["error"]} <'


def main():
    try:
        addr = argv[1]
        port = int(argv[2])
        if not 1024 <= port <= 65535:
            raise ValueError('tcp-порт должен быть в пределах [1024;65535]')
    except IndexError:
        addr = DEFAULT_ADDR
        port = DEFAULT_PORT
    except ValueError as err:
        print(err)
        exit(1)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((addr, port))

    msg = msg_creating()
    sock.send(json.dumps(msg).encode('utf-8'))

    answer = sock.recv(1024)
    decode_answer = json.loads(answer.decode('utf-8'))
    print('Ответ сервера: ', answer_parsing(decode_answer))


if __name__ == '__main__':
    main()
