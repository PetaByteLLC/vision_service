### [Интерфейс репозитория базы данных и реализация через SQL-запросы](../../../../web/common/base_repositories.py)

Ваш код определяет интерфейс `DatabaseRepositoryInterface`, который предоставляет методы для взаимодействия с базой данных. Также вы предоставляете реализацию этого интерфейса в классе `SqlQueryRepository`, который использует SQLAlchemy для выполнения SQL-запросов к базе данных.

#### Интерфейс DatabaseRepositoryInterface

Интерфейс `DatabaseRepositoryInterface` является абстрактным базовым классом, который определяет методы для основных операций с базой данных. Каждый метод принимает различные аргументы и аннотированы для асинхронной работы.

#### Методы интерфейса

- `get_retrieve(self, pk: Union[str, int], *args, **kwargs)`: Получает данные по первичному ключу `pk`.
- `get_list(self, *args, **kwargs)`: Получает список данных из базы данных.
- `create(self, *args, **kwargs)`: Создает новую запись в базе данных.
- `delete(self, pk: Union[str, int], *args, **kwargs)`: Удаляет запись из базы данных по первичному ключу `pk`.
- `update(self, pk: Union[str, int], data: Dict, *args, **kwargs)`: Обновляет запись в базе данных по первичному ключу `pk` с использованием данных из словаря `data`.

#### Реализация через SqlQueryRepository

Класс `SqlQueryRepository` реализует интерфейс `DatabaseRepositoryInterface` и предоставляет методы для выполнения SQL-запросов с использованием SQLAlchemy.

##### Поле `model`

В этом классе определено поле `model`, которое предполагается указать как модель SQLAlchemy, с которой будет взаимодействовать репозиторий.

##### Методы репозитория

- `get_retrieve(self, pk: Union[str, int]) -> Dict`: Получает данные по первичному ключу `pk`. Метод использует `async_session_maker` для выполнения запроса.
- `get_list(self) -> Dict`: Получает список данных из базы данных. Метод также использует `async_session_maker` для выполнения запроса.
- `create(self, **kwargs) -> int`: Создает новую запись в базе данных, используя переданные аргументы. Метод возвращает идентификатор созданной записи.
- `update(self, data: Dict, pk: int)`: Обновляет запись в базе данных, используя данные из словаря `data` и первичный ключ `pk`.
- `delete(self, pk: Union[str, int]) -> int`: Удаляет запись из базы данных по первичному ключу `pk`.

### Использование

Пример использования интерфейса и его реализации:

~~~python
# Создание объекта репозитория
repo = SqlQueryRepository()

# Получение данных по первичному ключу
data = await repo.get_retrieve(1)

# Получение списка данных
data_list = await repo.get_list()

# Создание новой записи
new_id = await repo.create(field1=value1, field2=value2)

# Обновление записи
await repo.update(new_data, new_id)

# Удаление записи
await repo.delete(new_id)
~~~
##### [Вернуться назад](./index.md)