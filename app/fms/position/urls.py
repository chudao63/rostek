from app import api
from .apis import *
from .fe_configure import PositionConfigureApi

api.add_resource(
    PositionApi,
    '/position',
    '/position/edit'
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
api.add_resource(
    PointApi,
    '/point'
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
)
=======

>>>>>>> parent of 257be39 (update robot)
=======
>>>>>>> parent of 257be39 (update robot)
=======
>>>>>>> parent of 257be39 (update robot)
=======
>>>>>>> parent of 257be39... update robot


api.add_resource(
    PositionConfigureApi, 
    '/position/filter',      # replace location to module name
    '/position/post',        # replace location to module name
    '/position/patch',       # replace location to module name
    '/position/delete'       # replace location to module name
)
