from datetime import datetime
from typing import Set, Dict, Tuple

from .base import InfoBase
from .type import TimeType


class DayTimeInfo(InfoBase):

    @property
    def __mapping__(self) -> Dict[Tuple, TimeType]:
        return {
            (0, 1, 2, 3, 4, 23): TimeType.NIGHT,
            (5, 6, 7, 8, 9): TimeType.MORNING,
            (10, 11): TimeType.MIDMORNING,
            (12,): TimeType.NOON,
            (13, 14, 15, 16, 17): TimeType.AFTERNOON,
            (18, 19, 20, 21, 22): TimeType.EVENING
        }

    @property
    def __inverse_mapping__(self) -> Dict[TimeType, Tuple]:
        return {v: k for k, v in self.__mapping__.items()}

    @property
    def types(self) -> Set[TimeType]:
        """Return a set of fitting time types for the given datetime"""

        if self._types:
            return self._types

        hour = self.date.hour

        for hours_range, time_type in self.__mapping__.items():
            if hour in hours_range:
                self._types.add(time_type)

        return self._types

    @property
    def is_morning(self) -> bool:
        """Return whether the given datetime is in the morning"""

        return self._is_in_daytime(TimeType.MORNING)

    @property
    def is_midmorning(self) -> bool:
        """Return whether the given datetime is in the midmorning"""

        return self._is_in_daytime(TimeType.MIDMORNING)

    @property
    def is_noon(self) -> bool:
        """Return whether the given datetime is at noon"""

        return self._is_in_daytime(TimeType.NOON)

    @property
    def is_afternoon(self) -> bool:
        """Return whether the given datetime is in the afternoon"""

        return self._is_in_daytime(TimeType.AFTERNOON)

    @property
    def is_evening(self) -> bool:
        """Return whether the given datetime is in the evening"""

        return self._is_in_daytime(TimeType.EVENING)

    @property
    def is_night(self) -> bool:
        """Return whether the given datetime is in the night"""

        return self._is_in_daytime(TimeType.NIGHT)

    def _is_in_daytime(self, time_type: TimeType) -> bool:
        return self.date.hour in self.__inverse_mapping__[time_type]


def day_time_info(date: datetime) -> DayTimeInfo:
    return DayTimeInfo(date)
