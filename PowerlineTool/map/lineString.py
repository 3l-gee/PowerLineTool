import networkx as nx
import uuid
import geojson
from datetime import datetime
import copy

class LineString:
    """
    A class representing a line graph structure with graph manipulation.

    Attributes:
        graph : nx.Graph()
            NetworkX graph object
        graph_id: str
            Unique identifier .
        history: List[Dict[str, Any]]
            List of dictionaries documenting the operations.
    """
    def __init__(self, existing_graph=None, graph_id=None, history=None):
        """
        Initializes a LineString object.

            Parameters:
                existing_graph (optional): nx.Graph()
                    An existing graph to be copied.
                graph_id (optional): str
                    A unique identifier for the graph.
                history (optional): List[Dict[str, Any]]
                    A list of dictionaries documenting the operations.

            Returns:
                None
        """
        if existing_graph:
            self.graph = existing_graph.copy()
            self.graph_id = graph_id
            self.history = history
        else:
            self.graph = nx.Graph()
            self.graph_id = None
            self.history = []

    def nodes(self, node_id=None):
        if node_id:
            return self.graph.nodes[node_id]
        return self.graph.nodes

    def add_node(self, node_id, **attributes):
        self.graph.add_node(node_id, **attributes)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    def add_edge(self, node_id1, node_id2, **attributes):
        self.graph.add_edge(node_id1, node_id2, **attributes)

    def remove_edge(self, node_id1, node_id2):
        self.graph.remove_edge(node_id1, node_id2)

    def neighbors(self, node_id):
        return list(self.graph.neighbors(node_id))
    
    def get_edge_data(self, node_id1, node_id2, default=None):
        return self.graph.get_edge_data(node_id1, node_id2, default=default)
    
    def divide(self, node_id):
        """
        Divides the graph into two subgraphs at the specified node.

            Parameters
            node_id: str
                ID of the node at which to divide.

            Returns:
                tuple: Two subgraphs as LineString objects.
        """
        if node_id not in self.graph.nodes:
            raise ValueError(f"Node {node_id} does not exist in the graph.")
        
        timestamp = datetime.now().isoformat()
        self.history.append({
            'timestamp': timestamp,
            'operation': 'divide',
            'parameter': {
                "source" : self.graph_id,
                "node_id" : node_id,
            }
        })

        left_graph_id = str("divided-" + str(uuid.uuid4())[:6])
        right_graph_id = str("divided-" + str(uuid.uuid4())[:6])

        neighbors = list(self.graph.neighbors(node_id))

        left_subgraph = self.graph.copy()
        right_subgraph = self.graph.copy()

        left_subgraph.remove_edge(node_id, neighbors[0])
        right_subgraph.remove_edge(node_id, neighbors[1])

        isolated_nodes_left = []
        for node in left_subgraph.nodes : 
            if not nx.has_path(left_subgraph, node_id, node):
                isolated_nodes_left.append(node)

        isolated_nodes_right = []
        for node in right_subgraph.nodes : 
            if not nx.has_path(right_subgraph, node_id, node):
                isolated_nodes_right.append(node)

        left_subgraph.remove_nodes_from(isolated_nodes_left)
        right_subgraph.remove_nodes_from(isolated_nodes_right)

        edges_to_remove_left = list(nx.isolates(left_subgraph))
        edges_to_remove_right = list(nx.isolates(right_subgraph))

        left_subgraph.remove_edges_from(edges_to_remove_left)
        right_subgraph.remove_edges_from(edges_to_remove_right)

        left_line = LineString(existing_graph=left_subgraph,graph_id=left_graph_id, history=self.history)
        right_line = LineString(existing_graph=right_subgraph,graph_id=right_graph_id, history=self.history)

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
        """
        Initializes the graph using data from TLM

            Parameters:
                tlm_data : dict
                    Data representing a TLM.
                graph_id : str
                    Unique identifier for the graph.

            Returns:
                None
        """
        self.graph_id = graph_id
        timestamp = datetime.now().isoformat()
        self.history.append({
            'timestamp': timestamp,
            'operation': 'init_TLM',
            'parameter': {
                "TLM_id" : graph_id
            }
        })

        for i in range(0, len(tlm_data["points"])-1):
            if i == 0: 
                

                node_id1_attributes = {
                    "x": tlm_data["points"][i]["location"]["x"],
                    "y": tlm_data["points"][i]["location"]["y"],
                    "structureHeight": tlm_data["points"][i]["structureHeight"]["magnitude"],
                    "elevation": tlm_data["points"][i]["terrain"]["magnitude"],
                    "currentLighting": "NONE",
                    "currentMarking": "NONE",
                    "description" : None
                }
                node_id1 = str(uuid.uuid4())[:6]
                self.graph.add_node(node_id1, **node_id1_attributes)

            node_id2_attributes = {
                "x": tlm_data["points"][i+1]["location"]["x"],
                "y": tlm_data["points"][i+1]["location"]["y"],
                "structureHeight": tlm_data["points"][i+1]["structureHeight"]["magnitude"],
                "elevation": tlm_data["points"][i+1]["terrain"]["magnitude"],
                "currentLighting": "NONE",
                "currentMarking": "NONE",
                "description" : None
            }
            node_id2 = str(uuid.uuid4())[:6]
            self.graph.add_node(node_id2, **node_id2_attributes)
            
            jth_attributes = {
                "structureHeight": tlm_data["lines"][i]["structureHeight"]["magnitude"],
                "currentMarking": "NONE"
            }
            self.graph.add_edge(node_id1, node_id2, attributes=jth_attributes) 
            node_id1 = node_id2

        
    def DCS_reader(self, dcs_data, graph_id): 
        """Initializes the graph using data from  DCS.

            Parameters:
                dcs_data : dict
                    Data representing a DCS.
                graph_id : str
                Unique identifier for the graph.

            Returns:
                None
            """
        self.graph_id = graph_id
        timestamp = datetime.now().isoformat()
        self.history.append({
            'timestamp': timestamp,
            'operation': 'init_DCS',
            'parameter': {
                "DCS_ID" : graph_id
            }
        })

        for i in range(0, len(dcs_data["points"])-1):
            if i == 0: 
                node_id1_attributes = {
                    "x": dcs_data["points"][i]["location"]["x"],
                    "y": dcs_data["points"][i]["location"]["y"],
                    "structureHeight": dcs_data["points"][i]["structureHeight"]["magnitude"],
                    "elevation": dcs_data["points"][i]["elevation"]["magnitude"],
                    "currentLighting": dcs_data["points"][i].get("currentLighting", "NONE"),
                    "currentMarking": dcs_data["points"][i].get("currentMarking", "NONE"),
                    "description" : dcs_data["points"][i].get("description", None)
                }
                node_id1 = str(uuid.uuid4())[:6]
                self.graph.add_node(node_id1, **node_id1_attributes)
            
            node_id2_attributes = {
                "x": dcs_data["points"][i+1]["location"]["x"],
                "y": dcs_data["points"][i+1]["location"]["y"],
                "structureHeight": dcs_data["points"][i+1]["structureHeight"]["magnitude"],
                "elevation": dcs_data["points"][i+1]["elevation"]["magnitude"],
                "currentLighting": dcs_data["points"][i+1].get("currentLighting", "NONE"),
                "currentMarking": dcs_data["points"][i+1].get("currentMarking", "NONE"),
                "description" : dcs_data["points"][i+1].get("description", None)
            }
            node_id2 = str(uuid.uuid4())[:6]
            self.graph.add_node(node_id2, **node_id2_attributes)
            
            jth_attributes = {
                "structureHeight": dcs_data["jths"][i]["structureHeight"]["magnitude"],
                "currentMarking": dcs_data["jths"][i].get("currentMarking","NONE")
            }
            self.graph.add_edge(node_id1, node_id2, attributes=jth_attributes) 

            node_id1 = node_id2
                    
    def find_end_nodes(self):
        end_nodes = [node for node in self.graph.nodes() if len(list(self.graph.neighbors(node))) == 1]
        return end_nodes
    
    # def traverse_graph(self):       
    #     end_nodes = self.find_end_nodes()
        
    #     print(f"Start Node: {end_nodes[0]}")
    
    #     path = nx.shortest_path(self.graph, end_nodes[0], end_nodes[1])
        
    #     for i in range(len(path) - 1):
    #         current_node = path[i]
    #         next_node = path[i + 1]
    
    #         edge_data = self.graph.get_edge_data(current_node, next_node)
    #         node_data = self.graph.nodes[next_node]
            
    #         print(f"Edge {current_node} - {next_node}")
    #         print(f"Node: {next_node}")
    

    def geo_json(self):
        """Generates a GeoJSON representation of the graph.

            Returns:
                geojson.FeatureCollection: 
                    GeoJSON representation of the graph.
            """
        end_nodes = self.find_end_nodes()

        path = nx.shortest_path(self.graph, end_nodes[0], end_nodes[1])

        def get_time(items):
            return items.get('timestamp')

        self.history.sort(key=get_time)
        
        coordinates = []
        features = []
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

        attributes = {
                "source" : self.graph_id,
                "history" : self.history[-3:],
                "ctrl"  :{
                    "nodes" : self.graph.number_of_nodes(),
                    "edges" : self.graph.number_of_edges()
                }
            }
        line_string = geojson.LineString(coordinates)
        feature = geojson.Feature(geometry=line_string, properties=attributes)
        features.append(feature)
        
        return geojson.FeatureCollection(features)
    
    def DCS_writer(self):
        """Generates a DCS formated json for Points and JTH of the graph
            Returns:
                json
        """
        res = {
            "points" : [],
            "jths" :[]
        }
        end_nodes = self.find_end_nodes()

        path = nx.shortest_path(self.graph, end_nodes[0], end_nodes[1])

        def get_time(items):
            return items.get('timestamp')
        
        first_node_data = self.graph.nodes[path[0]]
        res["points"].append({
            "structureHeight" : {
                "magnitude" : round(float(first_node_data['structureHeight']),3),
                "unit" : "METERS"
            },
            "currentMarking" : first_node_data['currentMarking'],
            "currentLighting" : first_node_data['currentLighting'],
            "description": first_node_data['description'] if first_node_data['description'] is not None else "TLM1",
            "location" : {
                "crs" : 2056,
                "x" : round(float(first_node_data['x']),3),
                "y" : round(float(first_node_data['y']),3)
            },
            "elevation" : {
                "magnitude" : round(float(first_node_data['elevation']),3),
                "unit" : "METERS",
                "verticalDatum" : 5728
            }
        })
        for i in range(1,len(path)) :
            node_data = self.graph.nodes[path[i]]
            edge_data = self.graph.get_edge_data(path[i-1], path[i])["attributes"]

            temp_point = {
                "structureHeight" : {
                    "magnitude" : round(float(node_data['structureHeight']),3),
                    "unit" : "METERS"
                },
                "currentMarking" : node_data['currentMarking'],
                "currentLighting" : node_data['currentLighting'],
                "description": node_data['description'] if node_data['description'] is not None else f"TLM{i+1}",
                "location" : {
                    "crs" : 2056,
                    "x" : round(float(node_data['x']),3),
                    "y" : round(float(node_data['y']),3)
                },
                "elevation" : {
                    "magnitude" : round(float(node_data['elevation']),3),
                    "unit" : "METERS",
                    "verticalDatum" : 5728
                }
            }
            copied_temp_point = copy.deepcopy(temp_point)
            res["points"].append(copied_temp_point)

            temp_jth = {
                "structureHeight" : {
                "magnitude" : round(float(edge_data["structureHeight"]),3),
                "unit" : "METERS"
                },
                "currentMarking" : edge_data["currentMarking"]
            }
            copied_temp_jth = copy.deepcopy(temp_jth)
            res["jths"].append(copied_temp_jth)

        return res