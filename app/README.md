## Парсер сайта МТС

Основные функции:
Извлекает данные с сайта МТС об услугах.
Фильтрирует и сортирует указанные данные на странице.


### Переменные среды
Переименовать файл .env.example в .env и установите свои данные

### Команды для запуска

1. Миграция и заполнение баз тестовыми данным: 
Запустите файл entrypoint.sh или выполните команды внизу:
```
python manage.py makemigrations
python manage.py migrate
python manage.py run_parser
python manage.py runserver 0.0.0.0:8000
```
2. Для выгрузки фикстур с командной строки наберите:
```
python manage.py dumpdata rate > tests/fixtures/rate-fixtures.json
```

### Сайт
```
http://127.0.0.1:8000
```