import json
import logging
from log.server_log_config import srv_logger as to_log
from log.deco import log
from socket import *
from ipaddress import ip_address
from sys import argv

DEFAULT_ADDR = 'localhost'
DEFAULT_PORT = 7777


@log(to_log)
def set_addr_port(cur_argv):
    addr = DEFAULT_ADDR
    port = DEFAULT_PORT

    try:
        if '-a' in cur_argv:
            try:
                addr_value = cur_argv[cur_argv.index('-a') + 1]
            except IndexError:
                to_log.error(f'Не указан IP-адрес. Сокет не был привязан')
                exit(1)
            else:
                addr = check_ip(addr_value)
    except ValueError:
        to_log.error(f'Сокет не был привязан')
        exit(1)
    try:
        if '-p' in cur_argv:
            try:
                port_value = int(cur_argv[cur_argv.index('-p') + 1])
            except ValueError:
                to_log.error(f'Указанный tcp-порт не является числом. Сокет не был привязан')
                exit(1)
            except IndexError:
                to_log.error(f'Не указан tcp-порт. Сокет не был привязан')
                exit(1)
            else:
                port = check_port(port_value)
    except ValueError:
        to_log.error(f'Сокет не был привязан')
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
def msg_processing(msg):
    if msg['action'] == 'presence' and ('time' in msg) and (msg['user']['account_name'] == 'alla'):
        to_log.info('Ответ положительный')
        return {'response': 200}
    to_log.info('Ответ отрицательный')
    return {'response': 400, 'error': 'bad request'}


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

    to_log.info(f'Попытка привязки сокета')
    sock_address = set_addr_port(argv)
    sock.bind(sock_address)
    sock.listen(5)
    to_log.info('Сокет привязан к {}:{}'.format(*sock_address))

    while True:
        try:
            to_log.info('Ожидание соединения...')
            client, client_addr = sock.accept()
        except KeyboardInterrupt:
            to_log.error('Соединение разорвано принудительно')
            sock.close()
            break
        to_log.info('Установлено соединение с клиентом {}:{}'.format(*client_addr))

        to_log.info('Сервер получает данные от клиента:')
        request_msg = client.recv(1024)
        decode_request_msg = msg_conversion(request_msg)
        to_log.info('Данные получены')
        print(f'Сообщение от клиента: ', decode_request_msg)

        to_log.info('Сервер готовит ответ клиенту:')
        response_msg = msg_processing(decode_request_msg)
        client.send(msg_conversion(response_msg))
        to_log.info('Ответ отправлен')

        client.close()
        to_log.info('Соединение с клиентом {}:{} закрыто'.format(*client_addr))


if __name__ == '__main__':
    main()
