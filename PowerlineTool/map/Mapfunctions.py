from pyproj import Proj, transform
import json
import geojson
import uuid
import copy

from . import LineStringInteractions



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
    
    elif type == "DCS-OO" :
        #OO
        lineString = LineStringInteractions.LineString()
        for i in range(0,len(feature["points"])-1) : 
            lineString.connect_points(feature["points"][i]["location"]["x"],feature["points"][i]["location"]["y"], feature["points"][i+1]["location"]["x"],feature["points"][i+1]["location"]["y"])

        return lineString
                
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

class StageOne: 
    def __init__(self, ) : 
        self.features = {}
        self.lineStringFeaturs = {}
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

        print(self.features)

    def addFeatureDCS(self, featureId, data) :
        test = dataConvert("DCS-OO", data)
        print(test.display_linetring())
        coordinates = dataConvert("DCS", data)
        self.features[featureId] = {
            "type"  : "DCS",
            "id"    : featureId, 
            "raw"   : data,
            "coordinates" : coordinates
        }

        print(coordinates)

    def remFeature(self, featureId) : 
        self.features.pop(featureId)

    def remFeatures(self) :
        self.features = {}


class Graph:
    def __init__(self):
        self.lineStrings = {}
    
    def add(self, lineString):
        self.lineStrings[lineString.id] = lineString
        
    def fuse_same_point(self, lineString_id1, point_id1, lineString_id2, point_id2):
        if lineString_id1 not in self.lineStrings or lineString_id2 not in self.lineStrings : 
            print(f"lineString: {lineString_id1} or {lineString_id2} not found in LineString")
            return
        
        lineString1 = self.lineStrings[lineString_id1]
        lineString2 = self.lineStrings[lineString_id2]
        
        if point_id1 not in lineString1.points or point_id2 not in lineString2.points :
            print(f"point: {point_id1} or {point_id2} not found in points")
            return 
        check = self._fuse_ctrl(lineString1.points[point_id1], lineString2.points[point_id2])
        if not all(check.values()):
            for key, item in check.items():
                print(key, " : ", item)
            return 
        
        # Create a new LineString to represent the fused line
        fused_Line = LineStringInteractions.LineString()
        
        # Copy points and edges from the first LineString
        fused_Line.points.update(copy.deepcopy(lineString1.points))
        fused_Line.edges.update(copy.deepcopy(lineString1.edges))
        
        # Copy points and edges from the second LineString
        fused_Line.points.update(copy.deepcopy(lineString2.points))
        fused_Line.edges.update(copy.deepcopy(lineString2.edges))
        
        # Remove duplicate data
        new_point = LineStringInteractions.Point(fused_Line.points[point_id1].x,fused_Line.points[point_id1].y)
        fused_Line.points[new_point.id] = new_point
        
        last_pts1 = fused_Line._out_point(point_id1)[0]
        last_pts2 = fused_Line._out_point(point_id2)[0]
        
        fused_Line.add_edge(last_pts1.id, new_point.id)
        fused_Line.add_edge(last_pts2.id, new_point.id)
                
        del fused_Line.edges[fused_Line.points[point_id2].edges[0]]
        del fused_Line.points[point_id2]
        
        del fused_Line.edges[fused_Line.points[point_id1].edges[0]]
        del fused_Line.points[point_id1]
        
        for key, point in fused_Line.points.items():
            for edge in point.edges : 
                if edge not in fused_Line.edges:
                    point.edges.remove(edge)
                        
        # Remove the second LineString
        del self.lineStrings[lineString_id2]
        del self.lineStrings[lineString_id1]
        
        # Update the first LineString with the fused LineString
        self.lineStrings[fused_Line.id] = fused_Line
        
        
    
    def divide(self, lineString_id, point_id):
        if lineString_id not in self.lineStrings:
            print(f"LineString id {lineString_id} not found.")
            return 
        
        lineString = self.lineStrings[lineString_id]
        
        if point_id not in lineString.points:
            print(f"Point id {point_id} not found in LineString {lineString_id}.")
            return
        
        out_edges_id = lineString.points[point_id].edges
        if len(out_edges_id) != 2:
            print(f"Cannot divide LineString {lineString_id} at point {point_id}.")
            return
                
        line_part1 = self.create_line_part(lineString, out_edges_id[0], point_id)
        line_part2 = self.create_line_part(lineString, out_edges_id[1], point_id)
        
        del self.lineStrings[lineString_id]
        
    def create_line_part(self, lineString, edge_id, point_id):
        line_part = LineStringInteractions.LineString()
        line_part.points = copy.deepcopy(lineString.points)
        line_part.edges = copy.deepcopy(lineString.edges)
        line_part.sup_edge(edge_id)
        line_part.sup_unreachable_points_edges(point_id)
        self.lineStrings[line_part.id] = line_part
        return line_part
        
    def display_graph(self):
        print("Graph:")
        for key, lineString in self.lineStrings.items():
            print(f"LineString ID: {lineString.id}")
            
            # Display points
            print("\tPoints:")
            for point_id, point in lineString.points.items():
                print(f"\t\tPoint: {point.id}, x/y: [{point.x}, {point.y}], edges: {point.edges}")
                
    
            # Display edges
            print("\tEdges:")
            for edge_id, edge in lineString.edges.items():
                print(f"\t\tEdge ID: {edge.id}, Start: {edge.start.id}, End: {edge.end.id}")
    
            print("\n")
            
    def _fuse_ctrl(self,point1,point2):
        valid = {}
        X_TOL = 0.1
        Y_TOL = 0.1
        #todo
        # ALTITUDE_TOL = 0.1
        # STRUCTURE_HEIGHT_TOL = 0.1
        
        valid['x_difference_check'] = abs(point1.x - point2.x) < X_TOL
        valid['y_difference_check'] = abs(point1.y - point2.y) < Y_TOL
        valid['pts1_is_ending_pts'] = len(point1.edges) == 1
        valid['pts2_is_ending_pts'] = len(point2.edges) == 1
        
        return valid
        
