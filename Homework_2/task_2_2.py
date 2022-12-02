import os
import json
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    order = {'item': item,
             'quantity': quantity,
             'price': price,
             'buyer': buyer,
             'date': date.strftime("%d-%m-%Y %H:%M")
             }
    files = os.scandir(os.getcwd())

    for file in files:
        if file.is_file() and file.name.startswith('orders'):
            with open(file.name, encoding='utf-8') as f:
                data_json = json.load(f)
                data_json['orders'].append(order)
            with open('orders.json', 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)
            print(f'Информация о заказе сохранена в <{file.name}>')


write_order_to_json('Пицца', 2, 1500, 'Сергей', datetime.now())
write_order_to_json('Суши', 1, 800, 'Alex', datetime.now())
