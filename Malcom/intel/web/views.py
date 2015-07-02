from flask import Blueprint, render_template, abort, g, url_for
from jinja2 import TemplateNotFound

from Malcom.web.webserver import app
from Malcom.intel.web.api import intel_api


PREFIX = '/intel'

malcom_intel = Blueprint('malcom_intel', __name__, template_folder='templates', static_folder='static')
app.register_blueprint(intel_api, url_prefix='/intel/api')

@malcom_intel.route('/')
def index():
	print_routing()
	entities = g.Model.find({'type': {'$in': ['incident', 'indicator', 'ttp', 'malware', 'campaign', 'actor']}})
	return render_template("index.html", entities=entities)

@malcom_intel.route('/table/<type>')
def entity_table(type):
	# type = request.args.get('type')
	entities = g.Model.find({'type': type})
	if entities.count() > 0:
		return render_template("entity_table.html", entities=entities)
	else:
		return "No entities of type {} to show".format(type)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def print_routing():
	for rule in app.url_map.iter_rules():
		print "Method", rule.methods
		if has_no_empty_params(rule):
			print "URL", url_for(rule.endpoint)
		print "endpoint", rule.endpoint