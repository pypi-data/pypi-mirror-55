import pytest

import wils


@pytest.mark.parametrize(('input', 'output'), (
        (0, '0'),
        (1, '1 μs'),
        (999, '999 μs'),
        (1000, '1.000 ms'),
        (999999, '999.999 ms'),
        (1000000, '1.000 s'),
        (1000001, '1.000 s'),
        (1001000, '1.001 s'),
))
def test_display_microseconds(input, output):
    assert output == wils.display_microseconds(input)


@pytest.mark.parametrize(('input', '_type', 'output'), (
        ('0', str, ''),
        ('0', int, 0),
        ('"a"', str, 'a'),
        ('"a"', int, 0),
        ('{}', str, ''),
        ('{}', dict, {}),
))
def test_json_load(input, _type, output):
    assert output == wils.json_load(input, _type)


@pytest.mark.parametrize(('input', 'output'), (
        ('', ''),
        ('t', 't'),
        ('12345678901234567890', '12345678901234567890'),
        ('12345678901234567890...', '12345678901234567890...'),
))
def test_string_brief(input, output):
    assert output == wils.string_brief(input)


@pytest.mark.parametrize(('input', 'length', 'output'), (
        ('', 3, ''),
        ('t', 3, 't'),
        ('12345678901234567890', 3, '123...'),
        ('12345678901234567890...', 3, '123...'),
))
def test_string_brief_with_length(input, length, output):
    assert output == wils.string_brief(input, length)
