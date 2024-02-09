## Настройка и подключение к базе данных

#### Для работы с базой данных в данном коде используется библиотека SQLAlchemy в асинхронном режиме (`sqlalchemy.ext.asyncio`) и библиотека `decouple` для чтения конфигурационных параметров из файла `.env`.

#### Перед использованием кода, убедитесь, что у вас есть файл .env, в котором содержатся следующие переменные:

    POSTGRES_USER: имя пользователя базы данных PostgreSQL.
    POSTGRES_PASSWORD: пароль пользователя базы данных PostgreSQL.
    POSTGRES_HOST: адрес хоста базы данных PostgreSQL.
    POSTGRES_DB: имя базы данных PostgreSQL.

#### Пример файла .env:
    
    POSTGRES_USER=myusername
    POSTGRES_PASSWORD=mypassword
    POSTGRES_HOST=localhost
    POSTGRES_DB=mydatabase

#### Код:

~~~python
from sqlalchemy.ext.asyncio import create_async_engine
from decouple import config

# Получение конфигурационных параметров из .env файла
username = config("POSTGRES_USER")
password = config("POSTGRES_PASSWORD")
host = config("POSTGRES_HOST")
dbname = config("POSTGRES_DB")

# Формирование URL для подключения к базе данных
database_url: str = (f"postgresql+asyncpg://{username}:{password}@{host}:5432/{dbname}")

# Создание асинхронного движка SQLAlchemy для работы с базой данных
engine = create_async_engine(str(database_url))
~~~

Вышеуказанный код читает конфигурационные параметры из файла .env, формирует URL для подключения к базе данных PostgreSQL и создает асинхронный движок SQLAlchemy для работы с этой базой данных.

##### [Вернуться назад](./index.md)