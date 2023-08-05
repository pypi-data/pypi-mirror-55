import inspect
from datetime import datetime
from typing import Set, Dict, Type, Union, Tuple

from .day import DayTimeInfo
from .season import SeasonInfo
from .type import TimeType, Hemisphere
from .week import WeekInfo


class TimeInfo(DayTimeInfo, WeekInfo, SeasonInfo):
    _mapping = {}

    @property
    def __mapping__(self) -> Dict[Union[str, Tuple], TimeType]:
        if not self._mapping:
            for cls in TimeInfo.__bases__:
                kwargs = self._base_kwargs(cls)
                self._mapping.update(cls(**kwargs).__mapping__)

        return self._mapping

    @property
    def types(self) -> Set[TimeType]:
        if not self._types:
            for cls in TimeInfo.__bases__:
                kwargs = self._base_kwargs(cls)
                self._types = self._types.union(cls(**kwargs).types)

        return self._types

    def _base_kwargs(self, cls: Type) -> Dict[str, Union[datetime, Hemisphere]]:
        args = inspect.getfullargspec(cls.__init__).args
        return {arg: self.__getattribute__(arg) for arg in args if arg != 'self'}


def whattime(date: datetime, hemisphere: Hemisphere) -> TimeInfo:
    return TimeInfo(date, hemisphere)


def week_info(date: datetime) -> WeekInfo:
    return WeekInfo(date)


def day_time_info(date: datetime) -> DayTimeInfo:
    return DayTimeInfo(date)


def season_info(date: datetime, hemisphere: Hemisphere) -> SeasonInfo:
    return SeasonInfo(date, hemisphere)
