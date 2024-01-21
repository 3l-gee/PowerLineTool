import networkx as nx
import uuid
import geojson
from datetime import datetime

class LineString:
    def __init__(self, existing_graph=None, graph_id=None, history=None):
        if existing_graph:
            self.graph = existing_graph.copy()
            self.graph_id = graph_id
            self.history = history
        else:
            self.graph = nx.Graph()
            self.graph_id = None
            self.history = [    ]

    def nodes(self, node_id=None):
        if node_id:
            return self.graph.nodes[node_id]
        return self.graph.nodes

    def add_node(self, node_id, **attributes):
        self.graph.add_node(node_id, **attributes)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    def add_edge(self, node1, node2, **attributes):
        self.graph.add_edge(node1, node2, **attributes)

    def remove_edge(self, node1, node2):
        self.graph.remove_edge(node1, node2)

    def neighbors(self, node_id):
        return list(self.graph.neighbors(node_id))
    
    def get_edge_data(self, node1, node2, default=None):
        return self.graph.get_edge_data(node1, node2, default=default)
    
    def divide(self, node_id):
        if node_id not in self.graph.nodes:
            raise ValueError(f"Node {node_id} does not exist in the graph.")

        left_graph_id = str("divided-" + str(uuid.uuid4())[:6])
        right_graph_id = str("divided-" + str(uuid.uuid4())[:6])

        left_line = LineString(existing_graph=self.graph.subgraph(nx.dfs_tree(self.graph, source=node_id).nodes))
        right_line = LineString(existing_graph=self.graph.subgraph(nx.dfs_tree(self.graph, source=node_id, reverse=True).nodes))

        left_graph = {
            "id": left_graph_id,
            "graph":left_line
        }
        right_graph = {
            "id": right_graph_id,
            "graph":right_line
        }
        return left_graph,right_graph

    def TLM_reader(self, tlm_data,graph_id):
        self.graph_id = graph_id
        timestamp = datetime.now().isoformat()
        self.history.append({
            'timestamp': timestamp,
            'operation': 'init_TLM',
            'parameter': graph_id
        })

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

        
    def DCS_reader(self, dcs_data, graph_id): 
        self.graph_id = graph_id
        timestamp = datetime.now().isoformat()
        self.history.append({
            'timestamp': timestamp,
            'operation': 'init_DCS',
            'parameter': graph_id
        })
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
    

    def geoJson(self): 
        # Find end nodes of the graph
        end_nodes = self._find_end_nodes()
        # Use nx.shortest_path to find the path
        path = nx.shortest_path(self.graph, end_nodes[0], end_nodes[1])

        def get_time(items):
            return items.get('timestamp')

        self.history.sort(key=get_time)
        
        # Create a list to store the coordinates of the LineString
        coordinates = []
        features = []
        # Traverse the linestring graph and collect node coordinates
        for node in path:
            node_data = self.graph.nodes[node]
            coordinates.append((node_data['x'], node_data['y']))
            attributes = {
                "id" : node,
                "source" : self.graph_id,
                "elevation" : node_data['elevation'],
                "structureHeight" : node_data['structureHeight']
            }
            point_geojson = geojson.Feature(geometry=geojson.Point((node_data['x'], node_data['y'])), properties=attributes)
            features.append(point_geojson)
        # Create a GeoJSON LineString
        attributes = {
                "source" : self.graph_id,
                "history" : self.history
            }
        line_string = geojson.LineString(coordinates)
        feature = geojson.Feature(geometry=line_string, properties=attributes)
        features.append(feature)
        
        return geojson.FeatureCollection(features)
    