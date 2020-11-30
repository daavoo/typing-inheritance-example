import uuid
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

# Base Repository ############################################


class IRepository:

    __metaclass__ = ABCMeta

    @classmethod
    def info(cls):
        return {"name": cls.__name__}

    @abstractmethod
    def save(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError


# User Specific Repository ####################################


@dataclass
class User:
    user_id: str
    name: str


class IUserRepository(IRepository):

    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, user_id: str) -> User:
        raise NotImplementedError


# In Memory implementation of User Specific Repository #########
class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User):
        if user.user_id in self.users:
            raise FileExistsError()
        self.users[user.user_id] = user

    def retrieve(self, user_id: str) -> User:
        if user_id not in self.users:
            raise FileNotFoundError()
        return self.users.get(user_id)


def create_random_user(repository: IUserRepository):
    user = User(user_id=str(uuid.uuid4()), name="Davila")
    repository.save(user)


def repository_provider(name: str) -> IRepository:
    if name == "user":
        return InMemoryUserRepository()
    else:
        raise FileNotFoundError()


repository = repository_provider("user")
create_random_user(repository)
