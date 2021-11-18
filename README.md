# YaMDB - Final 

![yamdb_final](https://github.com/kimkanovsky/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## О проекте
Этот проект является частью учебной программы Backend-разработчика от Яндекс.Практикум. В ходе своего выполнения позволяет на практике отработать навыки по использованию Docker, CI (Continious Integration), GitHub Actions.

## Проект
http://51.250.8.75/

## Cсылка на инструкцию по установке Docker
[Docker](https://docs.docker.com/engine/install/ubuntu/) - ссылка на официальную документацию
[Docker-compose](https://docs.docker.com/compose/install/) - ссылка на установку

## Клонирование
Для установки с DockerHub:
```
docker pull kimkanovsky/yamdb:v1.1
```
## .env

При разворачивании проекта на сервере - переменные наполняются из GitHub Secrets. Не забудьте наполнить Secrets.

В приложении в целях безопасности переменные хранятся в .env файле

| Переменная | Дефолт | Описание |
| ------ | ------ | ------ |
| DB_ENGINE | django.db.backends.postgresql |Движок базы данных |
| DB_NAME | postgres |Название базы данных |
| POSTGRES_USER | postgres | Имя пользователя БД PostgreSQL |
| POSTGRES_PASSWORD | postgres | Пароль пользователя БД PostgreSQL |
| DB_HOST | db | Хост контейнер с БД|
| DB_PORT | 5432 | Стандартный порт PostgreSQL |
| SECRET_KEY | Ваш в settings.py проекта |  |

## Установка

Для разворачивания проекта на удаленном сервере потребуется сам сервер:
[Yandex.Cloud](https://cloud.yandex.ru/) - один из вариантов

После создания сервера для подключения к нему:
```
ssh <имя-пользователя>@<внешний-ip-сервера>
```

### docker-compose

Необходимо установить Docker, Docker-compose.

Далее - скопировать на сервер файлы docker-compose.yaml, nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно
```
scp [OPTION] [user@]SRC_HOST:]file1 [user@]DEST_HOST:]file2
```

Запустить сборку:
```
sudo docker-compose build
```
Поднять контейнеры:
```
sudo docker-compose up
```
Войти в контейнер приложения:
```
sudo docker exec -it <cont_id> bash
```
Провести миграции в контейнере приложения:
Выполяется в директории с manage.py
```
python manage.py migrate
```

ИЛИ

```
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

Запустить тесты в контейнере приложения:
```
pytest
```
Остановить контейнеры:
```
sudo docker-compose down
```

## Технологии
- [Python](https://www.python.org/) - ЯП
- [Django](https://www.djangoproject.com/) - Основной фреймворк
- [DjangoRestFramework](https://www.django-rest-framework.org/) - API модуль
- [Nginx](https://nginx.org/) - Сервер для раздачи статики 
- [Gunicorn](https://gunicorn.org/) - Сервер для работы с Django
- [Docker](https://www.docker.com/) - Контейнеризация

## Автор
KimKanovsky
Telegram: @kimkanovsky