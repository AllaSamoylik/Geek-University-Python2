import json
import socket
import logging
from log.client_log_config import cli_logger as to_log
from log.deco import log
from ipaddress import ip_address
from sys import argv
from socket import *
from datetime import datetime
from server import DEFAULT_ADDR, DEFAULT_PORT


@log(to_log)
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
            to_log.warning(f'Передано больше двух параметров - {cur_argv[1:]}')
            raise ValueError('максимальное количество параметров - 2: <addr> [<port>]')
    except ValueError:
        to_log.error(f'Соединение не установлено')
        exit(1)
    return addr, port


@log(to_log)
def check_ip(addr):
    if addr != ('localhost' or ip_address(addr)):
        to_log.warning(f"Ошибка в IP-адресе сервера - '{addr}'")
        raise ValueError('некорректный IP-адрес сервера')
    return addr


@log(to_log)
def check_port(port):
    if not 1024 <= port <= 65535:
        to_log.warning(f"Указанный tcp-порт выходит за диапазон 1024-65535 - '{port}'")
        raise ValueError('некорректный tcp-порт')
    return port


@log(to_log)
def answer_parsing(answer_from_server):
    if answer_from_server['response'] < 300:
        to_log.info(f'Ответ сервера: ОК')
        return 'ОК'
    to_log.error(f'Ответ сервера: {answer_from_server["error"]}')
    return f'! {answer_from_server["error"]} !'


@log(to_log)
def msg_creating(account_name="alla"):
    msg = {
        'action': 'presence',
        'time': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'user': {
            'account_name': account_name,
            'status': 'online'
        }
    }
    to_log.info('Данные созданы')
    return msg


@log(to_log)
def msg_conversion(msg):
    if isinstance(msg, bytes):
        converted_message = json.loads(msg.decode('utf-8'))
        to_log.info('Успешная конвертация (-> json)')
    else:
        converted_message = json.dumps(msg).encode('utf-8')
        to_log.info('Успешная конвертация (json ->)')
    return converted_message


def main():
    sock = socket(AF_INET, SOCK_STREAM)

    to_log.info(f'Попытка соединения с сервером')
    srv_address = set_addr_port(argv)
    try:
        sock.connect(srv_address)
    except ConnectionRefusedError as err:
        to_log.error('Сервер {}:{} отверг запрос на соединение'.format(*srv_address))
        exit(1)
    else:
        to_log.info('Соединение c сервером {}:{} установлено'.format(*srv_address))

    to_log.info('Клиент отправляет данные на сервер:')
    msg = msg_creating()
    sock.send(msg_conversion(msg))
    to_log.info('Данные отправлены')

    to_log.info('Клиент принимает данные от сервера:')
    try:
        answer = sock.recv(1024)
    except ConnectionResetError as err:
        to_log.error('Сервер {}:{} принудительно разорвал соединение'.format(*srv_address))
        exit(1)
    else:
        decode_answer = msg_conversion(answer)
        print('Ответ сервера: ', answer_parsing(decode_answer))


if __name__ == '__main__':
    main()
