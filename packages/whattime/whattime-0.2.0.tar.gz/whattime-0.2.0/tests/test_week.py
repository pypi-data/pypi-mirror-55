from whattime import TimeType, week_info


def test_time_type_state_is_weekday(week):
    """Test week_info is_weekday of given datetime"""

    assert week_info(week.monday).is_weekday is True
    assert week_info(week.tuesday).is_weekday is True
    assert week_info(week.wednesday).is_weekday is True
    assert week_info(week.thursday).is_weekday is True
    assert week_info(week.friday).is_weekday is True
    assert week_info(week.saturday).is_weekday is False
    assert week_info(week.sunday).is_weekday is False


def test_time_type_state_is_weekend(week):
    """Test week_info is_weekday of given datetime"""

    assert week_info(week.monday).is_weekend is False
    assert week_info(week.tuesday).is_weekend is False
    assert week_info(week.wednesday).is_weekend is False
    assert week_info(week.thursday).is_weekend is False
    assert week_info(week.friday).is_weekend is False
    assert week_info(week.saturday).is_weekend is True
    assert week_info(week.sunday).is_weekend is True


def test_time_type_state_certain_day(week):
    """Test week_info days of given datetime"""

    for day in week._asdict().values():
        assert week_info(day).is_monday is (day is week.monday)
        assert week_info(day).is_tuesday is (day is week.tuesday)
        assert week_info(day).is_wednesday is (day is week.wednesday)
        assert week_info(day).is_thursday is (day is week.thursday)
        assert week_info(day).is_friday is (day is week.friday)
        assert week_info(day).is_saturday is (day is week.saturday)
        assert week_info(day).is_sunday is (day is week.sunday)


def test_time_type_state_types(week):
    """Test fitting types for the given datetime"""

    assert week_info(week.monday).types == {TimeType.MONDAY, TimeType.WEEKDAY}
    assert week_info(week.tuesday).types == {TimeType.TUESDAY, TimeType.WEEKDAY}
    assert week_info(week.wednesday).types == {TimeType.WEDNESDAY, TimeType.WEEKDAY}
    assert week_info(week.thursday).types == {TimeType.THURSDAY, TimeType.WEEKDAY}
    assert week_info(week.friday).types == {TimeType.FRIDAY, TimeType.WEEKDAY}
    assert week_info(week.saturday).types == {TimeType.SATURDAY, TimeType.WEEKEND}
    assert week_info(week.sunday).types == {TimeType.SUNDAY, TimeType.WEEKEND}
