import networkx as nx
import json
import uuid
from datetime import datetime
from . import lineString

class LineStringHandler: 
    """
    A class handling LineString objects and their features,

    Attributes:
        features : Dict[str, Dict]:
            Dictionary to store features
        graphs : Dict[str, LineString]):
            Dictionary to store LineString graphs, where the keys are feature IDs.
        TLMFeatures : Dict[str, Dict]:
            Dictionary to store TLM features, where the keys are TLM IDs.
    """
    def __init__(self) : 
        """
        Initializes a LineStringHandler object and loads all the tlm data in TLMFeatures

        Returns:
            None
        """
        self.features = {}
        self.graphs = {}
        self.TLMFeatures = {}
        tempList = json.load(open('PowerlineTool/map/static/map/data/TLMFullFeatures.json'))["obstacles"]
        for item in tempList :
            self.TLMFeatures[item["tlmID"]] = item

    def addFeatureTLM(self, featureId) :
        """
        Adds a TLM feature to the handler by loading its data from the generic TLM data.

        Parameters:
            featureId : str
                ID of the TLM feature to be added.

        Returns:
            None
        """
        rawFeature = self.TLMFeatures[featureId]
        graph = lineString.LineString()
        graph.TLM_reader(rawFeature,featureId)
        self.graphs[featureId] = graph
        self.features[featureId] = {
            "type"  : "TLM",
            "id"    : featureId, 
            "raw"   : rawFeature,
            "coordinates" : graph.geo_json(),
        }

    def addFeatureDCS(self, featureId, data) :
        """
        Adds a DCS feature to the handler.

        Parameters:
            featureId : str
                ID of the DCS feature to be added.
            data : Dict
                DCS data

        Returns:
            None
        """
        graph = lineString.LineString()
        graph.DCS_reader(data,featureId)
        self.graphs[featureId] = graph
        self.features[featureId] = {
            "type"  : "DCS",
            "id"    : featureId, 
            "raw"   : data,
            "coordinates" : graph.geo_json(),
        }


    def remFeature(self, featureId) :
        self.features.pop(featureId)
        self.graphs.pop(featureId)

    def remFeatures(self) :
        self.features = {}
        self.graphs = {}

    def divide(self, point_source, point_id):
        """
        Divides the features at the specified point
        Generates two sub features and all the linked information
        Deletes the original feature.

            Parameters:
                point_source : str
                    The source identifier of the point.
                point_id : str
                    The identifier of the point where the graph should be divided.

            Returns:
                None
        """
        left_graph,right_graph = self.graphs[point_source].divide(point_id)
        self.graphs[left_graph["id"]] = left_graph["graph"]
        self.graphs[right_graph["id"]] = right_graph["graph"]

        self.features[left_graph["id"]] = {
            "type"  : "divide",
            "id"    : left_graph["id"], 
            "raw"   : None,
            "coordinates" : self.graphs[left_graph["id"]].geo_json()
        }

        self.features[right_graph["id"]] = {
            "type"  : "divide",
            "id"    : right_graph["id"], 
            "raw"   : None,
            "coordinates" : self.graphs[right_graph["id"]].geo_json()
        }

        print(left_graph,right_graph)

        self.remFeature(point_source)
    
    def fuse(self, point1_source, point1_id, point2_source, point2_id):
        """
        Fuses two points from different sources into a new node and updates the graph and features accordingly.

        Parameters:
            point1_source : str
                The source identifier of the first point.
            point1_id : str
                The identifier of the first point.
            point2_source : str
                The source identifier of the second point.
            point2_id : str
                The identifier of the second point.

        Returns:
            None
        """
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
        new_node_id = str(uuid.uuid4())[:6]
        new_attributes = {
            "x": node1['x'],
            "y": node1['y'],
            "structureHeight": node1['structureHeight'],
            "elevation": node1['elevation'],
            "currentLighting": "TEST"
        }

        nx_graph1.add_node(new_node_id, **new_attributes)
        nx_graph2.add_node(new_node_id, **new_attributes)

        # Create a composed graph using nx.compose
        composed = nx.compose(nx_graph1, nx_graph2)
        
        # Reroute edges that used to go to pts1 and pts2 to the new_id
        for neighbor in list(nx_graph1.neighbors(point1_id)):
            composed.add_edge(neighbor, new_node_id, **nx_graph1.get_edge_data(point1_id, neighbor))
        for neighbor in list(nx_graph2.neighbors(point2_id)):
            composed.add_edge(neighbor, new_node_id, **nx_graph2.get_edge_data(point2_id, neighbor))

            
        # Remove old pts1 and pts2 nodes
        if (point1_id == point2_id) :
            composed.remove_node(point1_id)
        else :
            composed.remove_node(point1_id)
            composed.remove_node(point2_id)

        self.remFeature(point1_source)
        self.remFeature(point2_source)

        self.graphs[new_id] = lineString.LineString(composed,new_id, history)
        self.features[new_id] = {
            "type"  : "fused",
            "id"    : new_id,
            "raw"   : [],
            "coordinates" : self.graphs[new_id].geo_json(),
        }
        
    def neighboors(self, point_source, point_id):
        return self.graphs[point_source].neighboors(point_id)
             
           
    def same_point(self, point1_source, point1_id, point2_source, point2_id):
        """
        Checks if two points from different sources represent the same geographical location within specified tolerances.

        Parameters:
            point1_source : str
                The source identifier of the first point.
            point1_id : str
                The identifier of the first point.
            point2_source : str
                The source identifier of the second point.
            point2_id : str
                The identifier of the second point.

        Returns:
            bool: True 
                if the points represent the same geographical location within specified tolerances, False otherwise.
        
        Raises:
            ValueError: If one or both specified nodes do not exist in the graphs.
        """
        TOL_X = 0.1
        TOL_Y = 0.1
        TOL_ALTITUDE = 0.1
        TOL_STR_HEIGHT = 0.1

        # TODO structured test implementation
        # TESTS = {
        #     "tolerance_x" : {
        #         "tolrance" : TOL_X,
        #         "value" : None,
        #         "test" : ">=",
        #         "outcome" : False
        #     },
        #     "tolerance_y" :{
        #         "tolrance" : TOL_Y,
        #         "value" : None,
        #         "test" : ">="
        #         "outcome" : False
        #     },
        #     "tolerance_alt" :{
        #         "tolrance" : TOL_ALTITUDE,
        #         "value" : None,
        #         "test" : ">=",
        #         "outcome" : False
        #     },
        #     "tolerance_str_height" :{
        #         "tolrance" : TTOL_STR_HEIGHTOL_X,
        #         "value" : None,
        #         "test" : ">=",
        #         "outcome" : False
        #     },
        # }
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
