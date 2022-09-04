import random

import numpy as np

class Graph:
    def __init__(self):
        self._vertices = []

    def add_vertex(self, vertex: 'Vertex'):
        self._vertices.append(vertex)

    def add_vertices(self, vertices: list):
        self._vertices.extend(vertices)

    @property
    def vertices(self) -> tuple:
        return tuple(self._vertices)

    @property
    def n_unvisited_vertices(self) -> int:
        n_unvisited = 0
        for vertex in self._vertices:
            if vertex.to_edges or vertex.from_edges:
                n_unvisited += 1
        return n_unvisited

    def __str__(self) -> str:
        return "\n".join([str(vertex) for vertex in self._vertices])

    def __repr__(self) -> str:
        return str(self)


class Vertex:
    def __init__(self, id):
        self._id = id
        self._to_edges = [] # edges leaving this vertex
        self._from_edges = [] # edges arriving at this vertex

    def connect_to(self, vertex: 'Vertex'):
        edge = DirectedEdge(self, vertex)
        self._to_edges.append(edge)
        vertex.add_from_edge(edge)

    def add_from_edge(self, edge: 'DirectedEdge'):
        self._from_edges.append(edge)

    def del_to_edges(self):
        edge_copy = tuple(self._to_edges)
        for edge in edge_copy:
            edge.delete()
        self._to_edges = []

    def del_from_edges(self):
        edge_copy = tuple(self._from_edges)
        for edge in edge_copy:
            edge.delete()
        self._from_edges = []

    def del_all_edges(self):
        self.del_to_edges()
        self.del_from_edges()

    def del_to(self, edge):
        try:
            self._to_edges.remove(edge)
        except ValueError:
            pass

    def del_from(self, edge):
        try:
            self._from_edges.remove(edge)
        except ValueError:
            pass

    def get_edge_to(self, vertex: "Vertex") -> "DirectedEdge":
        for edge in self._to_edges:
            if edge.to_vertex == vertex:
                return edge

    def get_edge_from(self, vertex: "Vertex"):
        for edge in self._from_edges:
            if edge.from_vertex == vertex:
                return edge

    @property
    def id(self) -> int:
        return self._id

    @property
    def n_to_edges(self) -> int:
        return len(self._to_edges)

    @property
    def n_from_edges(self) -> int:
        return len(self._from_edges)

    @property
    def n_all_edges(self) -> int:
        return self.n_to_edges + self.n_from_edges

    @property
    def to_edges(self) -> tuple:
        return tuple(self._to_edges)

    @property
    def from_edges(self) -> tuple:
        return tuple(self._from_edges)

    @property
    def all_edges(self) -> tuple:
        return self.to_edges + self.from_edges

    @property
    def to_vertices(self) -> tuple:
        return tuple(edge.to_vertex for edge in self._to_edges)
        
    @property
    def from_vertices(self) -> tuple:
        return tuple(edge.from_vertex for edge in self._from_edges)

    @property
    def all_vertices(self) -> tuple:
        return self.to_vertices + self.from_vertices
    
    def __str__(self) -> str:
        return f"{[vertex.id for vertex in self.from_vertices]} -> {self.id} -> {[vertex.id for vertex in self.to_vertices]}"

    def __repr__(self) -> str:
        return str(self)


class DirectedEdge:
    def __init__(self, from_vertex: 'Vertex', to_vertex: 'Vertex'):
        self._from = from_vertex
        self._to = to_vertex

    @property
    def from_vertex(self) -> tuple:
        return self._from

    @property
    def to_vertex(self) -> tuple:
        return self._to

    def delete(self):
        self._from.del_to(self)
        self._to.del_from(self)

    def __str__(self) -> str:
        return f"{self._from.id} -> {self._to.id}"

    def __repr__(self) -> str:
        return str(self)


def get_min_outbound_edge_vertices(vertices: list) -> list:
    min_to_list = []
    min_to_len = float('inf')
    for vertex in vertices:
        if vertex.n_to_edges == min_to_len:
            min_to_list.append(vertex)
        elif 0 < vertex.n_to_edges < min_to_len:
            min_to_list = [vertex]
            min_to_len = vertex.n_to_edges

    return min_to_list


def get_min_inbound_edge_vertices(vertices: list) -> list:
    min_from_list = []
    min_from_len = float('inf')
    for vertex in vertices:
        if vertex.n_from_edges == min_from_len:
            min_from_list.append(vertex)
        elif 0 < vertex.n_from_edges < min_from_len:
            min_from_list = [vertex]
            min_from_len = vertex.n_from_edges

    return min_from_list
        
def simple_cycle_finder(graph: np.array, allow_pairs=True) -> list:
    # Allow cycles of 2 if the graph has a length of 2
    if len(graph) == 2:
        allow_pairs = True

    graph_edges = []
    fail_counter = 0

    # Repeat in case the solution is not valid
    while len(graph_edges) != len(graph):
        # Catch the edge case where the graph doesn't have any cycles
        fail_counter += 1
        if fail_counter > 5:
            raise ValueError("Unable to find Hamiltonian cycle for this graph")
        
        connection_graph = parse_graph(graph)


        while connection_graph.n_unvisited_vertices:
            # Randomly choose a node from those with the fewest outbound neighbours
            min_edge_vertices = get_min_outbound_edge_vertices(connection_graph.vertices)
            min_vertex = random.choice(min_edge_vertices)
            # Find the neighbours of the selected vertex with the fewest inbound neighbours
            neighbours = min_vertex.to_vertices
            if len(neighbours) > 1:
                min_neighbours = get_min_inbound_edge_vertices(neighbours)
                min_neighbour = random.choice(min_neighbours)
            else:
                min_neighbour = neighbours[0]

            edge = min_vertex.get_edge_to(min_neighbour)
            edge.delete()
            # If we don't want cycles of length 2, remove the reverse edge
            if not allow_pairs:
                reverse_edge = min_vertex.get_edge_from(min_neighbour)
                if reverse_edge:
                    reverse_edge.delete()
            min_vertex.del_to_edges()
            min_neighbour.del_from_edges()

            graph_edges.append(edge)

    cycles = []
    while len(graph_edges):
        edge = graph_edges[0]
        found_edges = {edge}
        cycle = [edge.from_vertex.id]
        next_vertex = edge.to_vertex
        while next_vertex.id != cycle[0]:
            for edge in graph_edges:
                if edge.from_vertex == next_vertex:
                    break
            cycle.append(edge.from_vertex.id)
            found_edges.add(edge)
            next_vertex = edge.to_vertex

        # breakpoint()
        graph_edges = [v for v in graph_edges if v not in found_edges]
        cycles.append(cycle)

    return cycles


def parse_graph(graph: np.array) -> Graph:
    graph_obj = Graph()

    # Create vertices
    graph_obj.add_vertices([Vertex(index) for index in range(len(graph))])

    # Connect the vertices
    for vertex, row in zip(graph_obj.vertices, graph):
        for index, connected in enumerate(row):
            if connected:
                vertex.connect_to(graph_obj.vertices[index])

    return graph_obj

if __name__ == "__main__":
    g = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0]])
    print(f"Sample graph is:\n{g}", end="\n\n")
    print(f"Full results:\n{simple_cycle_finder(g)}", end="\n\n")
