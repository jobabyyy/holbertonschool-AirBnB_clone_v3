#!/usr/bin/python3
"""Init"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
<<<<<<< HEAD
# from api.v1.views.places import *
from api.v1.views.users import *
=======
from api.v1.views.places import *
# from api.v1.views.users import *
>>>>>>> 0833bd2192359bd3633971bb7cc115ae50c9400b
# from api.v1.views.places_reviews import *
