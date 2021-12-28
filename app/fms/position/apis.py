from utils.apimodel import BaseApiPagination
from app.models.position import Position
from utils.common import create_response_message

class PositionApi(BaseApiPagination):
    """
    URL: /position
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Position, "/position")

    # def post(self):
    #     args = self.ModelType.get_all_attr()
    #     # required_args = ["id"]
    #     required_args = []
    #     parser = self.json_parser(args, required_args)
    #     if parser["validate"]:
    #         data = parser["data"]
    #     self.ModelType.add_new_from_dict(data):
    #         return create_response_message("Thêm mới thành công", 200)
    #     return parser["message"]


    