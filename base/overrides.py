def overrides(parent_class):

    def overrides_impl(method):
        assert (method.__name__ in dir(parent_class))
        method.__doc__ = getattr(parent_class, method.__name__).__doc__
        return method

    return overrides_impl
