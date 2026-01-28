from app.dao.base import BaseDao
from app.user.model import User


class User_dao(BaseDao):
    model = User