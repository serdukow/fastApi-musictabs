import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'

    id = sa.Column(sa.Integer, primary_key=True)
    file_id = sa.Column(sa.Integer)
    name = sa.Column(sa.String)
    tag = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    mime_type = sa.Column(sa.String)
    modification_time = sa.Column(sa.String)














