# Clean Architecture

This project is described a clean architecture written by Robert C. Martine.
Architecture is fellow a [clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)



## Table of contents

- [Features](#features)
- [Directory Structure](#diretorystructure)
- [Installation](#installation)
- [Example](#example)
- [Testing](#testing)

## DirectoryStructure

```bash
|-- clean_architecture
|    |-- domain
|    |	|-request_object.py
|    |	|-response_object.py
|    |	`-use_case.py
|    |-- entity
|    |	`-entity.py
|    |-- exception
|    |	|-exception.py
|    |	`- *_exception.py
|    |-- serializer
|    	`-serializer.py
```

## Installation

```bash
pip install clean-architecture
```

## Example

- Entity

```python
from clean_architecture.entity import Entity

class UserEntity(Entity):
    def __init__(
        self,
        user_id,
        name,
        created_at,
        updated_at
    ):
        self.id = user_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, adict):
        user = UserEntity(
            user_id=adict.get("id"),
            name=adict.get("name"),
            created_at=adict.get("created_at"),
            updated_at=adict.get("updated_at")
        )
        return user
```

- Domain

    - ValidRequestObject
    ```python
        from clean_architecture.domain import (
            ValidRequestObject,
            InvalidRequestObject,
            UseCase,
            ResponseSuccess
        )
        
        class CreateUserRequestObject(ValidRequestObject):
            def __init__(self, user):
                self.user = user

            if invalid_req.has_errors():
                return invalid_req
            
            return CreateUserRequestObject(
                user=UserEntity.from_dict(adict)
            )
    ```
    - UseCase
    ```python
        class CreatedUser(UseCase):
            def __init__(self, user_repository):
                self.user_repository = user_repository

            def process_request(self, request_object):
                user = self.user_repository.create(user=request_object.user)
                return ResponseSuccess(201, user)
    ```

- Serializer

```python
    from schema import Schema
    from clean_architecture.serializer import Serializer

    class CreateUserEncoder(Serializer):
        schema = Schema(
            {
                "name": str
            },
            ignore_extra_keys=True
        )
```

## Testing

```bash
$ pytest 
```
