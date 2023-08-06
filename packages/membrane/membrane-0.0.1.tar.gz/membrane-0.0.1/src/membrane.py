""""""


""""""


from flask import request
from collections.abc import Mapping


UnknownType = object()


class RequiredFieldError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotAnOptionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TypeConversionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Request(object):
    """"""

    def __init__(self, *args, **kwargs):
        """"""

        self.args = dict(request.args)
        self.args.update(kwargs)

        self.body = request.get_json()
        if self.body is None:
            self.body = {}

        self.form = request.form

        super().__init__()

    def get(
        self,
        name,
        default=UnknownType,
        location=None,
        required=False,
        options=None,
    ):
        """"""

        value = UnknownType

        if location == "args" or location is None:
            value = self.args.get(name, default)

        if location == "body" or (location is None and value is UnknownType):
            value = self.body.get(name, default)

        if location == "form" or (location is None and value is UnknownType):
            value = self.form.get(name, default)

        return value


def parse_field(name, handler, req):
    """This function will search for `name` in req and try to parse it using
    `value`. If it is not found, and no default is provided, it will return an
    UnknownType back to `parse_mapping` to be filtered out."""

    if isinstance(handler, Mapping):

        value = req.get(
            name,
            **{
                k: v
                for (k, v) in handler.items()
                if k in ("default", "location", "required", "options")
            },
        )

        if "type" in handler and value is not UnknownType:
            try:
                value = handler["type"](value)
            except Exception as e:
                raise TypeConversionError(
                    f"Attempted to convert value `{value}` - it didn't work using `{str(handler['type'])}`. {str(e)}"
                )

        if (
            "required" in handler
            and handler["required"]
            and value is UnknownType
        ):
            raise RequiredFieldError(f"A required field ({name}) wasn't found.")
        elif "options" in handler and value not in list(handler["options"]) + [
            UnknownType
        ]:
            raise NotAnOptionError(
                f"A value you provided, '{value}', is not an option for '{name}' in {str(handler['options'])}."
            )

        return value

    elif callable(handler):

        value = req.get(name)
        if value is UnknownType:
            return value

        try:
            value = handler(value)
        except Exception as e:
            raise TypeConversionError(
                f"Attempted to convert value `{value}` - it didn't work using `{str(handler)}`. {str(e)}"
            )

        return value


def parse_mapping(mapping, req):
    """"""

    return {
        key: value
        for (key, value) in {
            value["as"]
            if isinstance(value, Mapping) and "as" in value
            else key: parse_field(key, value, req)
            for (key, value) in mapping.items()
        }.items()
        if value is not UnknownType
    }


def parser(*mappings):
    """"""

    def inner(func):
        def request_handler(_=None, *args, **kwargs):
            req = Request(*args, **kwargs)
            args = [parse_mapping(mapping, req) for mapping in mappings]
            if _ is not None:
                args = [_] + args
            return func(*args)

        # for Flask, we need a unique name for routing purposes
        request_handler.__name__ = func.__name__

        return request_handler

    return inner
