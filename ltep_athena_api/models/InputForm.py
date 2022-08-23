from dataclasses import dataclass
from enum import Enum, auto, unique


@unique
class InputFieldType(Enum):
    """This Class represents an Enum of possible Input Field Type Selection options"""
    DROP_DOWN = auto()
    MULTI_SELECT = auto()
    TEXT_INPUT_FIELD = auto()
    CALENDAR = auto()
    TIME_HORIZON = auto()


@dataclass
class InputField():
    """This Class represents an Input Field object"""
    title: str
    subtitle: str
    input_field_type: str
    input_field_parameter_from_dataset: str = None
    input_field_parameter_in_custom_operation: str = None
    input_field_retrieval_operation_name: str = None

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, InputField) else hash(self.title + self.subtitle + self.input_field_type + str(self.input_field_parameter_from_dataset) + str(self.input_field_retrieval_operation_name)) == hash(
            __o.title + __o.subtitle + __o.input_field_type + str(__o.input_field_parameter_from_dataset) + str(__o.input_field_retrieval_operation_name))


@dataclass
class InputFieldGroup():
    """This Class represents an Input Field Group object"""
    title: str
    subtitle: str

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, InputFieldGroup) else hash(self.title + self.subtitle) == hash(
            __o.title + __o.subtitle)


@dataclass
class InputFieldGroupSelectionOption():
    """This Class represents an InputFieldGroupSelectionOption object"""
    selection_option_button_text: str

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, InputFieldGroupSelectionOption) else hash(self.selection_option_button_text) == hash(__o.selection_option_button_text)
