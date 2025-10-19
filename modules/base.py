from abc import ABC, abstractmethod


class BaseModule(ABC):

    name: str = "unnamed"
    version: str = "0.0.0"
    author: str = "unknown"

    @abstractmethod
    def get_widget(self):
        ...