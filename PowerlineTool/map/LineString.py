import networkx as nx
import uuid
import geojson

class LineString: 
    def __init__(self): 
        self.graph = nx.Graph()

    def TLM_reader(self, tlm_data):
        # Iterate through points in TLM data
        for i in range(0, len(tlm_data["points"])-1):
            if i == 0: 
                pts1_attributes = {
                    "x": tlm_data["points"][i]["location"]["x"],
                    "y": tlm_data["points"][i]["location"]["y"],
                    "structureHeight": tlm_data["points"][i]["structureHeight"]["magnitude"],
                    "elevation": tlm_data["points"][i]["terrain"]["magnitude"],
                    "currentLighting": "NONE",
                    "currentMarking": "NONE"
                }
                pts1_id = str(uuid.uuid4())[:6]
                self.graph.add_node(pts1_id, **pts1_attributes)

            # Add the second point as a node to the graph
            pts2_attributes = {
                "x": tlm_data["points"][i+1]["location"]["x"],
                "y": tlm_data["points"][i+1]["location"]["y"],
                "structureHeight": tlm_data["points"][i+1]["structureHeight"]["magnitude"],
                "elevation": tlm_data["points"][i+1]["terrain"]["magnitude"],
                "currentLighting": "NONE",
                "currentMarking": "NONE"
            }
            pts2_id = str(uuid.uuid4())[:6]
            self.graph.add_node(pts2_id, **pts2_attributes)
            
            # Add the edge between the two points with attributes
            jth_attributes = {
                "structureHeight": tlm_data["lines"][i]["structureHeight"]["magnitude"],
                "currentMarking": "NONE"
            }
            self.graph.add_edge(pts1_id, pts2_id, attributes=jth_attributes) 	
            pts1_id = pts2_id

        
    def DCS_reader(self, dcs_data): 
        # Iterate through points in DCS data
        for i in range(0, len(dcs_data["points"])-1):
            # Add the first point as a node to the graph
            if i == 0: 
                pts1_attributes = {
                    "x": dcs_data["points"][i]["location"]["x"],
                    "y": dcs_data["points"][i]["location"]["y"],
                    "structureHeight": dcs_data["points"][i]["structureHeight"]["magnitude"],
                    "elevation": dcs_data["points"][i]["elevation"]["magnitude"],
                    "currentLighting": dcs_data["points"][i]["currentLighting"],
                    "currentMarking": "NONE"
                }
                pts1_id = str(uuid.uuid4())[:6]
                self.graph.add_node(pts1_id, **pts1_attributes)
            
            # Add the second point as a node to the graph
            pts2_attributes = {
                "x": dcs_data["points"][i+1]["location"]["x"],
                "y": dcs_data["points"][i+1]["location"]["y"],
                "structureHeight": dcs_data["points"][i+1]["structureHeight"]["magnitude"],
                "elevation": dcs_data["points"][i+1]["elevation"]["magnitude"],
                "currentLighting": dcs_data["points"][i+1]["currentLighting"],
                "currentMarking": "NONE"
            }
            pts2_id = str(uuid.uuid4())[:6]
            self.graph.add_node(pts2_id, **pts2_attributes)
            
            # Add the edge between the two points with attributes
            jth_attributes = {
                "structureHeight": dcs_data["jths"][i]["structureHeight"]["magnitude"],
                "currentMarking": dcs_data["jths"][i]["currentMarking"]
            }
            self.graph.add_edge(pts1_id, pts2_id, attributes=jth_attributes) 	
            pts1_id = pts2_id
                    
    def _find_end_nodes(self):
        # Find nodes with only one neighbor (end nodes)
        end_nodes = [node for node in self.graph.nodes() if len(list(self.graph.neighbors(node))) == 1]
        return end_nodes
    
    def traverse_graph(self):       
        # Find end nodes of the graph
        end_nodes = self._find_end_nodes()
        
        # Traverse the linestring graph from the start node to each end node
        print(f"Start Node: {end_nodes[0]}")
    
        # Use nx.shortest_path to find the path
        path = nx.shortest_path(self.graph, end_nodes[0], end_nodes[1])
        
        # Traverse the linestring graph and print node and edge attributes
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
    
            edge_data = self.graph.get_edge_data(current_node, next_node)
            node_data = self.graph.nodes[next_node]
            
            print(f"Edge {current_node} - {next_node}")
            print(f"Node: {next_node}")
    

    def geoJson(self, type, graph_id): 
        # Find end nodes of the graph
        end_nodes = self._find_end_nodes()
        # Use nx.shortest_path to find the path
        path = nx.shortest_path(self.graph, end_nodes[0], end_nodes[1])
        
        # Create a list to store the coordinates of the LineString
        coordinates = []
        features = []
        # Traverse the linestring graph and collect node coordinates
        for node in path:
            node_data = self.graph.nodes[node]
            coordinates.append((node_data['x'], node_data['y']))
            attributes = {
                "id" : node,
                "description": graph_id,
                "elevation" : node_data['elevation'],
                "structureHeight" : node_data['structureHeight']
            }
            point_geojson = geojson.Feature(geometry=geojson.Point((node_data['x'], node_data['y'])), properties=attributes)
            features.append(point_geojson)
        # Create a GeoJSON LineString
        attributes = {
                "id" : graph_id,
                "type" : type
            }
        line_string = geojson.LineString(coordinates)
        feature = geojson.Feature(geometry=line_string, properties=attributes)
        features.append(feature)
        
        return geojson.FeatureCollection(features)