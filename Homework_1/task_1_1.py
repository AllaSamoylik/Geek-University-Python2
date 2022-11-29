def get_content_and_type(variables):
    for var in variables:
        print(f'"{var}" тип: {type(var)}')


words = [
    'разработка',
    'сокет',
    'декоратор'
]
words_uni = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
]

print('\n', 'str формат'.center(30, '-'))
get_content_and_type(words)
print('\n', 'unicode формат'.center(30, '-'))
get_content_and_type(words_uni)
