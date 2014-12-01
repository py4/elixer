import json, codecs, os

class DataHandler:
	def __init__(self, path):
		self.path = path

	@classmethod
	def get_path(self, x, y, z):
		return os.path.join("data", "+00"+str(x)+","+"+00"+str(y)+","+"+00"+str(z)+".json")

	def load_data(self,x,y,z):
		coordinates = []
		path = self.get_path(x,y,z)
		with open(path) as f:
			data = json.load(codecs.open(path, 'r', 'latin-1'))
			for feature in data["features"]:
				
				if("geometries" in list(feature["geometry"].keys())):
					for geometry in feature["geometry"]["geometries"]:
						coordinates.append({str(geometry["type"]): geometry["coordinates"]})
				else:
						coordinates.append({str(feature["geometry"]["type"]): feature["geometry"]["coordinates"]})
		return coordinates