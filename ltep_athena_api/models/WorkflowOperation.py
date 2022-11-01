from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkflowOperation:
    name: str
    custom_operation_func_signature: str
    description: Optional[str] = None

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, WorkflowOperation) else hash(self.custom_operation_func_signature) == hash(__o.custom_operation_func_signature)
