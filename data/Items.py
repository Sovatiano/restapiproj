import datetime
import sqlalchemy
from data import db_session


class Items(db_session.SqlAlchemyBase):
    __tablename__ = 'Items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    add_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)