def parse_query(query: str):
    """Parse the query to a dictionary"""

    query = query.strip()
    if query.startswith("[") and query.endswith("]"):
        query = query[1:-1].strip()
        meth = "getall"
    else:
        meth = "get"

    lang = "css"
    if query.startswith("_"):
        query = query[1:].strip()
        lang = "xpath"

    q = {"query": query, "meth": meth, "lang": lang}
    return q


def partial(func, *args, new_args_before=False, **keywords):
    def newfunc(*fargs, **fkeywords):
        if new_args_before:
            newkeywords = {**fkeywords, **keywords}
            newargs = [*fargs, *args]
        else:
            newkeywords = {**keywords, **fkeywords}
            newargs = [*args, *fargs]
        return func(*newargs, **newkeywords)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

