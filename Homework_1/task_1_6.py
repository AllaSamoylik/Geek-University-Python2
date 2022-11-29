from chardet import detect

data = [
    'сетевое программирование',
    'сокет',
    'декоратор'
]

# Заполняем файл, проверяем кодировку:
with open('test_file.txt', 'w+') as f:
    for data_str in data:
        f.write(f'{data_str}\n')
    f.seek(0)
    print(f'\nСодержимое файла (в формате {f.encoding}):\n{f.read()}')

# Пробуем открыть файл в UTF-8:
with open('test_file.txt', 'r', encoding='utf-8') as f:
    try:
        f.read()
    except UnicodeDecodeError:
        print(f'-> Попытка чтения в формате {f.encoding} - конфликт кодировок <-')

# Исправляем - проводим конвертации:
with open('test_file.txt', 'rb') as f:
    data_b = f.read()
    data_b_encoding = detect(data_b)['encoding']
    data_b_utf8 = data_b.decode(data_b_encoding).encode('utf-8')    # b_cp1251 -> str_cp1251 -> b_utf8
    data_b_utf8_encoding = detect(data_b_utf8)['encoding']
    data_str_utf8 = data_b_utf8.decode('utf-8')                     # b_utf8 -> str_utf8
    print(f'\nСодержимое файла (в формате {data_b_utf8_encoding}):\n{data_str_utf8}')
