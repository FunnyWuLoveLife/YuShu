from . import web


@web.app_errorhandler(BaseException)
def api_error(e):
    pass


@web.app_errorhandler(404)
def page_not_found(e):
    pass


@web.app_errorhandler(500)
def internal_server_error(e):
    pass


@web.before_request
def make_session_permanent():
    pass
