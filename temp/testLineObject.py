# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:17:30 2024

@author: Raphael_Gerth
"""
import networkx as nx
import uuid
import copy

class LineString: 
    def __init__(self): 
        self.graphs = {}
        
    def DCS_reader(self, dcs_data): 
        # Create a new graph for each DCS data
        graph = nx.Graph()
        graph_id = str(uuid.uuid4())[:6]
        
        # Iterate through points in DCS data
        for i in range(0, len(dcs_data["points"])-1):
            # Add the first point as a node to the graph
            if i == 0: 
                pts1_attributes = {
                    "x": dcs_data["points"][i]["location"]["x"],
                    "y": dcs_data["points"][i]["location"]["y"],
                    "structureHeight": dcs_data["points"][i]["structureHeight"]["magnitude"],
                    "elevation": dcs_data["points"][i]["elevation"]["magnitude"],
                    "currentLighting": dcs_data["points"][i]["currentLighting"]
                }
                pts1_id = str(uuid.uuid4())[:6]
                graph.add_node(pts1_id, **pts1_attributes)
            
            # Add the second point as a node to the graph
            pts2_attributes = {
                "x": dcs_data["points"][i+1]["location"]["x"],
                "y": dcs_data["points"][i+1]["location"]["y"],
                "structureHeight": dcs_data["points"][i+1]["structureHeight"]["magnitude"],
                "elevation": dcs_data["points"][i+1]["elevation"]["magnitude"],
                "currentLighting": dcs_data["points"][i+1]["currentLighting"]
            }
            pts2_id = str(uuid.uuid4())[:6]
            graph.add_node(pts2_id, **pts2_attributes)
            
            # Add the edge between the two points with attributes
            jth_attributes = {
                "structureHeight": dcs_data["jths"][i]["structureHeight"]["magnitude"],
                "currentMarking": dcs_data["jths"][i]["currentMarking"]
            }
            graph.add_edge(pts1_id, pts2_id, attributes=jth_attributes) 	
            pts1_id = pts2_id
            
        # Store the graph and its attributes
        self.graphs[graph_id] = {
            "graph": graph,
            "attribute": None 
        }
        
    def _find_end_nodes(self, graph):
        # Find nodes with only one neighbor (end nodes)
        end_nodes = [node for node in graph.nodes() if len(list(graph.neighbors(node))) == 1]
        return end_nodes
    
    def traverse_graph(self, graph_id):
        # Retrieve the graph from the stored data
        graph = self.graphs[graph_id]["graph"]
        
        # Find end nodes of the graph
        end_nodes = self._find_end_nodes(graph)
        
        # Traverse the linestring graph from the start node to each end node
        print(f"Start Node: {end_nodes[0]}")
    
        # Use nx.shortest_path to find the path
        path = nx.shortest_path(graph, end_nodes[0], end_nodes[1])
        
        # Traverse the linestring graph and print node and edge attributes
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
    
            edge_data = graph.get_edge_data(current_node, next_node)
            node_data = graph.nodes[next_node]
            
            print(f"Edge {current_node} - {next_node}")
            print(f"Node: {next_node}")
            
            
    def generate_geojson(self, graph_id):
        # Retrieve the graph from the stored data
        graph = self.graphs[graph_id]["graph"]
        
        # Find end nodes of the graph
        end_nodes = self._find_end_nodes(graph)
        
        # Traverse the linestring graph from the start node to each end node
        print(f"Start Node: {end_nodes[0]}")
    
        # Use nx.shortest_path to find the path
        path = nx.shortest_path(graph, end_nodes[0], end_nodes[1])
        
        # Traverse the linestring graph and print node and edge attributes
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
    
            edge_data = graph.get_edge_data(current_node, next_node)
            node_data = graph.nodes[next_node]
            
            print(f"Edge {current_node} - {next_node}")
            print(f"Node: {next_node}")
    
    def compose(self, graph1, pts1_id, graph2, pts2_id):
        # Extract nodes from both graphs
        pts1 = graph1[pts1_id]
        pts2 = graph2[pts2_id]
        
        # Create a new node with some attributes
        new_id = "test"
        new_attributes = {
            "x": 25,
            "y": 25,
            "structureHeight": 25,
            "elevation": 25,
            "currentLighting": "no"
        }
        
        # Add the new node to both graphs
        graph1.add_node(new_id, **new_attributes)
        graph2.add_node(new_id, **new_attributes)
        
        # Create a composed graph using nx.compose
        composed = nx.compose(graph1, graph2)
        
        # Reroute edges that used to go to pts1 and pts2 to the new_id
        for neighbor in list(graph1.neighbors(pts1_id)):
            composed.add_edge(neighbor, new_id, **graph1.get_edge_data(pts1_id, neighbor))
        for neighbor in list(graph2.neighbors(pts2_id)):
            composed.add_edge(neighbor, new_id, **graph2.get_edge_data(pts2_id, neighbor))
            
        # Remove old pts1 and pts2 nodes
        composed.remove_node(pts1_id)
        composed.remove_node(pts2_id)
        
        return composed

        

data = {
    "points": [
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 10,
                "y": 10
            },
            "elevation": {
                "magnitude": 775.45,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        },
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 20,
                "y": 20
            },
            "elevation": {
                "magnitude": 678.19,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        },
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 30,
                "y": 30
            },
            "elevation": {
                "magnitude": 836.46,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        }, {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 40,
                "y": 40
            },
            "elevation": {
                "magnitude": 775.45,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        },
    ],
    "jths": [
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentMarking": "NONE"
        },
        {
            "structureHeight": {
                "magnitude": 10,
                "unit": "METERS"
            },
            "currentMarking": "NONE"
        },
        {
            "structureHeight": {
                "magnitude": 30,
                "unit": "METERS"
            },
            "currentMarking": "NONE"
        }
    ]
}
            
data2 = {
    "points": [
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 110,
                "y": 110
            },
            "elevation": {
                "magnitude": 775.45,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        },
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 120,
                "y": 120
            },
            "elevation": {
                "magnitude": 678.19,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        },
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 130,
                "y": 130
            },
            "elevation": {
                "magnitude": 836.46,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        }, {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentLighting": "NONE",
            "location": {
                "crs": 2056,
                "x": 40,
                "y": 40
            },
            "elevation": {
                "magnitude": 775.45,
                "unit": "METERS",
                "verticalDatum": 5728
            }
        },
    ],
    "jths": [
        {
            "structureHeight": {
                "magnitude": 0,
                "unit": "METERS"
            },
            "currentMarking": "NONE"
        },
        {
            "structureHeight": {
                "magnitude": 10,
                "unit": "METERS"
            },
            "currentMarking": "NONE"
        },
        {
            "structureHeight": {
                "magnitude": 30,
                "unit": "METERS"
            },
            "currentMarking": "NONE"
        }
    ]
}

    

#G_composed = nx.compose(Graph1, Graph1)

LineString = LineString()

LineString.DCS_reader(data)
LineString.DCS_reader(data2)
