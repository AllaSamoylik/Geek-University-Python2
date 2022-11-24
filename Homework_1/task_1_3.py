words = [
    'attribute',
    'класс',
    'функция',
    'type'
]

for word in words:
    try:
        word.encode('ascii')
    except UnicodeError:
        print(f'\nСлово "{word}" невозможно записать в байтовом типе (с помощью ASCII)')
