import json
import os

class DataHandler:
	def __init__(self, path):
		self.path = path
	def load_data(self,x,y,z):
		coordinates = []
		with open(os.path.join("data","+00"+str(x)+","+"+00"+str(y)+","+"+00"+str(z)+".json")) as f:
			data = json.load(f)
			for feature in data["features"]:
				for geometry in feature["geometry"]["geometries"]:
					coordinates.append({str(geometry["type"]): geometry["coordinates"]})
		return coordinates