from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, Dict, Union, Tuple

from .type import TimeType, Hemisphere


class InfoBase(ABC):
    def __init__(self, date: datetime):
        self.date = date
        self._types = set()

    @abstractmethod
    def __mapping__(self) -> Dict[Union[str, Tuple], TimeType]:
        pass

    @abstractmethod
    def types(self) -> Set[TimeType]:
        pass


class LocationBasedInfoBase(InfoBase):
    def __init__(self, date: datetime, hemisphere: Hemisphere):
        self.hemisphere = hemisphere
        super().__init__(date)

    @abstractmethod
    def __inverse_mapping__(self) -> Dict[TimeType, Tuple]:
        pass

    @abstractmethod
    def types(self) -> Set[TimeType]:
        pass
