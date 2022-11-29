import yaml

data_to_write = {
    'clothes': ['Jumper', 'Dress', 'T-shirt'],
    'quantity': 3,
    'prices': {'Jumper': '20€', 'Dress': '40€', 'T-shirt': '12€'}
}

with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data_to_write, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open('file.yaml', encoding='utf-8') as f:
    load_data = yaml.load(f, Loader=yaml.FullLoader)

print(f'Считанные данные: {load_data}')
print('> Файлы совпадают <' if load_data == data_to_write else '> Файлы не совпадают <')
