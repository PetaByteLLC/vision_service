from typing import Dict, Union

from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete, update

from web.database.database import async_session_maker


class DatabaseRepositoryInterface(ABC):
    """
    This class defines a set of methods that any concrete repository class should implement.
    Being an abstract base class (ABC), it cannot be instantiated directly and only serves as a blueprint.
    """
    @abstractmethod
    async def get_retrieve(self, pk: Union[str, int], *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pk: Union[str, int], *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, pk: Union[str, int], data: Dict, *args, **kwargs):
        raise NotImplementedError


class SqlQueryRepository(DatabaseRepositoryInterface):

    """
    SqlQueryRepository is an implementation of DatabaseRepositoryInterface.
    It defines how each method of the interface is carried out using SQLAlchemy and async database sessions.
    """

    model = None

    async def get_retrieve(self, pk: Union[str, int]) -> Dict:
        async with async_session_maker() as session:
            statement = select(self.model).where(self.model.id == pk)
            result = await session.execute(statement)
            result_data = [row[0] for row in result.all()]
            return result_data

    async def get_list(self) -> Dict:
        async with async_session_maker() as session:
            statement = select(self.model)
            result = await session.execute(statement)
            result_data = [i[0] for i in result.all()]
            return result_data

    async def create(self, **kwargs) -> int:
        async with async_session_maker() as session:
            statement = insert(self.model).values(**kwargs).returning(self.model.id)
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one()

    async def update(self, data: Dict, pk: int):
        async with async_session_maker() as session:
            statement = (
                update(self.model)
                .where(self.model.id == pk)
                .values(**data)
                .returning(self.model.id)
            )
            result = await session.execute(statement)
            await session.commit()
            return result.scalar()

    async def delete(self, pk: Union[str, int]) -> int:
        async with async_session_maker() as session:
            statement = (
                delete(self.model).where(self.model.id == pk).returning(self.model.id)
            )
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one()
