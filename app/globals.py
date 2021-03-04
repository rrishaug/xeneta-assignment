from flask import current_app
from werkzeug.local import LocalProxy

def get_logger():
    return current_app.logger

logger = LocalProxy(get_logger)
