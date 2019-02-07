import pytest

from releasify.utils import (boolify, increment_version)


@pytest.mark.parametrize("test_input,expected", [
    ('v0.0.0', 'v1.0.0'),
    ('v0.0.1', 'v1.0.0'),
    ('v0.1.1', 'v1.0.0'),
])
def test_increment_major_version(test_input, expected):
    assert increment_version(test_input, 'major') == expected


@pytest.mark.parametrize("test_input,expected", [
    ('v0.0.0', 'v0.1.0'),
    ('v0.0.1', 'v0.1.0'),
])
def test_increment_minor_version(test_input, expected):
    assert increment_version(test_input, 'minor') == expected


@pytest.mark.parametrize("initial_version,expected", [
    ('v0.0.0', 'v0.0.1'),
    ('v0.0.1', 'v0.0.2'),
    ('v0.1.1', 'v0.1.2'),
    ('v1.1.1', 'v1.1.2'),
])
def test_increment_patch_version(initial_version, expected):
    assert increment_version(initial_version, 'patch') == expected


@pytest.mark.parametrize("input,expected", [
    ('y', True),
    ('Y', True),
    ('yes', True),
    ('YES', True),
    ('Yes', True),
    ('true', True),
    ('True', True),
    (1, True),
    ('1', True),
    ('no', False),
    ('N', False),
    ('false', False),
])
def test_boolify(input, expected):
    assert boolify(input) == expected
