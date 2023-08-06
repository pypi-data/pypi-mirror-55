import pytest

from formulaic.parser.algos.tokenize import tokenize
from formulaic.errors import FormulaParsingError


TOKEN_TESTS = {
    '': [],
    'a': ['name:a'],
    'a+b': ['name:a', 'operator:+', 'name:b'],
    'a + b': ['name:a', 'operator:+', 'name:b'],
    'a * b': ['name:a', 'operator:*', 'name:b'],
    'a * (b + c:d)': ['name:a', 'operator:*', 'operator:(', 'name:b', 'operator:+', 'name:c', 'operator::', 'name:d', 'operator:)'],
    'a() + d(a=1, b=2, c  = 3)': ['python:a()', 'operator:+', 'python:d(a=1, b=2, c  = 3)'],
    '1.32 + "string" / b': ['value:1.32', 'operator:+', 'value:"string"', 'operator:/', 'name:b'],
    'a ++ b': ['name:a', 'operator:++', 'name:b'],
    'a +   + b': ['name:a', 'operator:++', 'name:b'],
    'a(b() + c())': ['python:a(b() + c())'],
    r"'\''": [r"value:'\''"]
}

TOKEN_ERRORS = {
    'a"hello"': [FormulaParsingError, "Unexpected character '\"' following token 'a'."],
}


@pytest.mark.parametrize("formula,tokens", TOKEN_TESTS.items())
def test_tokenize(formula, tokens):
    assert [
        f"{token.kind.value}:{token.token}"
        for token in tokenize(formula)
    ] == tokens


@pytest.mark.parametrize("formula,exception_info", TOKEN_ERRORS.items())
def test_tokenize_exceptions(formula, exception_info):
    with pytest.raises(exception_info[0], match=exception_info[1]):
        list(tokenize(formula))
