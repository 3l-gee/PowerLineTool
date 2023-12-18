from pyproj import Proj, transform
import json
import geojson

def transform_coordinates(src_epsg, dest_epsg, x, y):
    # Create Proj instances for source and destination coordinate systems
    src_proj = Proj(init=f"epsg:{src_epsg}", preserve_units=False)
    dest_proj = Proj(init=f"epsg:{dest_epsg}", preserve_units=False)

    # Transform coordinates from source to destination
    dest_x, dest_y = transform(src_proj, dest_proj, x, y)

    return dest_x, dest_y

def dataConvert(type, feature) :
    features = []
    if type == "TLM" : 
        for i in range(len(feature["points"])) : 
            attributes = {
                "feature" : feature["tlmID"],
                "description": feature["points"][i]["description"],
                "terrain" : feature["points"][i]["terrain"]["magnitude"],
                "structureHeight" : round(feature["points"][i]["structureHeight"]["magnitude"],3)
            }
            point_geojson = geojson.Feature(geometry=geojson.Point((feature["points"][i]["location"]["x"], feature["points"][i]["location"]["y"])), properties=attributes)
            features.append(point_geojson)

        for i in range(len(feature["lines"])) : 
            attributes = {
                "feature" : feature["tlmID"],
                "from": feature["points"][i]["description"],
                "to": feature["points"][i+1]["description"],
                "structureHeight" : round(feature["points"][i]["structureHeight"]["magnitude"],3)
            }
            line_geojson = geojson.Feature(geometry=geojson.LineString([
                (feature["points"][i]["location"]["x"], feature["points"][i]["location"]["y"]),
                (feature["points"][i+1]["location"]["x"], feature["points"][i+1]["location"]["y"])
                ]), properties=attributes)
            features.append(line_geojson)

        feature_collection = geojson.FeatureCollection(features)
        return feature_collection
                
    elif type == "DCS" : 
        for i in range(len(feature["points"])) : 
            attributes = {
                "feature" : "TODO",
                "description": "TODO",
                "terrain" : feature["points"][i]["elevation"]["magnitude"],
                "structureHeight" : round(feature["points"][i]["structureHeight"]["magnitude"],3)
            }
            point_geojson = geojson.Feature(geometry=geojson.Point((feature["points"][i]["location"]["x"], feature["points"][i]["location"]["y"])), properties=attributes)
            features.append(point_geojson)

        for i in range(len(feature["jths"])) : 
            attributes = {
                "feature" : "TEST",
                "from": "TODO",
                "to": "TODO",
                "structureHeight" : round(feature["points"][i]["structureHeight"]["magnitude"],3)
            }
            line_geojson = geojson.Feature(geometry=geojson.LineString([
                (feature["points"][i]["location"]["x"], feature["points"][i]["location"]["y"]),
                (feature["points"][i+1]["location"]["x"], feature["points"][i+1]["location"]["y"])
                ]), properties=attributes)
            features.append(line_geojson)
        
        feature_collection = geojson.FeatureCollection(features)
        return feature_collection

class StageOne: 
    def __init__(self, ) : 
        self.features = {}
        self.TLMFeatures = {}
        tempList = json.load(open('map/static/map/data/TLMFullFeatures.json'))["obstacles"]
        for item in tempList :
            self.TLMFeatures[item["tlmID"]] = item

    def addFeatureTLM(self, featureId) :
        rawFeature = self.TLMFeatures[featureId]
        coordinates = dataConvert("TLM", rawFeature)
        self.features[featureId] = {
            "type"  : "TLM",
            "id"    : featureId, 
            "raw"   : rawFeature,
            "coordinates" : coordinates
        }

    def addFeatureDCS(self, featureId, data) :
        coordinates = dataConvert("DCS", data)
        self.features[featureId] = {
            "type"  : "DCS",
            "id"    : featureId, 
            "raw"   : data,
            "coordinates" : coordinates
        }

    def remFeature(self, featureId) : 
        self.features.pop(featureId)

    def remFeatures(self) :
        self.features = {}


class StageTow: 
    def __init__(self, stageOneFeatures):
        self.features = stageOneFeatures
