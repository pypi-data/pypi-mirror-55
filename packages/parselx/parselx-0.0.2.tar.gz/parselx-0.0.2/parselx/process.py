from .utils import parse_query, partial
from .x_instance import x


def _parsel_one(sel, query: str, **kwargs):
    """Use parsel to extract original values"""
    if not isinstance(query, str):
        raise TypeError(f"Query should be string: {query}")
    q = parse_query(query)
    lang = q["lang"]
    if lang == "xpath":
        val = getattr(getattr(sel, lang)(q["query"], **kwargs), q["meth"])()
    else:
        val = getattr(getattr(sel, lang)(q["query"]), q["meth"])()
    return val


def _process_by_funcs(val, funcs=None):
    """Process field with functions"""

    for func in funcs or []:
        if isinstance(func, str):
            li = func.split(":", 1)
            func_name = li[0]
            args = li[1].split(",") if len(li) == 2 else []
            func = partial(x.filters[func_name], *args, new_args_before=True)
        val = func(val)
    return val


def process(sel, queries, **kwargs):
    if isinstance(queries, dict):
        return {k: process(sel, v, **kwargs) for k, v in queries.items()}

    if isinstance(queries, list):
        query = queries[0]
        funcs = queries[1:]
        val = process(sel, query, **kwargs)
        return _process_by_funcs(val, funcs)
    else:
        query = queries
        return _parsel_one(sel, query, **kwargs)

