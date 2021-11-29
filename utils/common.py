import logging

def __as_dict(obj):
    """
        Convert SQLAlchemy class to dict
    """
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def object_as_dict(obj):
    """
        Convert SQLAlchemy class to object
    """
    if type(obj) is list:
        return [object_as_dict(_obj) for _obj in obj]
    return __as_dict(obj)

def create_response_message( message, code):
    return {'msg': message}, code