import json


def error(msg) -> dict:
    """Return an error message formatted in the way ifttt expects"""

    return json.dumps({'errors': [{'status': 'SKIP', 'message': msg}]})
