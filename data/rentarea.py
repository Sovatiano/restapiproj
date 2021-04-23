import datetime
import sqlalchemy
from data import db_session


class RentArea(db_session.SqlAlchemyBase):
    __tablename__ = 'RentArea'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sqmeters = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    update_date = sqlalchemy.Column(sqlalchemy.DateTime)