def get_entities(self, type=None):
	if type:
		entities = self._db.entities.find({'type': type})
	else:
		entities = self._db.entities.find()

	return entities

model_functions = [get_entities]