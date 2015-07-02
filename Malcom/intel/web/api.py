from flask_restful import Resource, reqparse, Api
from flask.ext.login import login_required
from flask import Blueprint, g

from Malcom.web.webserver import app
from Malcom.intel.model.entities import BaseEntity

intel_api = Blueprint('intel_api', __name__)

api = Api(intel_api)

class EntityList(Resource):
	"""Returns a list of specified entities"""
	decorators=[login_required]
	def get(self, type=None):
		return list(BaseEntity.find({'type': type}))

api.add_resource(EntityList, '/list', '/list/<string:type>', endpoint='list')
