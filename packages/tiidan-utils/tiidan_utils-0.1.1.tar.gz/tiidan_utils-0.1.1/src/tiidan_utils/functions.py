def nullify(f):
    def inner(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            return None

    return inner
