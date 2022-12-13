import json
import logging
from log.server_log_config import srv_logger as _log
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
                _log.error(f'Не указан IP-адрес. Сокет не был привязан')
                exit(1)
            else:
                addr = check_ip(addr_value)
    except ValueError:
        _log.error(f'Сокет не был привязан')
        exit(1)
    try:
        if '-p' in cur_argv:
            try:
                port_value = int(cur_argv[cur_argv.index('-p') + 1])
            except ValueError:
                _log.error(f'Указанный tcp-порт не является числом. Сокет не был привязан')
                exit(1)
            except IndexError:
                _log.error(f'Не указан tcp-порт. Сокет не был привязан')
                exit(1)
            else:
                port = check_port(port_value)
    except ValueError:
        _log.error(f'Сокет не был привязан')
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


def msg_processing(msg):
    if msg['action'] == 'presence' and ('time' in msg) and (msg['user']['account_name'] == 'alla'):
        _log.info('Ответ положительный')
        return {'response': 200}
    _log.info('Ответ отрицательный')
    return {'response': 400, 'error': 'bad request'}


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

    _log.info(f'Попытка привязки сокета')
    sock_address = set_addr_port(argv)
    sock.bind(sock_address)
    sock.listen(5)
    _log.info('Сокет привязан к {}:{}'.format(*sock_address))

    while True:
        try:
            _log.info('Ожидание соединения...')
            client, client_addr = sock.accept()
        except KeyboardInterrupt:
            _log.error('Соединение разорвано принудительно')
            sock.close()
            break
        _log.info('Установлено соединение с клиентом {}:{}'.format(*client_addr))

        _log.info('Сервер получает данные от клиента')
        request_msg = client.recv(1024)
        decode_request_msg = msg_conversion(request_msg)
        _log.info('Данные получены')
        print(f'Сообщение от клиента: ', decode_request_msg)

        _log.info('Сервер готовит ответ клиенту')
        response_msg = msg_processing(decode_request_msg)
        client.send(msg_conversion(response_msg))
        _log.info('Ответ отправлен')

        client.close()
        _log.info('Соединение с клиентом {}:{} закрыто'.format(*client_addr))


if __name__ == '__main__':
    main()
