# Python Parsing Access Log Nginx

Создаем каталог **logs** и копируем туда файлы лога nginx access log.
Поддерживает **gz** формат.

Для примера (формат расширений файла для парсинга):
- access.log
- access.log.1
- access.log.2.gz
- access.log.3.gz
- и тд...

По умолчанию лог расположен в (ubuntu): **/var/log/nginx**

Написано на python 3.10
