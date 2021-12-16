from app import api
from .apis import  *
from .fe_configure import UserFilterApi, UserColumnApi

api.add_resource(
    UserApi, 
    '/user',            #GET for all level, POST/PATCH/DELETE for only admin level
    '/user/all'
)

# api.add_resource(
#     UserManagerApi, 
#     '/usermanager',            #GET for all level, POST/PATCH/DELETE for only admin level
# )

api.add_resource(
    UserListApi, 
    '/user/list_id_tech',       #GET all list of tech id
    '/user/list_id_qc',         #GET all list of qc id
    '/user/list_id_manager'     #GET all list of manager id
)

api.add_resource(UserLogin, '/login')       #LOGOUT
api.add_resource(UserLogout, '/logout')     #LOGIN
api.add_resource(UserRoleApi, '/userrole', '/userrole/list_name')  #GET all user role
api.add_resource(UserProfile, '/profile')   #GET, POST to edit account
api.add_resource(UserRefreshToken, '/refresh_token')
api.add_resource(UserRevokeRefreshToken, '/revoke_refresh_token')


api.add_resource(
    UserFilterApi, 
    '/user/filter', # Get filter 
    '/user/post',   # Get atr post
    '/user/patch',   # Get atr patch
    '/user/delete'
)


api.add_resource(
    UserColumnApi, 
    '/user/column'
)
