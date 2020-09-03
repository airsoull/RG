from django.core.exceptions import ValidationError


def str_from_coinmarket_to_float(s: str) -> float:
    return float(s.replace('$', '').replace(',', ''))


def compare_keys(data: dict, valid_keys: list):
    if not sorted(list(data.keys())) == sorted(valid_keys):
        raise ValidationError('invalid keys')


def valid_if_is_float(data):
    try:
        float(data)
    except ValueError:
        raise ValueError('Error with data')
