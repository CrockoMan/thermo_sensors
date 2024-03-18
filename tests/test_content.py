import pytest


def one_more(x):
    return x + 1


def test_correct():
    assert one_more(4) == 5


@pytest.mark.xfail(reason='Пусть пока падает, завтра починю.')
def test_char_params():
    assert one_more('A') == 5


@pytest.mark.skip(reason='Что-то не работает')
def test_fail():
    assert one_more(3) == 5
