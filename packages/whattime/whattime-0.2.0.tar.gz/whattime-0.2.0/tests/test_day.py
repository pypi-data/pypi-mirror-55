from whattime import TimeType, day_time_info


def test_time_type_state_is_morning(day):
    """Test day_time_info is_morning returns True for morning hours"""

    assert day_time_info(day.hours_0).is_morning is False
    assert day_time_info(day.hours_1).is_morning is False
    assert day_time_info(day.hours_2).is_morning is False
    assert day_time_info(day.hours_3).is_morning is False
    assert day_time_info(day.hours_4).is_morning is False
    assert day_time_info(day.hours_5).is_morning is True
    assert day_time_info(day.hours_6).is_morning is True
    assert day_time_info(day.hours_7).is_morning is True
    assert day_time_info(day.hours_8).is_morning is True
    assert day_time_info(day.hours_9).is_morning is True
    assert day_time_info(day.hours_10).is_morning is False
    assert day_time_info(day.hours_11).is_morning is False
    assert day_time_info(day.hours_12).is_morning is False
    assert day_time_info(day.hours_13).is_morning is False
    assert day_time_info(day.hours_14).is_morning is False
    assert day_time_info(day.hours_15).is_morning is False
    assert day_time_info(day.hours_16).is_morning is False
    assert day_time_info(day.hours_17).is_morning is False
    assert day_time_info(day.hours_18).is_morning is False
    assert day_time_info(day.hours_19).is_morning is False
    assert day_time_info(day.hours_20).is_morning is False
    assert day_time_info(day.hours_21).is_morning is False
    assert day_time_info(day.hours_22).is_morning is False
    assert day_time_info(day.hours_23).is_morning is False


def test_time_type_state_is_midmorning(day):
    """Test day_time_info is_midmorning returns True for midmorning hours"""

    assert day_time_info(day.hours_0).is_midmorning is False
    assert day_time_info(day.hours_1).is_midmorning is False
    assert day_time_info(day.hours_2).is_midmorning is False
    assert day_time_info(day.hours_3).is_midmorning is False
    assert day_time_info(day.hours_4).is_midmorning is False
    assert day_time_info(day.hours_5).is_midmorning is False
    assert day_time_info(day.hours_6).is_midmorning is False
    assert day_time_info(day.hours_7).is_midmorning is False
    assert day_time_info(day.hours_8).is_midmorning is False
    assert day_time_info(day.hours_9).is_midmorning is False
    assert day_time_info(day.hours_10).is_midmorning is True
    assert day_time_info(day.hours_11).is_midmorning is True
    assert day_time_info(day.hours_12).is_midmorning is False
    assert day_time_info(day.hours_13).is_midmorning is False
    assert day_time_info(day.hours_14).is_midmorning is False
    assert day_time_info(day.hours_15).is_midmorning is False
    assert day_time_info(day.hours_16).is_midmorning is False
    assert day_time_info(day.hours_17).is_midmorning is False
    assert day_time_info(day.hours_18).is_midmorning is False
    assert day_time_info(day.hours_19).is_midmorning is False
    assert day_time_info(day.hours_20).is_midmorning is False
    assert day_time_info(day.hours_21).is_midmorning is False
    assert day_time_info(day.hours_22).is_midmorning is False
    assert day_time_info(day.hours_23).is_midmorning is False


def test_time_type_state_is_noon(day):
    """Test day_time_info is_noon returns True for the midday hour"""

    assert day_time_info(day.hours_0).is_noon is False
    assert day_time_info(day.hours_1).is_noon is False
    assert day_time_info(day.hours_2).is_noon is False
    assert day_time_info(day.hours_3).is_noon is False
    assert day_time_info(day.hours_4).is_noon is False
    assert day_time_info(day.hours_5).is_noon is False
    assert day_time_info(day.hours_6).is_noon is False
    assert day_time_info(day.hours_7).is_noon is False
    assert day_time_info(day.hours_8).is_noon is False
    assert day_time_info(day.hours_9).is_noon is False
    assert day_time_info(day.hours_10).is_noon is False
    assert day_time_info(day.hours_11).is_noon is False
    assert day_time_info(day.hours_12).is_noon is True
    assert day_time_info(day.hours_13).is_noon is False
    assert day_time_info(day.hours_14).is_noon is False
    assert day_time_info(day.hours_15).is_noon is False
    assert day_time_info(day.hours_16).is_noon is False
    assert day_time_info(day.hours_17).is_noon is False
    assert day_time_info(day.hours_18).is_noon is False
    assert day_time_info(day.hours_19).is_noon is False
    assert day_time_info(day.hours_20).is_noon is False
    assert day_time_info(day.hours_21).is_noon is False
    assert day_time_info(day.hours_22).is_noon is False
    assert day_time_info(day.hours_23).is_noon is False


def test_time_type_state_is_afternoon(day):
    """Test day_time_info is_afternoon returns True for afternoon hours"""

    assert day_time_info(day.hours_0).is_afternoon is False
    assert day_time_info(day.hours_1).is_afternoon is False
    assert day_time_info(day.hours_2).is_afternoon is False
    assert day_time_info(day.hours_3).is_afternoon is False
    assert day_time_info(day.hours_4).is_afternoon is False
    assert day_time_info(day.hours_5).is_afternoon is False
    assert day_time_info(day.hours_6).is_afternoon is False
    assert day_time_info(day.hours_7).is_afternoon is False
    assert day_time_info(day.hours_8).is_afternoon is False
    assert day_time_info(day.hours_9).is_afternoon is False
    assert day_time_info(day.hours_10).is_afternoon is False
    assert day_time_info(day.hours_11).is_afternoon is False
    assert day_time_info(day.hours_12).is_afternoon is False
    assert day_time_info(day.hours_13).is_afternoon is True
    assert day_time_info(day.hours_14).is_afternoon is True
    assert day_time_info(day.hours_15).is_afternoon is True
    assert day_time_info(day.hours_16).is_afternoon is True
    assert day_time_info(day.hours_17).is_afternoon is True
    assert day_time_info(day.hours_18).is_afternoon is False
    assert day_time_info(day.hours_19).is_afternoon is False
    assert day_time_info(day.hours_20).is_afternoon is False
    assert day_time_info(day.hours_21).is_afternoon is False
    assert day_time_info(day.hours_22).is_afternoon is False
    assert day_time_info(day.hours_23).is_afternoon is False


def test_time_type_state_is_evening(day):
    """Test day_time_info is_evening returns True for evening hours"""

    assert day_time_info(day.hours_0).is_evening is False
    assert day_time_info(day.hours_1).is_evening is False
    assert day_time_info(day.hours_2).is_evening is False
    assert day_time_info(day.hours_3).is_evening is False
    assert day_time_info(day.hours_4).is_evening is False
    assert day_time_info(day.hours_5).is_evening is False
    assert day_time_info(day.hours_6).is_evening is False
    assert day_time_info(day.hours_7).is_evening is False
    assert day_time_info(day.hours_8).is_evening is False
    assert day_time_info(day.hours_9).is_evening is False
    assert day_time_info(day.hours_10).is_evening is False
    assert day_time_info(day.hours_11).is_evening is False
    assert day_time_info(day.hours_12).is_evening is False
    assert day_time_info(day.hours_13).is_evening is False
    assert day_time_info(day.hours_14).is_evening is False
    assert day_time_info(day.hours_15).is_evening is False
    assert day_time_info(day.hours_16).is_evening is False
    assert day_time_info(day.hours_17).is_evening is False
    assert day_time_info(day.hours_18).is_evening is True
    assert day_time_info(day.hours_19).is_evening is True
    assert day_time_info(day.hours_20).is_evening is True
    assert day_time_info(day.hours_21).is_evening is True
    assert day_time_info(day.hours_22).is_evening is True
    assert day_time_info(day.hours_23).is_evening is False


def test_time_type_state_is_night(day):
    """Test day_time_info is_night returns True for night hours"""

    assert day_time_info(day.hours_0).is_night is True
    assert day_time_info(day.hours_1).is_night is True
    assert day_time_info(day.hours_2).is_night is True
    assert day_time_info(day.hours_3).is_night is True
    assert day_time_info(day.hours_4).is_night is True
    assert day_time_info(day.hours_5).is_night is False
    assert day_time_info(day.hours_6).is_night is False
    assert day_time_info(day.hours_7).is_night is False
    assert day_time_info(day.hours_8).is_night is False
    assert day_time_info(day.hours_9).is_night is False
    assert day_time_info(day.hours_10).is_night is False
    assert day_time_info(day.hours_11).is_night is False
    assert day_time_info(day.hours_12).is_night is False
    assert day_time_info(day.hours_13).is_night is False
    assert day_time_info(day.hours_14).is_night is False
    assert day_time_info(day.hours_15).is_night is False
    assert day_time_info(day.hours_16).is_night is False
    assert day_time_info(day.hours_17).is_night is False
    assert day_time_info(day.hours_18).is_night is False
    assert day_time_info(day.hours_19).is_night is False
    assert day_time_info(day.hours_20).is_night is False
    assert day_time_info(day.hours_21).is_night is False
    assert day_time_info(day.hours_22).is_night is False
    assert day_time_info(day.hours_23).is_night is True


def test_time_type_state_types(day):
    """Test fitting types for the given datetime"""

    assert day_time_info(day.hours_0).types == {TimeType.NIGHT}
    assert day_time_info(day.hours_1).types == {TimeType.NIGHT}
    assert day_time_info(day.hours_2).types == {TimeType.NIGHT}
    assert day_time_info(day.hours_3).types == {TimeType.NIGHT}
    assert day_time_info(day.hours_4).types == {TimeType.NIGHT}
    assert day_time_info(day.hours_5).types == {TimeType.MORNING}
    assert day_time_info(day.hours_6).types == {TimeType.MORNING}
    assert day_time_info(day.hours_7).types == {TimeType.MORNING}
    assert day_time_info(day.hours_8).types == {TimeType.MORNING}
    assert day_time_info(day.hours_9).types == {TimeType.MORNING}
    assert day_time_info(day.hours_10).types == {TimeType.MIDMORNING}
    assert day_time_info(day.hours_11).types == {TimeType.MIDMORNING}
    assert day_time_info(day.hours_12).types == {TimeType.NOON}
    assert day_time_info(day.hours_13).types == {TimeType.AFTERNOON}
    assert day_time_info(day.hours_14).types == {TimeType.AFTERNOON}
    assert day_time_info(day.hours_15).types == {TimeType.AFTERNOON}
    assert day_time_info(day.hours_16).types == {TimeType.AFTERNOON}
    assert day_time_info(day.hours_17).types == {TimeType.AFTERNOON}
    assert day_time_info(day.hours_18).types == {TimeType.EVENING}
    assert day_time_info(day.hours_19).types == {TimeType.EVENING}
    assert day_time_info(day.hours_20).types == {TimeType.EVENING}
    assert day_time_info(day.hours_21).types == {TimeType.EVENING}
    assert day_time_info(day.hours_22).types == {TimeType.EVENING}
    assert day_time_info(day.hours_23).types == {TimeType.NIGHT}
