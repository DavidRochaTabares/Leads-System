from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseWorker(ABC):
    @abstractmethod
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_task_data(self, task_data: Dict[str, Any]) -> bool:
        pass
