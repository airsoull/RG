def str_from_coinmarket_to_float(s: str) -> float:
    return float(s.replace('$', '').replace(',', ''))
