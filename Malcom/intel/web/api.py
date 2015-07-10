import re

from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from flask_restful import Resource, reqparse, Api
from flask.helpers import make_response
from flask.ext.login import login_required
from flask import Blueprint, g, request

from Malcom.web.webserver import app
from Malcom.intel.model.entities import BaseEntity

intel_api = Blueprint('intel_api', __name__)

api = Api(intel_api)


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

api.representations['application/json'] = output_json

class List(Resource):
	"""Returns a list of specified entities"""
	decorators=[login_required]
	def get(self, type=None):
		data = list(BaseEntity.find({'_type': type}))
		print data
		return data

api.add_resource(List, '/list', '/list/<string:type>', endpoint='list')


class Update(Resource):
	decorators=[login_required]
	def get(self, _id):
		entity = BaseEntity.find_one({"_id": ObjectId(_id)})
		print entity, _id
		d = dict(request.args)
		for key in d:
			if len(d[key]) == 1:
				entity[key] = d[key][0]
			else:
				entity[key] = d[key]

		entity.save()

api.add_resource(Update, '/update/<string:_id>', endpoint='update')


class Associate(Resource):
	decorators=[login_required]
	def get(self, src, dst):
		src = BaseEntity.find_one({'_id':ObjectId(src)})
		dst = BaseEntity.find_one({'_id':ObjectId(dst)})
		if src and dst:
			src.link(dst)

	def post(self, src):
		pass



api.add_resource(Associate, '/associate/<string:src>', '/associate/<string:src>/<string:dst>', endpoint='associate')

class Search(Resource):
	decorators=[login_required]
	def get(self):
		query = request.args.get('query')
		query = re.compile(query or "")
		return list(BaseEntity.find({'title': query}))

api.add_resource(Search, '/search', endpoint='search')






