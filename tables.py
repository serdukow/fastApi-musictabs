import datetime
from enum import Enum

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'

    id = sa.Column(sa.Integer, primary_key=True)
    artist = sa.Column(sa.String)
    song = sa.Column(sa.String)
    kind = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    mime_type = sa.Column(sa.String)
    modification_time = sa.Column(sa.String)














