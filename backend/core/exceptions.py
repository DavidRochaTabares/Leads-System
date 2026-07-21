class DomainException(Exception):
    pass


class EntityNotFoundError(DomainException):
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class ValidationError(DomainException):
    pass


class AuthenticationError(DomainException):
    pass


class AuthorizationError(DomainException):
    pass
