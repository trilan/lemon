from django.utils.safestring import mark_safe


def query_helper(query, *remove, **add):
    return get_query_string(query.copy(), remove, add)


def get_query_string(p, remove=None, add=None):
    if add is None:
        add = {}
    if remove is None:
        remove = []
    for r in remove:
        for k in p.keys():
            if k == r:
                del p[k]
    for k, v in add.items():
        if k in p and v is None:
            del p[k]
        elif v is not None:
            p[k] = v
    params = ['%s=%s' % (k, v) for k, v in p.items()]
    return mark_safe('?' + '&'.join(params).replace(' ', '%20'))


def string_to_dict(string):
    kwargs = {}
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '':
                continue
            kw, val = arg.split('=', 1)
            kwargs[kw] = val
    return kwargs


def string_to_list(string):
    args = []
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '':
                continue
            args.append(arg)
    return args
