from typing import Optional
import datetime
import flask
from flask import Request

from itgc.infrastructure import request_dict


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')
        self.year = datetime.datetime.now().year
        self.error: Optional[str] = None
        self.message: Optional[str] = None

    def to_dict(self):
        return self.__dict__
