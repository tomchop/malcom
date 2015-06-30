from flask import Blueprint, render_template, abort, g
from jinja2 import TemplateNotFound

from Malcom.web.webserver import app
from Malcom.web.intel.api import malcom_intel_api


PREFIX = '/intel'

malcom_intel = Blueprint('malcom_intel', __name__, template_folder='templates')
app.register_blueprint(malcom_intel_api, url_prefix='/intel/api')

@malcom_intel.route('/')
def index():
	entities = g.Model.find({'type': {'$in': ['incident', 'indicator', 'ttp', 'malware', 'campaign', 'actor']}})
	return render_template("index.html", entities=entities)