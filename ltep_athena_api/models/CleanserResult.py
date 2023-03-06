from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class CleanserResult:
    '''This Object helps you send the data in the right format for the LTEP Athena API. 
    Just pass the newly cleaned data in `cleaned_dataset` 
    and optionally the data you cleaned from the original dataset in `cleansed_dataset`'''
    cleaned_dataset: pd.DataFrame
    cleansed_dataset: Optional[pd.DataFrame]

    def __post_init__(self):
        self.formatted_results = {'cleaned_dataset': self.cleaned_dataset.to_json(
        ), 'cleansed_dataset': self.cleansed_dataset.to_json()}

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, CleanserResult) else hash(self.cleaned_dataset.to_string() + self.cleansed_dataset.to_string()) == hash(
            __o.cleaned_dataset.to_string() + __o.cleansed_dataset.to_string())
