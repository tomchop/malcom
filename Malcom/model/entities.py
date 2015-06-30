import datetime, os, sys
from Malcom.auxiliary.toolbox import debug_output
import Malcom.auxiliary.toolbox as toolbox

types = []

class BaseEntity(dict):
	"""docstring for BaseEntity"""

	def __init__(self):
		pass

	def to_dict(self):
		return self.__dict__

	def __getattr__(self, name):
		return self.get(name, None)

	def __setattr__(self, name, value):
		self[name] = value

	def __str__(self):
		return "[{} {} (tags: {})]".format(self.type, self.value, ",".join(self.tags))

	def upgrade_tags(self, tags):
		self['tags'].extend(tags)
		self['tags'] = list(set(self['tags']))

	# necessary for pickling
	def __getstate__(self): return self.__dict__
	def __setstate__(self, d): self.__dict__.update(d)


class Incident(BaseEntity):
	"""docstring for Incident"""
	def __init__(self, title=None):
		self.idref = None			# external reference ID
		self.timestamp = None
		self.title = title
		self.description = None		
		self.categories = None		# categories
		self.reporter = None		# source reporting the incident
		self.victim = None			# victims
		self.status = None			# status
		self.type = 'incident'


class Indicator(BaseEntity):
	"""docstring for Indicator"""
	# Indicator as in IOC. Indicators gather a group of technical observables
	def __init__(self, title=None):
		self.title = title
		self.description = None
		self._type = None			# Context in which the associated observable is observed --> http://stixproject.github.io/data-model/1.2/stixVocabs/IndicatorTypeVocab-1.1/
		self.description = None
		self.confidence = None	
		self.type = 'indicator'

# This is what we call Elements today		
# class Observable(BaseEntity):
# 	"""Placeholder for CyBOX Observable"""
# 	def __init__(self):
# 		pass

class TTP(BaseEntity):
	"""Placeholder for TTP"""
	def __init__(self, title=None):
		self.title = title			# Examples: Phishing, Spear-Phishing, Spamvertizing, Malware, C2 behavior, Encryption, callback, 
		self.description = None
		self.type = 'ttp'
		
class Malware(BaseEntity):			
	"""docstring for Malware"""
	# To be linked with TTPs
	def __init__(self, arg):
		self.name = None
		self._type = None
		self.type = 'malware'
		
class Campaign(BaseEntity):
	"""docstring for Campaign"""
	def __init__(self):
		self.title
		self.description
		self.names
		self.type = 'campaign'

class Actor(BaseEntity):
	"""docstring for Actor"""
	def __init__(self):
		self.name = None
		self.description = None
		self.type = 'actor'















