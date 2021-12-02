from app.users.models import RevokedTokenUser
from app import jwt

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    # if jwt_payload['type'] == 'access':
    jti = jwt_payload['jti']
    token = RevokedTokenUser.query.filter(RevokedTokenUser.jti==jti).first()
    if token:
        return True
    return False
    # return database_handler.in_blocklist(jti)