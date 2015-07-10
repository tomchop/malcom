from flask import Blueprint, render_template, url_for, request
from bson.objectid import ObjectId

from Malcom.web.webserver import app
from Malcom.intel.web.api import intel_api
from Malcom.intel.model.entities import BaseEntity


PREFIX = '/intel'

malcom_intel = Blueprint('malcom_intel', __name__, template_folder='templates', static_folder='static')
app.register_blueprint(intel_api, url_prefix='/intel/api')



@malcom_intel.route('/')
def index():
    entities = BaseEntity.find()
    return render_template("index.html", entities=entities)

@malcom_intel.route('/report/<_id>')
def report(_id):
    e = BaseEntity.find_one({'_id': ObjectId(_id)})
    rels = e.stix_related_elements()
    return render_template("report.html", entity=e, rels=rels)

@malcom_intel.route('/table')
def entity_table():
    _filter = request.args.get('filter')
    if _filter == 'all':
        q = {}
    else:
        q = {'_type': _filter}

    entities = list(BaseEntity.find(q))

    if len(entities) > 0:
        return render_template("entity_table.html", entities=entities)
    else:
        return "No entities of type {} to show".format(_filter)


@malcom_intel.route("/debug")
def debug():
    return get_routing()

def get_routing():
    rtng = ""
    for rule in app.url_map.iter_rules():
        rtng += "\nMethod: {}\n".format(rule.methods)
        if has_no_empty_params(rule):
            rtng += "URL: {}\n".format(url_for(rule.endpoint))
        rtng += "endpoint: {}\n".format(rule.endpoint)
    return "<pre>{}</pre>".format(rtng)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
