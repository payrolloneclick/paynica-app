class RepositoryException(Exception):
    pass


class ObjectAlreadyExists(RepositoryException):
    pass


class ObjectDoesNotExist(RepositoryException):
    pass
