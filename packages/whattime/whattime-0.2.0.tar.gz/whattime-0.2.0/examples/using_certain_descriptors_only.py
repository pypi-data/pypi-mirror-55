from datetime import datetime

from whattime import week_info, day_time_info, season_info, Hemisphere

# Asking for week info only for a e.g. a monday afternoon:
now = datetime.now()
info = week_info(now)

print(info.types)
# {<TimeType.WEEKDAY: 'weekday'>, <TimeType.MONDAY: 'monday'>}

print(info.is_weekday)
# True

print(info.is_weekend)
# False

print(info.is_morning)
# AttributeError: 'WeekInfo' object has no attribute 'is_morning'


# Asking for day time info only:
info = day_time_info(now)

print(info.types)
# {<TimeType.AFTERNOON: 'afternoon'>}

print(info.is_afternoon)
# True

print(info.is_evening)
# False

print(info.is_weekend)
# AttributeError: 'DayTimeInfo' object has no attribute 'is_weekend'


# Asking for the season e.g. in summer on the southern hemisphere:
info = season_info(now, Hemisphere.SOUTHERN)

print(info.types)
# {<TimeType.SUMMER: 'summer'>}

print(info.is_spring)
# False

print(info.is_summer)
# True

print(info.is_autumn)
# False

print(info.is_winter)
# False

print(info.is_monday)
# AttributeError: 'SeasonInfo' object has no attribute 'is_monday'
