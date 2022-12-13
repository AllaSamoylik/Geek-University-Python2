import logging
from pathlib import Path

log_path = Path(__file__).parent.parent / 'logs'
log_path.mkdir(exist_ok=True)

# Логгер
cli_logger = logging.getLogger('client')
cli_logger.setLevel(logging.DEBUG)

# Хэндлер (вывод в файл)
cli_handler = logging.FileHandler(log_path / 'client.log', encoding='utf-8')
cli_handler.setLevel(logging.DEBUG)

# Форматтер
strfmt = '%(asctime)s  %(levelname)-8s [%(module)s] >>> %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
cli_formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
cli_handler.setFormatter(cli_formatter)

# Хэндлер -> в логгер
cli_logger.addHandler(cli_handler)


if __name__ == '__main__':
    # Хэндлер (вывод в терминал)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(cli_formatter)
    cli_logger.addHandler(console_handler)
    # Проверка записи
    cli_logger.info('info')
    cli_logger.critical('critical')
