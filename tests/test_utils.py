from releaser.utils import increment_version

def test_increment_major_version():
    assert increment_version('v0.0.0', 'major') == 'v1.0.0'
    assert increment_version('v0.0.1', 'major') == 'v1.0.0'
    assert increment_version('v0.1.1', 'major') == 'v1.0.0'
