from . import upload_blueprint

@upload_blueprint.app_errorhandler(404)
def page_not_found(e):
    return 'Page Not Found'

@upload_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return 'Internam Server Error'
