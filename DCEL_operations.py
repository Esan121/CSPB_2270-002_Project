from Dcel_Classes import Vertex, HalfEdge, Face
import matplotlib.pyplot as plt
import pandas as pd

def create_dcel(vertices):
  
    num_vertices = len(vertices)

    # Create half-edges
    half_edges = []
    for i in range(num_vertices):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % num_vertices]
        e1 = HalfEdge(v1, None, None, None, None)
        e2 = HalfEdge(v2, None, None, None, None)
        e1.twin = e2
        e2.twin = e1
        half_edges.append(e1)
        half_edges.append(e2)

    # Link half-edges
    for i in range(num_vertices):
        e1 = half_edges[2 * i]
        e2 = half_edges[2 * (i + 1) % (2 * num_vertices)]
        e3 = half_edges[(2 * i + 1) % (2 * num_vertices)]
        e1.next = e2
        e2.prev = e1
        e3.next = e1
        e1.prev = e3

    # Create face
    face = Face(half_edges[0])
    for e in half_edges:
        e.face = face

    return [face]

def point_in_polygon(point, face):

  x, y = point
  inside = False  # Initialize inside variable

  # Start at the outer component of the face
  edge = face.outer_component

  while True:
    # Check if y falls outside polygon's vertical range (early exit)
    if y < min(edge.origin.y, edge.next.origin.y) or y > max(edge.origin.y, edge.next.origin.y):
      return False

    # Get edge start and end points
    edge_start = edge.origin
    edge_end = edge.next.origin

    # Check if y lies between edge's y range
    if y > min(edge_start.y, edge_end.y) and y <= max(edge_start.y, edge_end.y):

      # Check if x is to the right of the edge (considering direction)
      if edge_end.x > edge_start.x:
        if x <= max(edge_start.x, edge_end.x):
          # Calculate and compare intersection (if not horizontal)
          if edge_start.y != edge_end.y:
            x_intersect = (y - edge_start.y) * (edge_end.x - edge_start.x) / (edge_end.y - edge_start.y) + edge_start.x
            if x_intersect <= x:
              inside = not inside
      else:  # Edge goes from right to left
        if x >= min(edge_start.x, edge_end.x):
          # Calculate and compare intersection (if not horizontal)
          if edge_start.y != edge_end.y:
            x_intersect = (y - edge_start.y) * (edge_end.x - edge_start.x) / (edge_end.y - edge_start.y) + edge_start.x
            if x_intersect > x:
              inside = not inside

    edge = edge.next
    if edge is face.outer_component:
      break

  return inside

def line_intersection(line_start, line_end, face):

  def do_segments_intersect(p0, p1, p2, p3):

   def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

  # Check if the line segments intersect
  return ccw(p0, p2, p3) != ccw(p1, p2, p3) and ccw(p0, p1, p2) != ccw(p0, p1, p3)

  edge = face.outer_component
  while True:
    edge_start = edge.origin
    edge_end = edge.next.origin

    if do_segments_intersect(line_start, line_end, edge_start, edge_end):
      return True

    edge = edge.next
    if edge is face.outer_component:
      break

  return False

def insert_vertex(half_edge, new_vertex):
  new_half_edge1 = HalfEdge(new_vertex, None, None, None)
  new_half_edge2 = HalfEdge(half_edge.origin, None, None, None)

  # Adjust pointers
  new_half_edge1.twin = new_half_edge2
  new_half_edge2.twin = new_half_edge1

  new_half_edge1.next = half_edge.next
  half_edge.next.prev = new_half_edge1

  new_half_edge2.next = new_half_edge1
  new_half_edge1.prev = new_half_edge2

  half_edge.next = new_half_edge2
  new_half_edge2.prev = half_edge


  return new_half_edge1, new_half_edge2

def delete_vertex(vertex):
  start_edge = vertex.incident_edge
  current_edge = start_edge

  while True:
    next_edge = current_edge.next

    # Update twin pointers
    current_edge.twin.twin = next_edge
    next_edge.twin = current_edge.twin

    # Update next and prev pointers
    current_edge.next.prev = current_edge.prev
    current_edge.prev.next = current_edge.next

    # Update face information
    face = current_edge.incident_face
    if face:
      if face.outer_component == current_edge:
        face.outer_component = next_edge
      elif face.outer_component == current_edge.twin:
        face.outer_component = next_edge.twin

      # Handle empty face
      if face.outer_component == face.outer_component.next:
        if face in your_face_data_structure:
          your_face_data_structure.remove(face)

    current_edge = next_edge
    if current_edge == start_edge:
      break



def print_polygon(face):
  start_edge = face.outer_component
  current_edge = start_edge

  while True:
    print(current_edge.origin.x, current_edge.origin.y)
    current_edge = current_edge.next
    if current_edge == start_edge:
      break

def draw_polygon(face):
  x_coords, y_coords = [], []
  start_edge = face.outer_component
  current_edge = start_edge

  while True:
    x_coords.append(current_edge.origin.x)
    y_coords.append(current_edge.origin.y)
    current_edge = current_edge.next
    if current_edge == start_edge:
      break

  plt.plot(x_coords, y_coords, '-o')
  plt.axis('equal')
  plt.show()

def calculate_area(face):
  half_edge = face.outer_component # Starting half-edge
  area = 0.0

  while True:
    p1 = half_edge.origin
    p2 = half_edge.next.origin
    area += (p1.x * p2.y) - (p2.x * p1.y)
    half_edge = half_edge.next
    if half_edge == face.outer_component:
      break

  return abs(area) / 2.0