from pyproj import Proj, transform
import networkx as nx
import json
import geojson
import uuid
import copy
from datetime import datetime
from . import lineString



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
        graph = lineString.LineString()
        graph.TLM_reader(rawFeature,featureId)
        self.graphs[featureId] = graph
        self.features[featureId] = {
            "type"  : "TLM",
            "id"    : featureId, 
            "raw"   : rawFeature,
            "coordinates" : graph.geoJson(),
        }

    def addFeatureDCS(self, featureId, data) :
        graph = lineString.LineString()
        graph.DCS_reader(data,featureId)
        self.graphs[featureId] = graph
        self.features[featureId] = {
            "type"  : "DCS",
            "id"    : featureId, 
            "raw"   : data,
            "coordinates" : graph.geoJson(),
        }


    def remFeature(self, featureId) : 
        self.features.pop(featureId)
        self.graphs.pop(featureId)

    def remFeatures(self) :
        self.features = {}
        self.graphs = {}

    def divide(self, point_source, point_id):
        feature = self.features[point_source]
        graph =self.graphs[point_source]

        left_graph,right_graph = graph.divide(point_id)
        self.graphs[left_graph["id"]] = left_graph["graph"]
        self.graphs[right_graph["id"]] = right_graph["graph"]

        self.features["left_graph"] = {
            "type"  : "divide",
            "id"    : left_graph["id"], 
            "raw"   : None,
            "coordinates" : self.graphs[left_graph["id"]].geoJson()
        }

        self.features["right_graph"] = {
            "type"  : "divide",
            "id"    : right_graph["id"], 
            "raw"   : None,
            "coordinates" : self.graphs[right_graph["id"]].geoJson()
        }
    
    def fuse(self, point1_source, point1_id, point2_source, point2_id):
        nx_graph1 = self.graphs[point1_source].graph
        nx_graph2 = self.graphs[point2_source].graph

        history = self.graphs[point1_source].history + self.graphs[point2_source].history

        timestamp = datetime.now().isoformat()
        history.append({'timestamp': timestamp,
                        'operation': 'fuse', 
                        'parameter': str(point1_source + " / " + point2_source)})
        
        node1 = nx_graph1.nodes[point1_id]
        node2 = nx_graph2.nodes[point2_id]

        new_id = str("fused-" + str(uuid.uuid4())[:6])
        new_attributes = {
            "x": node1['x'],
            "y": node1['y'],
            "structureHeight": node1['structureHeight'],
            "elevation": node1['elevation'],
            "currentLighting": "TEST"
        }

        nx_graph1.add_node(new_id, **new_attributes)
        nx_graph2.add_node(new_id, **new_attributes)

        # Create a composed graph using nx.compose
        composed = nx.compose(nx_graph1, nx_graph2)
        
        # Reroute edges that used to go to pts1 and pts2 to the new_id
        for neighbor in list(nx_graph1.neighbors(point1_id)):
            composed.add_edge(neighbor, new_id, **nx_graph1.get_edge_data(point1_id, neighbor))
        for neighbor in list(nx_graph2.neighbors(point2_id)):
            composed.add_edge(neighbor, new_id, **nx_graph2.get_edge_data(point2_id, neighbor))
            
        # Remove old pts1 and pts2 nodes
        composed.remove_node(point1_id)
        composed.remove_node(point2_id)

        self.remFeature(point1_source)
        self.remFeature(point2_source)

        self.graphs[new_id] = lineString.LineString(composed,new_id, history)
        self.features[new_id] = {
            "type"  : "fused",
            "id"    : new_id,
            "raw"   : [],
            "coordinates" : self.graphs[new_id].geoJson(),
        }
        
           
    def same_point(self, point1_source, point1_id, point2_source, point2_id):
        TOL_X = 0.1
        TOL_Y = 0.1
        TOL_ALTITUDE = 0.1
        TOL_STR_HEIGHT = 0.1

         # Check if the specified nodes exist in the graphs
        if point1_id not in self.graphs[point1_source].nodes() or point2_id not in self.graphs[point2_source].nodes():
            raise ValueError("One or both specified nodes do not exist in the graphs.")


        point1 = self.graphs[point1_source].nodes(point1_id)
        point2 = self.graphs[point2_source].nodes(point2_id)

        if abs(point1['x'] - point2['x']) >= TOL_X:
            return False
        
        if abs(point1['y'] - point2['y']) >= TOL_Y:
            return False
        
        if abs(point1['elevation'] - point2['elevation']) >= TOL_ALTITUDE:
            return False
        
        if abs(point1['structureHeight'] - point2['structureHeight']) >= TOL_STR_HEIGHT:
            return False
        return True

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
