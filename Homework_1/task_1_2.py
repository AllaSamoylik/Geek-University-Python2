words_bytes = [
    b'class',
    b'function',
    b'method'
]

print('\n', 'байтовый тип'.center(35, '-'))
for word in words_bytes:
    print(f'{word} тип: {type(word)} длина: {len(word)}')
