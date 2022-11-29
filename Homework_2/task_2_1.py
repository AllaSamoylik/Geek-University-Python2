import os
import csv
import re
from chardet import detect


def get_data():
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    idx = 0
    files = os.scandir(os.getcwd())

    for file in files:
        if file.is_file() and file.name.startswith('info_'):
            with open(file.name, 'rb') as f:

                for line in f:
                    line_encoding = detect(line)['encoding']
                    f_line = line.decode(encoding=line_encoding).rstrip()
                    if (match := re.search(r'^([^:]+): *(.*)', f_line)) is not None:
                        if match.group(1) == 'Изготовитель системы':
                            os_prod_list.append(match.group(2))
                        elif match.group(1) == 'Название ОС':
                            os_name_list.append(match.group(2))
                        elif match.group(1) == 'Код продукта':
                            os_code_list.append(match.group(2))
                        elif match.group(1) == 'Тип системы':
                            os_type_list.append(match.group(2))
                main_data.extend([[os_prod_list[idx], os_name_list[idx], os_code_list[idx], os_type_list[idx]]])
                idx += 1

    print(f"{'os_prod_list:':<15} {os_prod_list}")
    print(f"{'os_name_list:':<15} {os_name_list}")
    print(f"{'os_code_list:':<15} {os_code_list}")
    print(f"{'os_type_list:':<15} {os_type_list}")
    print(f"{'main_data:':<15} {main_data}")
    return main_data


def write_to_csv(csv_file):
    data_to_write = get_data()
    with open(csv_file, 'w', encoding='utf-8', newline="") as f:
        f_writer = csv.writer(f)
        f_writer.writerows(data_to_write)
    return print(f'\nДанные сохранены в <{csv_file}>')


write_to_csv('file.csv')
