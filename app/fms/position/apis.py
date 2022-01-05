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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD


    
<<<<<<< HEAD
=======
    @ApiBase.exception_error
    def delete(self):
        """
        Xóa một điểm
        Khi xóa một điểm ->  Xóa step chứa điểm đó -> Xóa các bước của mission chứa step đó
        URL:'/point'
        METHOD: DELETE
        """
        data = request.get_json(force = True)
        position = Position.query.get(data['id'])
        assert position is not None, f"Point {data['id']} không tồn tại"
        steps = Step.query.filter(or_((Step.start_point == data['id']), (Step.end_point == data['id']))).all()

        for step in steps:
            if step.start_point == data['id']:
                step.start_point = None
                db.session.add(step)
            if step.end_point == data['id']:
                step.end_point = None
                db.session.add(step)
            db.session.commit()
        db.session.delete(position)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)

=======
>>>>>>> parent of 257be39 (update robot)
=======
>>>>>>> parent of 257be39 (update robot)
=======
>>>>>>> parent of 257be39 (update robot)


    
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
