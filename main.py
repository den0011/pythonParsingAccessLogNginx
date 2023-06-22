import re
import glob
import gzip
from collections import defaultdict

# Каталог с файлами журнала доступа
log_directory = 'logs/'

# Паттерны для поиска IP-адресов, User-Agent и путей запросов
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
user_agent_pattern = r'"([^"]*)"$'
path_pattern = r'"[A-Z]{3,} (.*?) HTTP'

# Получаем список файлов журнала доступа в указанном каталоге
log_files = glob.glob(log_directory + '*.*') + glob.glob(log_directory + '*.*.*') + glob.glob(log_directory + '*.*.*.*')

# Словари для хранения количества повторений IP-адресов, User-Agent и путей запросов
ip_counts = defaultdict(int)
user_agent_counts = defaultdict(int)
path_counts = defaultdict(int)

# Счетчик обработки файлов
file_counter = 0

# Парсим каждый файл журнала доступа
for file_path in log_files:
    file_counter += 1
    print(f"Обработка файла {file_counter}/{len(log_files)}: {file_path}")

    if file_path.endswith('.gz'):
        # Если файл сжат с помощью gzip, открываем его с помощью gzip.open
        with gzip.open(file_path, 'rt') as file:
            log_data = file.readlines()
    else:
        # Если файл не сжат, открываем его обычным способом
        with open(file_path, 'r') as file:
            log_data = file.readlines()

    # Ищем IP-адреса, User-Agent и пути запросов в каждой строке журнала доступа
    for line in log_data:
        ip_match = re.search(ip_pattern, line)
        user_agent_match = re.search(user_agent_pattern, line)
        path_match = re.search(path_pattern, line)

        if ip_match and user_agent_match and path_match:
            ip_address = ip_match.group()
            user_agent = user_agent_match.group(1)
            path = path_match.group(1)

            ip_counts[ip_address] += 1
            user_agent_counts[user_agent] += 1
            path_counts[path] += 1

# Сортируем IP-адреса по убыванию повторений
sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)

# Определение максимальной длины IP-адреса и количества повторений
max_ip_length = max(len(ip) for ip, _ in sorted_ips)
max_count_length = max(len(str(count)) for _, count in sorted_ips)

# Записываем данные IP-адресов в отдельный файл
ip_output_file = 'ip_statistics.txt'
with open(ip_output_file, 'w') as file:
    file.write('IP-адрес\tКоличество повторений\n')
    for ip, count in sorted_ips:
#        file.write(f'{ip}\t{count}\n')
        ip_padding = ' ' * (max_ip_length - len(ip))
        count_padding = ' ' * (max_count_length - len(str(count)))
        file.write(f'{ip}{ip_padding}\t{count}{count_padding}\n')


print(f"Данные IP-адресов сохранены в файл: {ip_output_file}")

# Записываем данные User-Agent в отдельный файл
user_agent_output_file = 'user_agent_statistics.txt'
with open(user_agent_output_file, 'w') as file:
    file.write('User-Agent\tКоличество повторений\n')
    for user_agent, count in user_agent_counts.items():
        file.write(f'{user_agent}\t{count}\n')

print(f"Данные User-Agent сохранены в файл: {user_agent_output_file}")

# Записываем данные путей запросов в отдельный файл, если запросов на один путь больше 10
path_output_file = 'path_statistics.txt'
with open(path_output_file, 'w') as file:
    file.write('Путь запроса\tКоличество повторений\n')
    for path, count in path_counts.items():
        if count > 10:
            file.write(f'{path}\t{count}\n')

print(f"Данные путей запросов сохранены в файл: {path_output_file}")
