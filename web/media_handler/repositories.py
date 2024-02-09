from web.common.base_repositories import SqlQueryRepository

from web.media_handler.models import Media


class MediaSqlRepository(SqlQueryRepository):
    """
    The MediaSqlRepository class you've provided is a simple extension of a base repository class,
    SqlQueryRepository, specifically tailored for handling database operations related to the Media model.
    This class is a part of the repository pattern implementation,
    which separates the data access logic from the business logic of your application.
    Here's a breakdown of its structure and functionality:
    """
    model = Media
