## [Сервисы для работы с медиафайлами и зависимости для FastAPI](../../../../web/media_handler/services.py)

Данный код определяет сервисы и зависимости для работы с медиафайлами в вашем FastAPI-приложении. Сервисы `MediaService` и `MediaFormService` используются для выполнения операций с данными медиафайлов, а функции `media_depends_execute` и `media_form_depends_execute` определяют зависимости, которые используются при создании маршрутов в FastAPI.

### Сервисы

#### `MediaService`

- `create(self, schema: MediaCreateSchema, url: str)`: Создает запись в базе данных, используя данные из схемы `MediaCreateSchema` и URL медиафайла. Возвращает идентификатор созданной записи.

#### `MediaFormService`

- `create(self, data: dict, url: str)`: Создает запись в базе данных, используя данные из словаря `data` и URL медиафайла. Возвращает идентификатор созданной записи.

Оба сервиса также предоставляют методы для получения, обновления и удаления данных, но эти методы в данном коде не реализованы и оставлены для дальнейшей разработки.

### Зависимости

#### `media_depends_execute`

- Возвращает экземпляр `MediaService`, используя `MediaSqlRepository` в [качестве репозитория](./repositories.md). Эта зависимость может быть использована в FastAPI-маршрутах для выполнения операций с данными медиафайлов.

#### `media_form_depends_execute`

- Возвращает экземпляр `MediaFormService`, также используя `MediaSqlRepository` [качестве репозитория](./repositories.md). Эта зависимость может быть использована в FastAPI-маршрутах для выполнения операций с данными медиафайлов.

### Пример использования:

~~~python
# Создание записи в базе данных через MediaService
media_service = media_depends_execute()
new_media_id = await media_service.create(media_create_schema, "https://example.com/image.jpg")

# Создание записи в базе данных через MediaFormService
media_form_service = media_form_depends_execute()
new_media_id = await media_form_service.create(data_dict, "https://example.com/image.jpg")
~~~

##### [Вернуться назад](./index.md)