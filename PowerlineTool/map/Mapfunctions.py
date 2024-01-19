from pyproj import Proj, transform
import json
import geojson
import uuid
import copy

from . import LineString



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
        #GeoJSon
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

        line_coordinates = [(feature["points"][0]["location"]["x"], feature["points"][0]["location"]["y"])]

        for i in range(len(feature["jths"])) : 
            attributes = {
                "feature" : "TEST",
                "from": "TODO",
                "to": "TODO",
                "structureHeight" : round(feature["points"][i]["structureHeight"]["magnitude"],3)
            }
            line_coordinates.append((feature["points"][i+1]["location"]["x"], feature["points"][i+1]["location"]["y"]))


        line_geojson = geojson.Feature(geometry=geojson.LineString(line_coordinates), properties=attributes)
            
        features.append(line_geojson)
        
        feature_collection = geojson.FeatureCollection(features)
        return feature_collection

class LineStringHandler: 
    def __init__(self) : 
        self.features = {}
        self.graphs = {}
        self.TLMFeatures = {}
        tempList = json.load(open('map/static/map/data/TLMFullFeatures.json'))["obstacles"]
        for item in tempList :
            self.TLMFeatures[item["tlmID"]] = item

    def addFeatureTLM(self, featureId) :
        rawFeature = self.TLMFeatures[featureId]
        graph = LineString.LineString()
        graph.TLM_reader(rawFeature)
        coordinates = dataConvert("TLM", rawFeature)
        self.graphs[featureId] = graph
        self.features[featureId] = {
            "type"  : "TLM",
            "id"    : featureId, 
            "raw"   : rawFeature,
            "coordinates" : graph.geoJson("TLM", featureId),
        }

    def addFeatureDCS(self, featureId, data) :
        graph = LineString.LineString()
        graph.DCS_reader(data)
        coordinates = dataConvert("DCS", data)
        self.graphs[featureId] = graph
        self.features[featureId] = {
            "type"  : "DCS",
            "id"    : featureId, 
            "raw"   : data,
            "coordinates" : graph.geoJson("DCS",featureId),
        }


    def remFeature(self, featureId) : 
        self.features.pop(featureId)

    def remFeatures(self) :
        self.features = {}

    def divide_graph(self, featureId, start_node):
        feature = self.features[featureId]

        self.features["test_Divide_A"] = {
            "type"  : feature["type"],
            "id"    : "test_Divide_A", 
            "raw"   : feature["raw"],
            "coordinates" : feature["coordinates"]
        }

        self.features["test_Divide_B"] = {
            "type"  : feature["type"],
            "id"    : "test_Divide_B", 
            "raw"   : feature["raw"],
            "coordinates" : feature["coordinates"]
        }

        # visited = set()

        # def dfs(node):
        #     visited.add(node)
        #     for neighbor in graph.neighbors(node):
        #         if neighbor not in visited:
        #             dfs(neighbor)

        # dfs(start_node)

        # # Create subgraphs based on visited and unvisited nodes
        # left_side_nodes = visited
        # right_side_nodes = set(graph.nodes) - visited

        # left_side_subgraph = graph.subgraph(left_side_nodes)
        # right_side_subgraph = graph.subgraph(right_side_nodes)

        # return left_side_subgraph, right_side_subgraph





# class StageTwo: 
#     def __init__(self, features):
#         self.lineString = LineString.LineString()
#         for feature in features : 
#             self.lineString = []



        
#     def compose(self, graph1, pts1_id, graph2, pts2_id):
#         return
        # # Extract nodes from both graphs
        # pts1 = graph1[pts1_id]
        # pts2 = graph2[pts2_id]
        
        # # Create a new node with some attributes
        # new_id = "test"
        # new_attributes = {
        #     "x": 25,
        #     "y": 25,
        #     "structureHeight": 25,
        #     "elevation": 25,
        #     "currentLighting": "no"
        # }
        
        # # Add the new node to both graphs
        # graph1.add_node(new_id, **new_attributes)
        # graph2.add_node(new_id, **new_attributes)
        
        # # Create a composed graph using nx.compose
        # composed = nx.compose(graph1, graph2)
        
        # # Reroute edges that used to go to pts1 and pts2 to the new_id
        # for neighbor in list(graph1.neighbors(pts1_id)):
        #     composed.add_edge(neighbor, new_id, **graph1.get_edge_data(pts1_id, neighbor))
        # for neighbor in list(graph2.neighbors(pts2_id)):
        #     composed.add_edge(neighbor, new_id, **graph2.get_edge_data(pts2_id, neighbor))
            
        # # Remove old pts1 and pts2 nodes
        # composed.remove_node(pts1_id)
        # composed.remove_node(pts2_id)
        
        # return composed
