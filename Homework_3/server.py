import json
from socket import *
from sys import argv

DEFAULT_ADDR = 'localhost'
DEFAULT_PORT = 7777


def msg_processing(msg):
    if msg['action'] == 'presence' and 'time' in msg and msg['user']['account_name'] == 'alla':
        return {'response': 200}
    return {'response': 400, 'error': 'bad request'}


def main():
    try:
        if '-a' in argv:
            addr = argv[argv.index('-a') + 1]
        else:
            addr = DEFAULT_ADDR
    except IndexError:
        print('После параметра > -a < необходимо указать IP-адрес для прослушивания')
        exit(1)

    try:
        if '-p' in argv:
            port = int(argv[argv.index('-p') + 1])
            if not 1024 <= port <= 65535:
                raise ValueError('tcp-порт должен быть в пределах [1024;65535]')
        else:
            port = DEFAULT_PORT
    except IndexError:
        print('После параметра > -p < необходимо указать TCP-порт')
        exit(1)
    except ValueError as err:
        print(err)
        exit(1)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen(5)

    while True:
        try:
            client, client_addr = sock.accept()
        except KeyboardInterrupt:
            print('Соединение разорвано (принудительно)')
            sock.close()
            break
        print(f'\nУстановлено соединение: с {client_addr} на {client.getsockname()}')
        request_msg = client.recv(1024)
        decode_request_msg = json.loads(request_msg.decode('utf-8'))
        print(f'Сообщение от клиента: ', decode_request_msg)

        response_msg = msg_processing(decode_request_msg)
        client.send(json.dumps(response_msg).encode('utf-8'))
        client.close()


if __name__ == '__main__':
    main()
