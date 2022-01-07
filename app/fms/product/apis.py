from logging import log
import logging
import re
from flask_restful import Api, request
from sqlalchemy.sql.sqltypes import REAL
from app.models.step import Step
from utils.apimodel import ApiBase, BaseApiPagination
from app.models.product import Product
from utils.common import create_response_message
from utils.dbmodel import DbBaseModel
from app import db

class ProductApi(BaseApiPagination):
    """
    URL: /product
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Product, "/product")

class DeleteProductApi(ApiBase):
    def delete(self):
        data = request.get_json(force = True)
        steps = Step.query.all()
        for step in steps:
            for index in step.products:
                if index.id == data['id']:
                    while len(step.products):
                        step.products.pop(0)
                        db.session.add(step)
                        db.session.commit
        productId = Product.query.get(data['id'])
        db.session.delete(productId)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)