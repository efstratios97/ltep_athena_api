from dataclasses import dataclass


@dataclass
class CustomOperation:
    custom_operation_func_signature: str

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, CustomOperation) else hash(self.custom_operation_func_signature) == hash(__o.custom_operation_func_signature)
