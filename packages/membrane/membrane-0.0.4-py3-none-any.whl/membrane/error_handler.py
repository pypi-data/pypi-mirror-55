""""""


from .membrane import RequiredFieldError, NotAnOptionError, TypeConversionError


def error_handler(app, errors=[], message_key="error", default_status=400):
    """"""

    # TODO maybe I should allow users to override all these?
    for e in (
        [RequiredFieldError, NotAnOptionError, TypeConversionError]
        + errors
        + [Exception]
    ):

        @app.errorhandler(e)
        def error(e):
            status_code = default_status
            res = {message_key: str(e)}
            if hasattr(e, "status_code"):
                status_code = e.status_code
            if hasattr(e, "payload"):
                res.update(e.payload)
            return res, status_code
