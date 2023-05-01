from dataclasses import dataclass


from desktop.src.models.entity import Entity


@dataclass()
class Platform(Entity):
    id: int
    title: str
