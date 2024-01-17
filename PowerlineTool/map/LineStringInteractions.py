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
        
        #attributes
        #self.source = attributes["source"]
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
        

