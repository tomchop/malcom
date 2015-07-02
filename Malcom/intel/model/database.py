import pymongo
from pymongo import MongoClient
from pymongo.son_manipulator import SONManipulator
from pymongo.read_preferences import ReadPreference
import pymongo.errors
# import Malcom.intel.model.entities as entities

_connection = MongoClient()
db = _connection['malcom']
