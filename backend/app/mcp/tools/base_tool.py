from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = ""
    description = ""

    @abstractmethod
    async def execute(self, **kwargs):
        pass