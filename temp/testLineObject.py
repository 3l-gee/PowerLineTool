# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:17:30 2024

@author: Raphael_Gerth
"""
import networkx as nx
import uuid
import copy

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

Graph1 = nx.Graph()

for i in range(0, len(data["points"])-1):
    if i == 0 : 
        pts1_attributes = {
                "x": data["points"][i]["location"]["x"],
                "y": data["points"][i]["location"]["y"],
                "structureHeight": data["points"][i]["structureHeight"]["magnitude"],
                "elevation": data["points"][i]["elevation"]["magnitude"],
                "currentLighting":data["points"][i]["currentLighting"]
                }
        pts1_id = str(uuid.uuid4())[:6]
        Graph1.add_node(pts1_id, **pts1_attributes)
        
    pts2_attributes = {
        "x": data["points"][i+1]["location"]["x"],
        "y": data["points"][i+1]["location"]["y"],
        "structureHeight": data["points"][i+1]["structureHeight"]["magnitude"],
        "elevation": data["points"][i+1]["elevation"]["magnitude"],
        "currentLighting":data["points"][i+1]["currentLighting"],
#        "currentMarking":data["points"][i+1]["currentMarking"]
        }
    pts2_id = str(uuid.uuid4())[:6]
    Graph1.add_node(pts2_id, **pts2_attributes)
    
    jth_attributes = {
            "structureHeight": data["jths"][i]["structureHeight"]["magnitude"],
            "currentMarking": data["jths"][i]["currentMarking"]
            }
    Graph1.add_edge(pts1_id, pts2_id, attributes=data["jths"][i]) 	
    pts1_id = pts2_id
    
Graph2 = nx.Graph()

for i in range(0, len(data2["points"])-1):
    if i == 0 : 
        pts1_attributes = {
                "x": data2["points"][i]["location"]["x"],
                "y": data2["points"][i]["location"]["y"],
                "structureHeight": data2["points"][i]["structureHeight"]["magnitude"],
                "elevation": data2["points"][i]["elevation"]["magnitude"],
                "currentLighting":data2["points"][i]["currentLighting"]
                }
        pts1_id = str(uuid.uuid4())[:6]
        Graph2.add_node(pts1_id, **pts1_attributes)
        
    pts2_attributes = {
        "x": data2["points"][i+1]["location"]["x"],
        "y": data2["points"][i+1]["location"]["y"],
        "structureHeight": data2["points"][i+1]["structureHeight"]["magnitude"],
        "elevation": data2["points"][i+1]["elevation"]["magnitude"],
        "currentLighting":data2["points"][i+1]["currentLighting"],
#        "currentMarking":data["points"][i+1]["currentMarking"]
        }
    pts2_id = str(uuid.uuid4())[:6]
    Graph2.add_node(pts2_id, **pts2_attributes)
    
    jth_attributes = {
            "structureHeight": data2["jths"][i]["structureHeight"]["magnitude"],
            "currentMarking": data2["jths"][i]["currentMarking"]
            }
    Graph2.add_edge(pts1_id, pts2_id, attributes=data2["jths"][i]) 	
    pts1_id = pts2_id
    

    
def find_end_nodes(graph):
    end_nodes = [node for node in graph.nodes() if len(list(graph.neighbors(node))) == 1]
    return end_nodes

def traverse_graph(graph):
    # Function to find the end nodes
    def find_end_nodes(graph):
        end_nodes = [node for node in graph.nodes() if len(list(graph.neighbors(node))) == 1]
        return end_nodes


    # Find the start and end nodes
    end_nodes = find_end_nodes(graph)

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
#        print(f"Node attributes: {graph.nodes[current_node]}")
#        print(f"Edge {current_node} - {next_node}")
#        print(f"Edge attributes: {edge_data}")
#        print(f"Node: {next_node}")
#        print(f"Next node attributes: {node_data}")
#        print()

def compose(graph1, pts1_id,graph2, pts2_id):
    pts1 = graph1[pts1_id]
    pts2 = graph2[pts2_id]
    
    new_id = "test"
    
    new_attributes = {
        "x": 25,
        "y": 25,
        "structureHeight": 25,
        "elevation": 25,
        "currentLighting": "no"
        }
    
    graph1.add_node(new_id, **new_attributes)
    graph2.add_node(new_id, **new_attributes)
    
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
    
end_nodes = find_end_nodes(Graph1)

traverse_graph(Graph1)
traverse_graph(Graph2)

#G_composed = nx.compose(Graph1, Graph1)