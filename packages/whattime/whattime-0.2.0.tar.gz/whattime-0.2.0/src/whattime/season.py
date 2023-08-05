from datetime import datetime
from typing import Set, Dict, Tuple

from .base import LocationBasedInfoBase
from .type import Hemisphere, TimeType


class SeasonInfo(LocationBasedInfoBase):
    __northern_mapping__ = {
        (1, 2, 12): TimeType.WINTER,  # Jan, Feb, Dec
        (3, 4, 5): TimeType.SPRING,  # Mar, Apr, May
        (6, 7, 8): TimeType.SUMMER,  # Jun, Jul, Aug
        (9, 10, 11): TimeType.AUTUMN,  # Sep, Oct, Nov
    }

    __southern_mapping__ = {
        (1, 2, 12): TimeType.SUMMER,  # Jan, Feb, Dec
        (3, 4, 5): TimeType.AUTUMN,  # Mar, Apr, May
        (6, 7, 8): TimeType.WINTER,  # Jun, Jul, Aug
        (9, 10, 11): TimeType.SPRING,  # Sep, Oct, Nov
    }

    @property
    def __mapping__(self) -> Dict[Tuple, TimeType]:
        if self.hemisphere == Hemisphere.NORTHERN:
            return self.__northern_mapping__
        else:
            return self.__southern_mapping__

    @property
    def __inverse_mapping__(self) -> Dict[TimeType, Tuple]:
        return {v: k for k, v in self.__mapping__.items()}

    @property
    def types(self) -> Set[TimeType]:
        """Return a set of fitting time types for the given datetime"""

        if self._types:
            return self._types

        month = self.date.month

        for month_range, time_type in self.__mapping__.items():
            if month in month_range:
                self._types.add(time_type)

        return self._types

    @property
    def is_spring(self) -> bool:
        """Return whether the given date is in spring on the given hemisphere"""

        return self._is_in_season(TimeType.SPRING)

    @property
    def is_summer(self) -> bool:
        """Return whether the given date is in summer on the given hemisphere"""

        return self._is_in_season(TimeType.SUMMER)

    @property
    def is_autumn(self) -> bool:
        """Return whether the given date is in autumn on the given hemisphere"""

        return self._is_in_season(TimeType.AUTUMN)

    @property
    def is_winter(self) -> bool:
        """Return whether the given date is in winter on the given hemisphere"""

        return self._is_in_season(TimeType.WINTER)

    def _is_in_season(self, time_type: TimeType) -> bool:
        return self.date.month in self.__inverse_mapping__[time_type]


def season_info(date: datetime, hemisphere: Hemisphere) -> SeasonInfo:
    return SeasonInfo(date, hemisphere)
