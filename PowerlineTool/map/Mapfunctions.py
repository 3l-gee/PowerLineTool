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

def dataConvert(feature, type) :
    features = []

    if type == "TLM" : 
        for i in range(len(feature["points"])) : 
            attributes = {
                "feature" : feature["tlmID"],
                "description": feature["points"][i]["description"],
                "terrain" : feature["points"][i]["terrain"]["magnitude"],
                "structureHeight" : feature["points"][i]["structureHeight"]["magnitude"]
            }
            point_geojson = geojson.Feature(geometry=geojson.Point((feature["points"][i]["location"]["x"], feature["points"][i]["location"]["y"])), properties=attributes)
            features.append(point_geojson)


        feature_collection = geojson.FeatureCollection(features)

        return feature_collection
             
    #    for point in feature["points"]:
    #         attributes = {
    #             "feature" : feature["tlmID"],
    #             "description": point["description"],
    #             "terrain" : point["terrain"]["magnitude"],
    #             "structureHeigh" : point["structureHeigh"]["magnitude"]
    #                       }
    #         point_geojson = geojson.Feature(geometry=geojson.Point((point["location"]["x"], point["location"]["y"])), properties=attributes)
    #         features.append(point_geojson)
        
    #     for line in feature["lines"]:
    #         attributes = {"attribute_name": line["attribute_value"]}
    #         line_geojson = geojson.Feature(geometry=geojson.LineString([(point["longitude"], point["latitude"]) for point in line]), properties=attributes)
    #         features.append(line_geojson)


    
    elif type == "DCS" : 
        return 

class StageOne: 
    def __init__(self, ) : 
        self.features = {}
        self.TLMFeatures = {}
        tempList = json.load(open('map/static/map/data/TLMFullFeatures.json'))["obstacles"]
        for item in tempList :
            self.TLMFeatures[item["tlmID"]] = item

    def addFeatureTLM(self, featureId) :
        rawFeature = self.TLMFeatures[featureId]
        coordinates = dataConvert(rawFeature, "TLM")
        self.features[featureId] = {
            "type"  : "TLM",
            "id"    : featureId, 
            "raw"   : rawFeature,
            "coordinates" : coordinates
        }

    def addFeatureDCS(self, featureId, data) :


        self.features[featureId] = {
            "type"  : "DCS",
            "id"    : featureId, 
            "raw"   : data,
            "coordinates" : [[2600000,1200000],[2600100,1200100]]
        }

    def remFeature(self) :
        self.features = {}


