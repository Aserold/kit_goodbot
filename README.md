# Kitbot
## _Бот для студентов СПБ ГБПОУ КИТ_

- Просмотр расписания
- Просмотр замен
- Почасовое обновление данных с 12 до 23

## Технологии

Dillinger uses a number of open source projects to work properly:

- [Python](https://www.python.org/)
- [Aiogram](https://github.com/aiogram/aiogram)
- [Docker](https://www.docker.com/)
- [Celery](https://github.com/celery/celery)

## Установка

Для запуска своего бота нужно установить Python 3.9+, [Docker](https://www.docker.com/get-started/)(docker-compose)

Для начала создайте своего бота, проделав следушие действия в чате [BotFather](https://t.me/BotFather).
Замените "Имя_бота" на имя вашего бота и "Bot_nameX_bot" на имя вашего бота с окончанием "bot".

![image](https://github.com/Aserold/kit_goodbot/assets/132985115/1033508d-e5c5-4416-a02f-d50b4e64868e)
Обратите внимание на токен.

Форкните или склонируйте репозиторий

```sh
git clone https://github.com/Aserold/kit_goodbot.git
```

В рабочем репозитории создайте файл ```.env``` и заполните данные:
```sh
TOKEN=
DB_HOST=localhost
DB_NAME=
DB_PASS=
DB_PORT=
DB_USER=
```
```TOKEN``` - вставьте токен от BotFather

Создайте и активируйте виртуальное окружение:

- На windows -
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- На linux -
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

Запустите ```docker-compose.yml```
```
  docker-compose up
```
или
```
  docker compose up
```

Выполните миграции
```
alembic upgrade head
```

Если вы хотите парсить данные с сайта, нужно запустить celery worker и celerybeat.
В разных терминалах запустите celery worker
```
celery -A tasks.tasks worker --loglevel=INFO
```
и celerybeat
```
celery -A tasks.tasks beat --loglevel=INFO
```

Данные должны загружаться по часам с 14 до 23.

Наконец запустите файл ```main.py```
```
venv/bin/python main.py
```

Зайдите по ссылке на вашего бота и запустите его коммандой ```/start``` и наслаждайтесь.
![image](https://github.com/Aserold/kit_goodbot/assets/132985115/00c2cd5d-fdfe-4743-873a-d20e3cb23a02)
