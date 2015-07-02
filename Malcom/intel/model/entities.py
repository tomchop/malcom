import datetime, os, sys
from pymongo.son_manipulator import SONManipulator

from Malcom.auxiliary.toolbox import debug_output
import Malcom.auxiliary.toolbox as toolbox
from Malcom.intel.model.database import db


class BaseEntity(dict):
    """docstring for BaseEntity"""

    display_fields = [('title', "Title"), ('type', "Type")]
    entity_collection = 'entities'
    entity_graph = 'entity_graph'

    def to_dict(self):
        return {k: self[k] for k in self}

    @staticmethod    
    def from_dict(d, entity_type):
        f = entity_type()
        for key in d:
            f[key] = d[key]
        return f

    def __getattr__(self, name):
        return self.get(name, None)

    def __setattr__(self, name, value):
        self[name] = value

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.title)

    def upgrade_tags(self, tags):
        self['tags'].extend(tags)
        self['tags'] = list(set(self['tags']))

    # database methods

    @staticmethod
    def find(query={}):
        return db[BaseEntity.entity_collection].find(query)

    @staticmethod
    def find_one(query):
        return db[BaseEntity.entity_collection].find_one(query)

    def save(self):
        db[BaseEntity.entity_collection].save(self)

    def link(self, entity, attribs={}):
        link = {'src': self._id, 'dst': entity._id, 'attribs': attribs}
        db[BaseEntity.entity_graph].save(link)

    def dst_link(self):
        if not self._id:
            raise ValueError("This {} has no _id set".format(self.__class__.__name__))
        
        dst_ids = [l['dst'] for l in db['graph'].find({'src': self._id})]
        return db[BaseEntity.entity_collection].find({'_id': {'$in': dst_ids}})

    def src_link(self):
        if not self._id:
            raise ValueError("This {} has no _id set".format(self.__class__.__name__))
        
        src_ids = [l['src'] for l in db['graph'].find({'dst': self._id})]
        return db[BaseEntity.entity_collection].find({'_id': {'$in': src_ids}})

    def neighbors(self):
        if not self._id:
            raise ValueError("This {} has no _id set".format(self.__class__.__name__))

        dst_ids = [l['dst'] for l in db['graph'].find({'src': self._id})]
        src_ids = [l['src'] for l in db['graph'].find({'dst': self._id})]
        ids = list(set(dst_ids + src_ids))

        return db[BaseEntity.entity_collection].find({'_id': {'$in': ids}})



class Incident(BaseEntity):
    """docstring for Incident"""
    def __init__(self, title=None):
        self.idref = None           # external reference ID
        self.timestamp = None
        self.title = title
        self.description = None     
        self.categories = None      # categories
        self.reporter = None        # source reporting the incident
        self.victim = None          # victims
        self.status = None          # status
        self._type = 'incident'


class Indicator(BaseEntity):
    """docstring for Indicator"""
    # Indicator as in IOC. Indicators gather a group of technical observables
    def __init__(self, title=None):
        self.title = title
        self.description = None
        self.type = None           # Context in which the associated observable is observed --> http://stixproject.github.io/data-model/1.2/stixVocabs/IndicatorTypeVocab-1.1/
        self.description = None
        self.confidence = None  
        self._type = "indicator"

# This is what we call "Elements" today     
# class Observable(BaseEntity):
#   """Placeholder for CyBOX Observable"""
#   def __init__(self):
#       pass

class TTP(BaseEntity):
    """Placeholder for TTP"""
    def __init__(self, title=None):
        self.title = title          # Examples: Phishing, Spear-Phishing, Spamvertizing, Malware, C2 behavior, Encryption, callback, 
        self.description = None
        self._type = 'ttp'

        
class Malware(BaseEntity):          
    """docstring for Malware"""
    # To be linked with TTPs
    def __init__(self, title=None):
        self.title = title
        self.family = title
        self.type = None
        self._type = 'malware'

        
class Campaign(BaseEntity):
    """docstring for Campaign"""
    def __init__(self):
        self.title
        self.description
        self.names
        self._type = 'campaign'


class Actor(BaseEntity):
    """docstring for Actor"""
    def __init__(self):
        self.name = None
        self.description = None
        self._type = 'actor'


class EntityTransform(SONManipulator):
    
    DataTypes = {
        'incident': Incident,
        'indicator': Indicator,
        'ttp': TTP,
        'malware': Malware,
        'campaign': Campaign,
        'actor': Actor,
    }

    def transform_incoming(self, son, collection):
        for (key, value) in son.items():
            if isinstance(value, dict):
                son[key] = self.transform_incoming(value, collection)
        return son

    def transform_outgoing(self, son, collection):
        if '_type' in son:
            t = son['_type']
            return BaseEntity.from_dict(son, EntityTransform.DataTypes[t])
        else:
            return son

db.add_son_manipulator(EntityTransform())


