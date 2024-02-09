## Установка

Вот основные инструкции по установке веб-сервиса `AutoVision`.

### Установка переменных окружения

Для корректной работы вам необходимо настроить следующие переменные окружения в файле ".env":

Заполните поле "Ваше значение" соответствующими значениями, которые вы хотите использовать для каждой переменной.

```shell
   POSTGRES_DB=POSTGRES_DB
   POSTGRES_USER=POSTGRES_USER
   POSTGRES_PASSWORD=POSTGRES_PASSWORD
   POSTGRES_HOST=POSTGRES_HOST
   POSTGRES_PORT=POSTGRES_PORT
   ALLOWED_HOSTS=ALLOWED_HOSTS
   SECRET_KEY=SECRET_KEY
   CSRF_TRUSTED_ORIGINS=CSRF_TRUSTED_ORIGINS
   PGADMIN_DEFAULT_EMAIL=pgadmin4@pgadmin.org
   PGADMIN_DEFAULT_PASSWORD=admin
```

### Запуск приложения

1. Сначала вам следует клонировать репозиторий на свой компьютер. Если вы еще этого не сделали, выполните следующую команду:
    ```
    git-clone https://github.com/
    ```

2. Перейдите в папку проекта:

    ```
    cd AutoVision
    ```

3. Запустите Docker Compose:

    ```
    docker-compose up -d --build
    ```

   Это запустит все необходимые службы, перечисленные в вашем "docker-compose.yml", включая ваше приложение Django, базу данных Postgres
   и другие.

### Работа с приложением

1. Чтобы войти в приложение, откройте веб-браузер и перейдите по ссылке:
    
~~~
http://localhost:8989/docs.
~~~

##### [Вернуться назад](./index.md)
