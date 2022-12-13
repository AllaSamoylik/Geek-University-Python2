import logging.handlers
from pathlib import Path

log_path = Path(__file__).parent.parent / 'logs'
log_path.mkdir(exist_ok=True)

# Логгер
srv_logger = logging.getLogger('server')
srv_logger.setLevel(logging.DEBUG)

# Хэндлер (вывод в файл)
srv_handler = logging.handlers.TimedRotatingFileHandler(log_path / 'server.log',
                                                        when='midnight', interval=1, encoding='utf-8')
srv_handler.suffix = "%Y%m%d"
srv_handler.setLevel(logging.DEBUG)

# Форматтер
strfmt = '%(asctime)s  %(levelname)-8s [%(module)s] >>> %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
srv_formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
srv_handler.setFormatter(srv_formatter)

# Хэндлер -> в логгер
srv_logger.addHandler(srv_handler)


if __name__ == '__main__':
    # Хэндлер (вывод в терминал)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(srv_formatter)
    srv_logger.addHandler(console_handler)
    # Проверка записи
    srv_logger.error('error')
    srv_logger.critical('critical')
