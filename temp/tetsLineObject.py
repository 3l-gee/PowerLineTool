# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 08:12:51 2024

@author: gerth
"""
import uuid
import copy

class Point:
    def __init__(self, x, y):
        # Generate a unique identifier for the point
        self.id = str(uuid.uuid4())[:6]
        
        # Set the x and y coordinates of the point
        self.x = x
        self.y = y
        
        # Initialize an empty list to store the edges connected to this point
        self.edges = []
        
    def __str__(self):
        # Return a string representation of the Point for easy printing
        return f"\t\t{self.id}: [{self.x}, {self.y}, Edges: {self.edges}]"

class Edge:
    def __init__(self, start, end):
        # Generate a unique identifier for the edge
        self.id = str(uuid.uuid4())[:6]
        
        # Set the start and end points of the edge
        self.start = start
        self.end = end
        
        # Update the edges lists of the start and end points to include this edge
        self.start.edges.append(self.id)
        self.end.edges.append(self.id)
        
    def __str__(self):
        # Return a string representation of the Edge for easy printing
        return f"\t\t{self.id}: {self.start.id} to {self.end.id}"
            

class LineString:
    def __init__(self):
        # Generate a unique identifier for the LineString
        self.id = str(uuid.uuid4())[:6]
        
        # Dictionary to store points (key: point_id, value: Point instance)
        self.points = {}
        
        # Dictionary to store edges (key: edge_id, value: Edge instance)
        self.edges = {}
        
    def add_point(self, x, y):
        """Add a new point to the LineString."""
        new_point = Point(x, y)
        self.points[new_point.id] = new_point
        
    def add_edge(self, point_id_1, point_id_2):
        if point_id_1 not in self.points or point_id_2 not in self.points:
            print(f"One or more points not found.")
            return

        new_edge = Edge(self.points[point_id_1], self.points[point_id_2])

        self.edges[new_edge.id] = new_edge
        
    def connect_points(self, x1, y1, x2, y2):
        """Add a new edge to the LineString."""
        pts1 = Point(x1, y1)
        pts2 = Point(x2, y2)
        validation = self._validation(pts1)
        
        if validation is True:
            self.points[pts1.id] = pts1
            self.points[pts2.id] = pts2
            new_edge = Edge(pts1, pts2)
            self.edges[new_edge.id] = new_edge
        else:
            self.points[pts2.id] = pts2
            new_edge = Edge(validation, pts2)
            self.edges[new_edge.id] = new_edge
            
    def sup_point(self, point_id):
        """Remove a point and its associated edges."""
        if point_id not in self.points:
            print(f"Point with id {point_id} not found.")
            return

        # Remove edges associated with the point
        self.edges = {key: edge for key, edge in self.edges.items() if edge.start.id != point_id and edge.end.id != point_id}

        # Remove the point itself
        del self.points[point_id]
        
    def sup_edge(self, edge_id):
        """Remove an edge and update associated points."""
        if edge_id not in self.edges:
            print(f"Edge with id {edge_id} not found.")
            return

        # Get the edge and remove it from the start and end points' edge lists
        edge = self.edges[edge_id]
        for point_id in [edge.start.id, edge.end.id]:
            if edge_id in self.points[point_id].edges:
                self.points[point_id].edges.remove(edge_id)

        # Remove the edge itself
        del self.edges[edge_id]
                    
    def remove_unused_edges(self, visited):
        """Remove edges that are not marked as visited."""
        unused_edges = [edge_id for edge_id in self.edges if edge_id not in visited]
        for edge_id in unused_edges:
            self.sup_edge(edge_id)

    def remove_unused_points(self, visited):
        """Remove points that are not marked as visited."""
        unused_points = [point_id for point_id in self.points if point_id not in visited]
        for point_id in unused_points:
            self.sup_point(point_id)
            
            
    def _validation(self, point):
        """Check if a point with the same coordinates already exists."""
        for existing_point in self.points.values():
            if point.x == existing_point.x and point.y == existing_point.y:
                return existing_point
            
        return True         
                        
    def display_linetring(self):
        """Print the points and edges of the LineString."""
        print("\tPoints:")
        for point in self.points.values():
            print(point)

        print("\tEdges:")
        for edge in self.edges.values():
            print(edge)
            
    def sup_unreachable_points_edges(self, start_point_id):
        """Remove unused edges and points."""
        visited = set()

        # Start DFS from the specified point
        self._depth_first_search(start_point_id, visited)

        # Remove unused edges and points
        self.remove_unused_edges(visited)
        self.remove_unused_points(visited)

        # Check if all points are visited
        return len(visited) == len(self.points)
    
    def _depth_first_search(self, current_point_id, visited):
        """Perform depth-first search and mark visited points and edges."""
        visited.add(current_point_id)
        for edge_id in self.points[current_point_id].edges:
            visited.add(edge_id)
    
        # Explore the neighbors of the current point
        neighbors = self._out_point(current_point_id)
        for neighbor in neighbors:
            if neighbor.id not in visited:
                self._depth_first_search(neighbor.id, visited)
                       
            
    def invers_graph(self):
        """Reverse the direction of all edges in the LineString."""
        for edge in self.edges.values():
            edge.start, edge.end = edge.end, edge.start

    def _out_point(self, point_id):
        """Return the neighboring points of a given point."""
        res = []
        for edge_id in self.points[point_id].edges:
            points = [self.edges[edge_id].start, self.edges[edge_id].end]
            for point in points:
                if point.id != point_id:
                    res.append(point)
        return res

    def __str__(self):
        """Return a string representation of the LineString."""
        return f"\t{self.id}\n\t{len(self.points)} / {len(self.edges)}"
        
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
        fused_Line = LineString()
        
        # Copy points and edges from the first LineString
        fused_Line.points.update(copy.deepcopy(lineString1.points))
        fused_Line.edges.update(copy.deepcopy(lineString1.edges))
        
        # Copy points and edges from the second LineString
        fused_Line.points.update(copy.deepcopy(lineString2.points))
        fused_Line.edges.update(copy.deepcopy(lineString2.edges))
        
        # Remove duplicate data
        new_point = Point(fused_Line.points[point_id1].x,fused_Line.points[point_id1].y)
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
        line_part = LineString()
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
           

graph = Graph()

lineString1 = LineString()
for i in range(0,len(data["points"])-1) : 
    lineString1.connect_points(data["points"][i]["location"]["x"],data["points"][i]["location"]["y"], data["points"][i+1]["location"]["x"],data["points"][i+1]["location"]["y"])

graph.add(lineString1)

lineString2 = LineString()
for i in range(0,len(data2["points"])-1) : 
    lineString2.connect_points(data2["points"][i]["location"]["x"],data2["points"][i]["location"]["y"], data2["points"][i+1]["location"]["x"],data2["points"][i+1]["location"]["y"])

graph.add(lineString2)

graph.display_graph()

graph.fuse_same_point("xx1", "xx2", "yy1", "yy2")

    
# lineString1.display_linetring()
    
