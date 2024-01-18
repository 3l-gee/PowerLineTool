# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 08:12:51 2024

@author: gerth
"""
import uuid
import copy

class Point:
    def __init__(self, x, y, attributes=None):
        # Generate a unique identifier for the point
        self.id = str(uuid.uuid4())[:6]
        
        # Set the x and y coordinates of the point
        self.x = x
        self.y = y
                
        self.attributes = attributes
        
    def __str__(self):

        # Return a string representation of the Point for easy printing
        return f"{self.id}: [{self.x}, {self.y}"

class Edge:
    def __init__(self, start, end, attributes=None):
        # Generate a unique identifier for the edge
        self.id = str(uuid.uuid4())[:6]
        
        # Set the start and end points of the edge
        self.start = start
        self.end = end
        
        self.attributes = attributes
        
    def reroute(self, new_start, new_end):
        # No need to remove from the old points since they no longer store edges
        self.start = new_start
        self.end = new_end

        
    def __str__(self):
        # Return a string representation of the Edge for easy printing
        return f"{self.id}: {self.start.id} to {self.end.id}"
    
    
class LineString:
    def __init__(self):
        # Generate a unique identifier for the LineString
        self.id = str(uuid.uuid4())[:6]
        
        # Dictionary to store points (key: point_id, value: Point instance)
        self.points = {}
        
        # Dictionary to store edges (key: edge_id, value: Edge instance)
        self.edges = {}
        
    def add_point(self, x, y, attributes=None):
        """Add a new point to the LineString."""
        new_point = Point(x, y, attributes)
        self.points[new_point.id] = new_point
        return new_point

    def add_edge(self, start_point, end_point, attributes=None):
        """Add a new edge to the LineString."""
        new_edge = Edge(start_point, end_point, attributes)
        self.edges[new_edge.id] = new_edge
        
    def remove_edge(self, edge_id):
        if edge_id not in self.edges:
            print(f"Edge with id {edge_id} not found.")
            return

        # Remove the edge itself
        del self.edges[edge_id]
        
    def remove_point(self, point_id):
        if point_id not in self.points:
            print(f"Point with id {point_id} not found.")
            return

        # Remove the point itself
        del self.points[point_id]

        # Remove edges associated with the point
        for edge_id in list(self.edges):
            edge = self.edges[edge_id]
            if edge.start.id == point_id or edge.end.id == point_id:
                self.remove_edge(edge_id)
                
    def outgoing_edges(self, point_id):
        """Get the outgoing edges of a point in the LineString."""
        if point_id not in self.points:
            print(f"Point id {point_id} not found in LineString.")
            return []

        return [edge for edge in self.edges.values() if edge.start.id == point_id or edge.end.id == point_id]
                
    def find_endpoints(self):
        """Find endpoints in the LineString."""
        endpoints = [point_id for point_id, point in self.points.items() if self._count_connections(point) == 1]
        return endpoints

    def _count_connections(self, point):
        """Count the number of edges connected to a point."""
        return sum(1 for edge in self.edges.values() if edge.start.id == point.id or edge.end.id == point.id)
                
    def traverse_graph(self, start_point_id=None):
        """Traverse the graph using Depth-First Search (DFS) starting from an endpoint."""
        endpoints = self.find_endpoints()

        if not endpoints:
            print("No endpoints found. The graph might be disconnected or incomplete.")
            return

        # If start_point_id is not provided, start from the first endpoint found
        start_point_id = start_point_id or endpoints[0]

        visited_points = set()

        def dfs(point_id):
            visited_points.add(point_id)
            current_point = self.points[point_id]
            print(f"\nNode {current_point.id}: [{current_point.x}, {current_point.y}] attributes: {current_point.attributes}")

            # Find edges connected to the current point
            connected_edges = [edge_id for edge_id, edge in self.edges.items()
                               if edge.start.id == point_id or edge.end.id == point_id]

            for edge_id in connected_edges:
                edge = self.edges[edge_id]
                print(f"\tEdge {edge.id}: {edge.start.id} to {edge.end.id}  attributes: {edge.attributes}")

                # Determine the next point to visit
                next_point_id = edge.end.id if edge.start.id == point_id else edge.start.id

                # Recursively traverse the next point if it hasn't been visited
                if next_point_id not in visited_points:
                    dfs(next_point_id)

        dfs(start_point_id)
        
    def find_reachable_points(self, start_point_id):
        """Find reachable points in the LineString starting from a given point."""
        visited_points = set()

        def dfs(point_id):
            visited_points.add(point_id)
        
            for edge in self.outgoing_edges(point_id):
                next_point_id = edge.end.id if edge.start.id == point_id else edge.start.id
                if next_point_id not in visited_points:
                    dfs(next_point_id)

        dfs(start_point_id)
        return visited_points
                

        
class LineString_OLD:
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
        """Print the points and edges of the LineString by traversing connections."""
        visited_points = set()
        visited_edges = set()
    
        def find_starting_point():
            # Find a point with only one connection (an edge)
            for point_id, point in self.points.items():
                if len(point.edges) == 1:
                    return point
            return None
    
        def traverse_from_point(point):
            if point.id in visited_points:
                return
            visited_points.add(point.id)
    
            print(f"\t\tPoint: {point.id}, x/y: [{point.x}, {point.y}]")
    
            for edge_id in point.edges:
                edge = self.edges[edge_id]
                if edge.id not in visited_edges:

                    visited_edges.add(edge.id)
                    next_point = edge.end if edge.start.id == point.id else edge.start
                    print(f"\t\t\tEdge: {edge.id}:  {point.id} to {next_point.id}")
                    traverse_from_point(next_point)
    
        starting_point = find_starting_point()
        if starting_point:
            traverse_from_point(starting_point)
    
        print("\tUnused Edges:")
        for edge_id in self.edges:
            if edge_id not in visited_edges:
                edge = self.edges[edge_id]
                print(f"\t\tEdge ID: {edge.id}, Start: {edge.start.id}, End: {edge.end.id}")
    
        print("\tUnused Points:")
        for point_id in self.points:
            if point_id not in visited_points:
                point = self.points[point_id]
                print(f"\t\tPoint: {point.id}, x/y: [{point.x}, {point.y}]")



                        
    # def display_linetring(self):
    #     """Print the points and edges of the LineString."""
    #     print("\tPoints:")
    #     for point in self.points.values():
    #         print(point)

    #     print("\tEdges:")
    #     for edge in self.edges.values():
    #         print(edge)
            
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
        fused_line = LineString()
        
        # Copy points and edges from the first LineString
        fused_line.points.update(copy.deepcopy(lineString1.points))
        fused_line.edges.update(copy.deepcopy(lineString1.edges))
        
        # Copy points and edges from the second LineString
        fused_line.points.update(copy.deepcopy(lineString2.points))
        fused_line.edges.update(copy.deepcopy(lineString2.edges))
        
        # Remove duplicate data
        new_point = Point(fused_line.points[point_id1].x,fused_line.points[point_id1].y)
        fused_line.points[new_point.id] = new_point
        
        last_point2_id = [fused_line.edges[fused_line.outgoing_edges(point_id2)[0].id].start.id, fused_line.edges[fused_line.outgoing_edges(point_id2)[0].id].end.id]
        last_point2_id.remove(point_id2)
        last_point2_id
        
        last_point1_id = [fused_line.edges[fused_line.outgoing_edges(point_id1)[0].id].start.id, fused_line.edges[fused_line.outgoing_edges(point_id1)[0].id].end.id]
        last_point1_id.remove(point_id1)
        last_point1_id
        
        
        
        print(last_point2_id, last_point1_id)
        fused_line.add_edge(last_point1_id, new_point.id)
        fused_line.add_edge(last_point2_id, new_point.id)
        
        # print(point_id1)
                
        # print (fused_line.outgoing_edges(point_id1))
        # print (fused_line.edges[fused_line.outgoing_edges(point_id1)[0].id])
        # del fused_line.edges[fused_line.outgoing_edges(point_id1)[0].id]
        # del fused_line.points[point_id2]
        
        # del fused_line.edges[fused_line.outgoing_edges(point_id2)[0].id]
        # del fused_line.points[point_id1]
        
        # for key, point in fused_Line.points.items():
        #     for edge in point.edges : 
        #         if edge not in fused_Line.edges:
        #             point.edges.remove(edge)
                        
        # Remove the second LineString
        del self.lineStrings[lineString_id2]
        del self.lineStrings[lineString_id1]
        
        # Update the first LineString with the fused LineString
        self.lineStrings[fused_line.id] = fused_line
        
       

        
    def create_line_part(self, lineString, edge_id, point_id):
        line_part = LineString()
        line_part.points = copy.deepcopy(lineString.points)
        line_part.edges = copy.deepcopy(lineString.edges)
    
        # Remove the specified edge
        line_part.remove_edge(edge_id)
    
        # Remove unreachable points and edges in the new line part
        reachable_points = line_part.find_reachable_points(point_id)
        unreachable_points_ids = []
        for key, point in line_part.points.items() :
            if point.id not in reachable_points:
                unreachable_points_ids.append(point.id)
                
        for unreachable_point_id in unreachable_points_ids: 
            line_part.remove_point(unreachable_point_id)
            
        # Add the new line part to the graph
        self.lineStrings[line_part.id] = line_part
    
        
    def display_graph(self):
        print("Graph:")
        for key, lineString in self.lineStrings.items():
            print(f"LineString ID: {lineString.id}")
            
            print(lineString.traverse_graph())
            
            # # Display points
            # print("\tPoints:")
            # for point_id, point in lineString.points.items():
            #     print(f"\t\tPoint: {point.id}, x/y: [{point.x}, {point.y}], edges: {point.edges}")
                
    
            # # Display edges
            # print("\tEdges:")
            # for edge_id, edge in lineString.edges.items():
            #     print(f"\t\tEdge ID: {edge.id}, Start: {edge.start.id}, End: {edge.end.id}")
    
            # print("\n")
            
    def _fuse_ctrl(self,point1,point2):
        valid = {}
        X_TOL = 0.1
        Y_TOL = 0.1
        #todo
        # ALTITUDE_TOL = 0.1
        # STRUCTURE_HEIGHT_TOL = 0.1
        
        valid['x_difference_check'] = abs(point1.x - point2.x) < X_TOL
        valid['y_difference_check'] = abs(point1.y - point2.y) < Y_TOL
        # valid['pts1_is_ending_pts'] = len(point1.edges) == 1
        # valid['pts2_is_ending_pts'] = len(point2.edges) == 1
        
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
pts1 = lineString1.add_point(data["points"][0]["location"]["x"],data["points"][0]["location"]["y"], attributes={"point" : 0})
for i in range(1,len(data["points"])) : 
    pts2 = lineString1.add_point(data["points"][i]["location"]["x"],data["points"][i]["location"]["y"], attributes={"point" : i})
    lineString1.add_edge(pts1, pts2, attributes={"segment" : i})     
    pts1 = pts2
    
graph.add(lineString1)

lineString2 = LineString()
pts1 = lineString2.add_point(data2["points"][0]["location"]["x"],data2["points"][0]["location"]["y"])
for i in range(1,len(data2["points"])) : 
    pts2 = lineString2.add_point(data2["points"][i]["location"]["x"],data2["points"][i]["location"]["y"])
    lineString2.add_edge(pts1, pts2)     
    pts1 = pts2
    
graph.add(lineString2)

graph.display_graph()

# graph.fuse_same_point("xx1", "xx2", "yy1", "yy2")

    
# lineString1.display_linetring()
    
