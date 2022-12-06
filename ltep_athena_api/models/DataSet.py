import pandas as pd

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DataSet:
    name: str
    description: str
    data: pd.DataFrame
    label: Optional[str] = None
    access_user_list: Optional[list] = ""
    access_business_unit_list:  Optional[list] = ""
    cleaned: Optional[Any] = 0
    owner: Optional[str] = None
