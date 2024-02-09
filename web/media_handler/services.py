from typing import Union

from web.common.base_service import BaseService
from web.media_handler.schemas import MediaCreateSchema, MediaUpdateSchema
from web.media_handler.repositories import MediaSqlRepository


class MediaService(BaseService):
    """
    This class manages operations related to media entities using a schema-based approach.
    It interacts with a repository (likely a database) to perform CRUD operations.
    """
    async def create(self, schema: MediaCreateSchema, url: str):
        """
        Description: Creates a new media record using the provided schema and URL.
        params:
            schema: An instance of MediaCreateSchema, containing the data for the new media record.
            url: A string representing the URL of the media.
        returns: The result of the commit operation (likely the newly created media record).
        """
        data = schema.model_dump()
        data.update({"url": url})
        commit = await self.repository.create(**data)
        return commit

    async def get_retrieve(self, pk: Union[str, int]):
        pass

    async def get_list(self):
        pass

    async def update(self, product_schema: MediaUpdateSchema, product_id: int):
        pass

    async def delete(self, product_id: int):
        pass


class MediaFormService(BaseService):
    """
    Similar to MediaService, but it uses a dictionary to handle data instead of a schema.
    """
    async def create(self, data: dict, url: str):
        """
        Description: Creates a new media record using the provided data dictionary and URL.
        params:
            data: A dictionary containing the data for the new media record.
            url: A string representing the URL of the media.
        returns: The result of the commit operation.
        """
        data.update({"url": url})
        commit = await self.repository.create(**data)
        return commit

    async def get_retrieve(self, pk: Union[str, int]):
        pass

    async def get_list(self):
        pass

    async def update(self, product_schema: MediaUpdateSchema, product_id: int):
        pass

    async def delete(self, product_id: int):
        pass


def media_depends_execute():
    """
    Description: Instantiates and returns a MediaService object with a MediaSqlRepository.
    Returns: An instance of MediaService.
    """
    return MediaService(MediaSqlRepository)


def media_form_depends_execute():
    """
    Description: Instantiates and returns a MediaFormService object with a MediaSqlRepository.
    Returns: An instance of MediaFormService.
    """
    return MediaFormService(MediaSqlRepository)
