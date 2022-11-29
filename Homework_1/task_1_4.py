words = [
    'разработка',
    'администрирование',
    'protocol',
    'standard'
]

for word in words:
    word_bytes = word.encode('utf-8')
    word_str = word_bytes.decode('utf-8')
    print(f'\nСлово "{word}": \nв байтовом формате - {word_bytes}, \nв строковом формате - {word_str}\n')
