class RepositoryError(Exception):
    ...


class NotFoundError(RepositoryError):
    ...


class UniqueViolationError(RepositoryError):
    ...


class ForeignKeyViolationError(RepositoryError):
    ...
