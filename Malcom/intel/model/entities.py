from pymongo.son_manipulator import SONManipulator

from Malcom.intel.model.database import db


class BaseEntity(dict):
    """docstring for BaseEntity"""

    display_fields = [('title', "Title", "str"), ('_type', "Type", "bound:entity_types")]
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

    def outgoing_links(self):
        if not self._id:
            raise ValueError("This {} has no _id set".format(self.__class__.__name__))

        dst_ids = [l['dst'] for l in db[BaseEntity.entity_graph].find({'src': self._id})]
        return db[BaseEntity.entity_collection].find({'_id': {'$in': dst_ids}})

    def incoming_links(self):
        if not self._id:
            raise ValueError("This {} has no _id set".format(self.__class__.__name__))

        src_ids = [l['src'] for l in db[BaseEntity.entity_graph].find({'dst': self._id})]
        return db[BaseEntity.entity_collection].find({'_id': {'$in': src_ids}})

    def all_links(self):
        if not self._id:
            raise ValueError("This {} has no _id set".format(self.__class__.__name__))

        dst_ids = [l['dst'] for l in db[BaseEntity.entity_graph].find({'src': self._id})]
        src_ids = [l['src'] for l in db[BaseEntity.entity_graph].find({'dst': self._id})]
        ids = list(set(dst_ids + src_ids))

        return db[BaseEntity.entity_collection].find({'_id': {'$in': ids}})

    def stix_related_elements(self):
        links = list(self.all_links())
        print links
        rels = {}
        for _type, label in self.stix_relationships:
            rels[(_type, label)] = [e for e in links if e['_type'] == _type]

        return rels


class Incident(BaseEntity):
    """docstring for Incident"""
    display_fields = BaseEntity.display_fields + [("idref", "ID ref", "int"),
                                                  ("timestamp", "Timestamp", "datetime"),
                                                  ("description", "Description", "str"),
                                                  ("categories", "Categories", "bound:incident_categories"),
                                                  ("reporter", "Reporter", "bound:reporter"),
                                                  ("victim", "Victim", "bound:victim"),
                                                  ("status", "Status", "bound:status")
                                                  ]

    stix_relationships = [('ttp', "Leveraged TTPs"),
                          ('indicator', "Related Indicators"),
                          ('observable', "Related Observables"),
                          ('actor', "Related Threat Actor"),
                          ('campaign', "Related campaign"),
                          ('malware', "Leveraged Malware"),
                          ('incident', "Related Incidents"),
                          ]

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

    display_fields = BaseEntity.display_fields + [("description", "Description", "datetime"),
                                                  ("type", "Indicator Type", "bound:indicator_types"),
                                                  ("confidence", "Reporter", "bound:reporter"),
                                                  ]

    stix_relationships = [('ttp', "Indicated TTPs"),
                          ('incident', "Used in Incidents"),
                          ('observable', "Related Observables"),
                          ('campaign', "Related campaign"),
                          ('malware', "Leveraged Malware"),
                          ('indicator', "Related Indicators"),
                          ]

    def __init__(self, title=None):
        self.title = title
        self.description = None
        self.type = None           # Context in which the associated observable is observed --> http://stixproject.github.io/data-model/1.2/stixVocabs/IndicatorTypeVocab-1.1/
        self.confidence = None
        self._type = "indicator"



# This is what we call "Elements" today
# class Observable(BaseEntity):
#   """Placeholder for CyBOX Observable"""
#   def __init__(self):
#       pass


class TTP(BaseEntity):
    """Placeholder for TTP"""

    display_fields = BaseEntity.display_fields + [("description", "Description", "datetime"),
                                                  ("type", "TTP Type", "bound:ttp_types"),
                                                  ]

    stix_relationships = [
                          ('incident', "Related Incidents"),
                          ('indicator', "Related Indicators"),
                          ('observable', "Related Observables"),
                          ('campaign', "Related Campaign"),
                          ('malware', "Characterizing Malware"),
                          ('actor', "Characterizing Threat Actors"),
                          ('ttp', "Related TTPs"),
                          ]

    def __init__(self, title=None):
        self.title = title          # Examples: Phishing, Spear-Phishing, Spamvertizing, Malware, C2 behavior, Encryption, callback,
        self.description = None
        self._type = 'ttp'


class Malware(BaseEntity):
    """docstring for Malware"""
    # To be linked with TTPs

    display_fields = BaseEntity.display_fields + [("family", "Family", "str"),
                                                  ("type", "Malware type", "bound:malware_types"),
                                                  ]

    stix_relationships = [('ttp', "Known TTPs"),
                          ('incident', "Seen in incidents"),
                          ('indicator', "Related Indicators"),
                          ('observable', "Related Observables"),
                          ('campaign', "Related Campaigns"),
                          ('actor', "Used by Actors"),
                          ('malware', "Related Malware")
                          ]


    def __init__(self, title=None):
        self.title = title
        self.family = title
        self.type = None
        self._type = 'malware'


class Campaign(BaseEntity):
    """docstring for Campaign"""

    display_fields = BaseEntity.display_fields + [("description", "Description", "str"),
                                                  ("timestamp", "Date", "datetime"),
                                                  ]

    stix_relationships = [('ttp', "Related TTPs"),
                          ('incident', "Related Incidents"),
                          ('indicator', "Related Indicators"),
                          ('actor', "Attribution"),
                          ('malware', "Related Malware"),
                          ('campaign', "Related Campaigns"),
                          ]

    def __init__(self):
        self.title
        self.description
        self.timestamp
        self._type = 'campaign'


class Actor(BaseEntity):
    """docstring for Actor"""

    display_fields = BaseEntity.display_fields + [("description", "Description", "str"),
                                                  ("aliases", "Aliases", "array:str")
                                                  ]

    stix_relationships = [('ttp', "Observed TTPs"),
                          ('incident', "Related Incidents"),
                          ('indicator', "Related Indicators"),
                          ('campaign', "Related Campaigns"),
                          ('malware', "Used Malware"),
                          ('actor', "Associated actors"),
                          ]


    def __init__(self):
        self.name = None
        self.description = None
        self.aliases = None
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


