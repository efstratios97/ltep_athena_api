import pandas as pd

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DataSet:
    name: str
    description: str
    label: Optional[str] = "NO_LABEL"
    access_user_list: Optional[list] = ""
    access_business_unit_list:  Optional[list] = ""
    cleaned: Optional[Any] = 0
    owner: Optional[str] = None
    size: Optional[int] = None
    hash_of_dataset: Optional[str] = None
    data: Optional[pd.DataFrame] = None
    creation_date: Optional[Any] = None
    dataset_id: Optional[str] = None
