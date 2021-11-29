from .apis import UpdateApi, VersionApi
from app import api

api.add_resource(UpdateApi, '/updatesoftware')  #GET update lasted version software
api.add_resource(VersionApi, '/version')        #GET software version
