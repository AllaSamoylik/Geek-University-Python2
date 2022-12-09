import json
import socket
import logging
from log.client_log_config import cli_logger as _log
from ipaddress import ip_address
from sys import argv
from socket import *
from datetime import datetime
from server import DEFAULT_ADDR, DEFAULT_PORT


def set_addr_port(cur_argv):
    addr = DEFAULT_ADDR
    port = DEFAULT_PORT

    try:
        if len(cur_argv) <= 3:
            if len(cur_argv) > 1:
                addr = check_ip(cur_argv[1])
                if len(cur_argv) > 2:
                    port = check_port(int(cur_argv[2]))
                else:
                    port = DEFAULT_PORT
        else:
            _log.warning(f'Передано больше двух параметров - {cur_argv[1:]}')
            raise ValueError('максимальное количество параметров - 2: <addr> [<port>]')
    except ValueError:
        _log.error(f'Соединение не установлено')
        exit(1)
    return addr, port


def check_ip(addr):
    if addr != ('localhost' or ip_address(addr)):
        _log.warning(f"Ошибка в IP-адресе сервера - '{addr}'")
        raise ValueError('некорректный IP-адрес сервера')
    return addr


def check_port(port):
    if not 1024 <= port <= 65535:
        _log.warning(f"Указанный tcp-порт выходит за диапазон 1024-65535 - '{port}'")
        raise ValueError('некорректный tcp-порт')
    return port


def answer_parsing(answer_from_server):
    if answer_from_server['response'] < 300:
        _log.info(f'Ответ сервера: ОК')
        return 'ОК'
    _log.error(f'Ответ сервера: {answer_from_server["error"]}')
    return f'! {answer_from_server["error"]} !'


def msg_creating(account_name='alla'):
    msg = {
        'action': 'presence',
        'tme': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'user': {
            'account_name': account_name,
            'status': 'online'
        }
    }
    _log.info('Данные созданы')
    return msg


def msg_conversion(msg):
    if isinstance(msg, bytes):
        converted_message = json.loads(msg.decode('utf-8'))
        _log.info('Успешная конвертация (-> json)')
    else:
        converted_message = json.dumps(msg).encode('utf-8')
        _log.info('Успешная конвертация (json ->)')
    return converted_message


def main():
    sock = socket(AF_INET, SOCK_STREAM)

    _log.info(f'Попытка соединения с сервером')
    srv_address = set_addr_port(argv)
    try:
        sock.connect(srv_address)
    except ConnectionRefusedError as err:
        _log.error('Сервер {}:{} отверг запрос на соединение'.format(*srv_address))
        exit(1)
    else:
        _log.info('Соединение c сервером {}:{} установлено'.format(*srv_address))

    _log.info('Клиент отправляет данные на сервер')
    msg = msg_creating()
    sock.send(msg_conversion(msg))
    _log.info('Данные отправлены')

    _log.info('Клиент принимает данные от сервера')
    try:
        answer = sock.recv(1024)
    except ConnectionResetError as err:
        _log.error('Сервер {}:{} принудительно разорвал соединение'.format(*srv_address))
        exit(1)
    else:
        decode_answer = msg_conversion(answer)
        print('Ответ сервера: ', answer_parsing(decode_answer))


if __name__ == '__main__':
    main()
