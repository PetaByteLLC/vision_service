from web.common.base_repositories import DatabaseRepositoryInterface


class BaseService:
    """
    The BaseService class you've provided is designed to be a foundational class for service layers in a web application.
    It's structured to interact with a database through a repository, which follows the repository pattern.
    Here's an analysis of the class:
    """
    def __init__(self, repository: DatabaseRepositoryInterface) -> None:
        self.repository: DatabaseRepositoryInterface = repository()
