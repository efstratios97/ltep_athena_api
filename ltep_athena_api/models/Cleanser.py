from dataclasses import dataclass
from typing import Optional


@dataclass
class Cleanser:
    '''This Object represents a Cleanser Object. You can use the CleanserManager in your LTEP Athena Platform. 
    Each cleanser consists of metadata and an data manipulation and/or cleansing operation.
    :param str name: name of cleanser
    :param Optional[str] description: description of cleanser
    :param str dataset_label: the dataset label (type of dataset/dataset family) your cleanser shall be applied to 
    :param custom_operation_func_signature: the signature of your custom function that shall be applied to a dataset'''
    name: str
    description: Optional[str]
    dataset_label: str
    custom_operation_func_signature: str
