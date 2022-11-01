from dataclasses import dataclass


@dataclass
class AnalysisBlock:
    title: str
    dataset_label: str
    icon: str = 'default'

    def __eq__(self, __o: object) -> bool:
        return False if not isinstance(__o, AnalysisBlock) else hash(self.title + self.dataset_label) == hash(__o.title + __o.dataset_label)
