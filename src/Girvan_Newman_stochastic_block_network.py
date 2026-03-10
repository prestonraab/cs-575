""" Create a graph using the algorithm following equations 1 and 2 
from https://arxiv.org/pdf/cond-mat/0210146

Newman, Mark EJ, and Michelle Girvan. 
"Mixing patterns and community structure in networks." 
Statistical mechanics of complex networks. 
Springer, Berlin, Heidelberg, 2003. 66-87.

Implementation by Mike Goodrich
Brigham Young University
February 2022

Updated February 2024
Updated March 2025
"""

import networkx as nx # type: ignore
import numpy as np
from numpy.typing import NDArray
import random
from typing import List, Tuple


########################
## Set Default Values ##
########################
# Default mixing matrix has four classes
DEFAULT_M: NDArray[np.float32] = np.array([[0.4, 0.02, 0.01, 0.03],
                [0.02, 0.4, 0.03, 0.02],
                [0.01, 0.03, 0.4, 0.01],
                [0.03, 0.02, 0.01, 0.4]]) 
# By default, all node classes have same degree distribution
DEFAULT_LAMBDA: list[int] = [5, 4, 3, 2] 
DEFAULT_NUM_EDGES: int = 200

class Node_Type:
    def __init__(self, ID: int, remaining_degree: int, node_type: int):
        self.ID: int = ID
        self.remaining_degree: int = remaining_degree
        self.node_type: int = node_type

    def __repr__(self) -> str:
        return f"Node_Type(ID={self.ID}, remaining_degree={self.remaining_degree}, node_type={self.node_type})"

class AssortativeMixing:
    edge_count_by_type: dict[tuple[int, int], int] = {}
    stubs_per_class: dict[int, int] = {}

    def __init__(self,
                 M: NDArray[np.float32] = DEFAULT_M, 
                 poisson_lambda:list[int] = DEFAULT_LAMBDA, 
                 num_edges:int = DEFAULT_NUM_EDGES,
                 seed: int | None = None,
                 ) -> None:
        
        self.partition: list[set[int]] = []
        self._random: random.Random = random.Random(seed)
        self._np_random: np.random.Generator = np.random.default_rng(seed)

        ## Choose how many edges of each type will be  used
        edge_count_by_type = self._draw_edges_from_mixing_matrix(M, num_edges)
        type(self).edge_count_by_type = edge_count_by_type
        self.edge_count_by_type = edge_count_by_type

        # Count the number of stubs required in each class
        stubs_per_class = self._get_number_of_stubs_per_class(edge_count_by_type, len(M))
        type(self).stubs_per_class = stubs_per_class
        self.stubs_per_class = stubs_per_class

        ## For each class
        starting_node_id: int = 0
        all_nodes: list[Node_Type] = []
        
        for node_class in stubs_per_class.keys():
            # Get the number of nodes required for that class
            num_required_nodes = self._get_number_nodes_in_class(stubs_per_class[node_class], 
                                                                 poisson_lambda[node_class])
            
            # Create that many nodes with random degrees
            node_list = self._create_nodes_for_class(node_class, 
                                                     num_required_nodes, 
                                                     poisson_lambda[node_class], 
                                                     starting_node_id)
            starting_node_id += len(node_list)
            
            # Resample node degree so that total degree = required number of stubs
            node_list = self._resample_node_degrees_in_nodelist(node_list, 
                                                                stubs_per_class[node_class],
                                                                poisson_lambda[node_class])

            # Add nodes from this class to list of all nodes
            all_nodes.extend(node_list)
        ## End of for loop over nodes to add

        ## Find edges to add
        all_edges = self._add_edges(edge_count_by_type, all_nodes)

        # Create an empty graph and add nodes and edges to it
        G: nx.Graph = nx.Graph()
        G = self._add_nodes_to_graph(G, all_nodes)
        G = self._add_edges_to_graph(G, all_edges)
        
        self.G: nx.Graph = G
            
    #############################
    ## Initialization Routines ##
    #############################
    def _draw_edges_from_mixing_matrix(self, 
                    mixing_matrix: NDArray[np.float32],
                    num_edges: int
                    ) -> dict[tuple[int,int],int]:
        """
            Choose the number of each edge type between and within classes 
            that will be in the graph using the mixing matrix

            • Input: a square mixing matrix with probabilities
                describing probability of edges within and
                across classes
            • Output: a dictionary keyed by a tuple of edge type
                with values the number of edges of that type
        """
        num_types: int = len(mixing_matrix)
        edge_count_by_type: dict[tuple[int, int], int] = dict()
        # Initialize dictionary of edges (i,j) 
        edge_count_by_type = {(i, j): 0 for i in range(num_types) for j in range(num_types)}
                
        # Draw edges until the desired number is reached
        count: int = 0
        edge_types: list[tuple[int, int]] = list(edge_count_by_type.keys())
        while True:
            # Shuffle edge order
            self._random.shuffle(edge_types)
            for edge in edge_types:
                if self._random.uniform(0.0, 1.0) < mixing_matrix[edge[0]][edge[1]]:
                    edge_count_by_type[edge] += 1
                    count += 1
                    if count == num_edges:
                        return edge_count_by_type

    def _get_number_of_stubs_per_class(self,
                                   edge_count_by_type: dict[tuple[int,int],int],
                                   num_classes: int
                                   ) -> dict[int, int]:
        """
            Once we know how many edges are needed for each edge type, count
            the number of stubs that are needed in each class. Do this by
            counting the number of edge end points that are in each class

            • Input: 
                - a dictionary of the number of edges indexed by edge type
                - the number of classes
            • Output: a dictionary indexed by the class number that contains
                the number of stubs required for that class
        """

        class_total_degree: dict[int, int] = dict()
        class_total_degree = {node_class: 0 for node_class in range(num_classes)}
        for edge in edge_count_by_type.keys():
            class_total_degree[edge[0]] += edge_count_by_type[edge]
            class_total_degree[edge[1]] += edge_count_by_type[edge]
        return class_total_degree

    def _get_number_nodes_in_class(self,
                                    stubs_in_class: int,
                                    average_degree_per_node: int
                                   ) -> int:
        """
            Given the number of stubs in a class, determine the number
            of nodes that will be required in that class. This is done
            by dividing the number of stubs in the class by the average
            degree per node in the class

            • Input: number of stubs per class
            • Output: number of nodes in the class
        """
        
        return int(np.ceil(stubs_in_class/average_degree_per_node))

    ##################################
    ## Routines for loop over nodes ##
    ##################################
    def _create_nodes_for_class(self, 
                                node_class: int,
                                num_required_nodes: int,
                                poisson_lambda: int,
                                starting_node_ID: int
                                ) -> list[Node_Type]:
        """
            Given a required number of nodes and the lambda value
            for a class, create a list of that many nodes and their
            degree, which are randomly chosen.  Nodes are labeled
            with IDs that start at the starting node ID

            • Input:
                - node class
                - required number of nodes in the class
                - the poisson parameter used to assign the degree for the node
                - the starting node ID 
            • Output: a list of nodes, which has a node ID and a node degree
        """ 
        node_list: list[Node_Type] = []
        for node_id in range(starting_node_ID, starting_node_ID+num_required_nodes):
            node_degree: int = int(self._np_random.poisson(poisson_lambda))
            # No nodes with degree zero are allowed
            while node_degree == 0:
                node_degree = int(self._np_random.poisson(poisson_lambda))
            node_list.append(Node_Type(node_id, node_degree, node_class))
        return node_list
    
    def _resample_node_degrees_in_nodelist(self,
                                          node_list: list[Node_Type],
                                          required_number_of_stubs: int,
                                          poisson_lambda: int
                                          ) -> list[Node_Type]:
        """
            The list of nodes that were generated in the previous step have
            arbitrary degree, and the total degree of the nodes might not
            match the number of stubs required for the class. Choose a node
            at random, resample its degree, and repeat until the total degree
            equals the required number of stubs
        """

        total_degree: int = sum([node.remaining_degree for node in node_list])
        while total_degree != required_number_of_stubs:
            node: Node_Type = self._random.choice(node_list)
            total_degree -= node.remaining_degree
            node.remaining_degree = int(self._np_random.poisson(poisson_lambda))
            # No nodes with degree zero are allowed
            while node.remaining_degree == 0:
                node.remaining_degree = int(self._np_random.poisson(poisson_lambda))
            total_degree += node.remaining_degree

        return node_list
    
    ###############################
    ## Routines for adding edges ##
    ###############################
    def _add_edges(self,
                   edge_count_by_class: dict[Tuple[int, int], int],
                   node_list: list[Node_Type],
                   max_attempts: int = 100
                   ) -> List[Tuple[Node_Type, Node_Type]]:
        """ 
            Desparately needs to be refactored!
        """
        
        # Number of edges that need to be added
        edges_to_add: list[tuple[Node_Type, Node_Type]] = []

        # List of nodes in each class dictionary
        nodelist_by_class: dict[int, set[Node_Type]] = {class_id: set() for class_id in {node.node_type for node in node_list}}
        for node in node_list:
            nodelist_by_class[node.node_type].add(node) 

        # List of all edge types to be added with repeat elements. 
        # This facilitates randomization
        edge_types_to_add: list[Tuple[int, int]] = []
        for edge_type, count in edge_count_by_class.items():
            for _ in range(count):
                edge_types_to_add.append(edge_type)

        # Shuffle order of edge types to add to avoid bias        
        self._random.shuffle(edge_types_to_add)

        # Iterate through each edge type to add
        while len(edge_types_to_add) > 0:
            edge_type = edge_types_to_add[0]
            choices_for_node_1: list[Node_Type] = [node for node in nodelist_by_class[edge_type[0]] if node.remaining_degree>0]
            choices_for_node_2: list[Node_Type] = [node for node in nodelist_by_class[edge_type[1]] if node.remaining_degree>0]
            failed_attempt: bool = True
            if len(choices_for_node_1) > 0 and len(choices_for_node_2) > 0:
                for _ in range(max_attempts):
                    node1: Node_Type = self._random.choice(choices_for_node_1)
                    node2: Node_Type = self._random.choice(choices_for_node_2)
                    if node1.ID != node2.ID and \
                        (node1, node2) not in edges_to_add and\
                        (node2, node1) not in edges_to_add:
                        failed_attempt = False
                        # Notice that we have to check whether eigher order of the edge is in
                        # the set of edges to add since the graph is undirected
                        break
            
            if failed_attempt:
                # If I've tried hard to add an edge but run into problems, remove a random edge and try again
                edge = self._random.choice(edges_to_add)
                # Put the edge type back in the list of edge types that need to be added
                edge_types_to_add.append((edge[0].node_type, edge[1].node_type))
                # remove the edge from list of edges to be added
                edges_to_add.remove(edge)
                # update the remaining degree for the nodes at the ends of the edges
                edge[0].remaining_degree += 1
                edge[1].remaining_degree += 1
            else:
                edge_types_to_add = edge_types_to_add[1:]
                edges_to_add.append((node1, node2))
                node1.remaining_degree -= 1
                node2.remaining_degree -= 1

        return edges_to_add
    
    ########################
    ## Graph Construction ##
    ########################
    def _add_nodes_to_graph(self,
                             G: nx.Graph,
                             node_list: list[Node_Type]
                             ) -> nx.Graph:
        """ 
            Take an empty graph and add the nodes from the nodelist to it.
            Label each node with its class and its degree

            • Input:
                - empty graph nx.Graph
                - node list

            • Output: graph with nodes added
        """
        for node in node_list:
            G.add_node(node.ID, node_class = node.node_type)
        
        return G
    
    def _add_edges_to_graph(self,
                             G: nx.Graph,
                             edge_list: list[Tuple[Node_Type,Node_Type]]
                             ) -> nx.Graph:
        """ 
            Take graph with node edges and add the edges from the.
            Label each node with its class and its degree

            • Input:
                - graph nx.Graph with no edges
                - edge list

            • Output: graph with edges added
        """
        for node1, node2 in edge_list:
            G.add_edge(node1.ID, node2.ID)
        
        return G