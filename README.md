# **Foodgram-project**

Дипломный проект в рамках профессии Яндекс.Практикума python-разработчик.
Foodgram - онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

В данный момент проект реализован только локально. Однако в ближайшей перспективе добавить в него CI. Добавить тестировение при изменений ветки мастер. Добавить автоматическое развертывае на сервере с использованием docker-compose. Заменить SQLite на PostgreSQL.

При работе над проектом использован стек технологий: Django, Python, PostgreSQL, Nginx, Docer, TDD, код написанв в IDE PyCharm OS Linux Mint  

## Разворачивание проекта

1.  Склонируйте проект

        docker-compose up --build

        docker-compose exec web bash

        python manage.py migrate

        python manage.py createsuperuser

        python manage.py load_product_data

        python manage.py collectstatic

2.  Выполните миграции

        ./manage.py migrate

3.  Создайте суперпользователя

        ./manage.py createsuperuser

4.  Добавте в базу прдукты и теги

        python manage.py create_main_tags
