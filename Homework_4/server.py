import json
from socket import *
from ipaddress import ip_address
from sys import argv

DEFAULT_ADDR = 'localhost'
DEFAULT_PORT = 7777


def set_addr_port(cur_argv):
    addr = DEFAULT_ADDR
    port = DEFAULT_PORT

    try:
        if '-a' in cur_argv:
            try:
                addr_value = cur_argv[cur_argv.index('-a') + 1]
            except IndexError:
                print('некорректный IP-адрес для прослушивания (не указан)')
                exit(1)
            else:
                addr = check_ip(addr_value)
    except ValueError as err:
        print(err)
        exit(1)
    try:
        if '-p' in cur_argv:
            try:
                port_value = int(cur_argv[cur_argv.index('-p') + 1])
            except ValueError:
                print('некорректный tcp-порт (не является числом)')
                exit(1)
            except IndexError:
                print('некорректный tcp-порт (не указан)')
                exit(1)
            else:
                port = check_port(port_value)
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


def msg_processing(msg):
    if msg['action'] == 'presence' and ('time' in msg) and (msg['user']['account_name'] == 'alla'):
        return {'response': 200}
    return {'response': 400, 'error': 'bad request'}


def msg_conversion(msg):
    if isinstance(msg, bytes):
        converted_message = json.loads(msg.decode('utf-8'))
    else:
        converted_message = json.dumps(msg).encode('utf-8')
    return converted_message


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((set_addr_port(argv)))
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
        decode_request_msg = msg_conversion(request_msg)
        print(f'Сообщение от клиента: ', decode_request_msg)
        response_msg = msg_processing(decode_request_msg)
        client.send(msg_conversion(response_msg))
        client.close()


if __name__ == '__main__':
    main()
