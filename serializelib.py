import time
import datetime

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.time)):
        serial = obj.isoformat()
        return serial

    if hasattr(obj, 'default'):
        return obj.default()

    return obj.__dict__
