## Dendrogram
## 
## Mike Goodrich
## Brigham Young University
## Feb 2025, December 2024
## 
## Basic code started with sharing the get_all_partitions with chatGPT
## and asking for code to generate the link matrix required for scipy's
## dendrogram function. ChatGPT's code didn't work, but by using the
## understanding_dendrograms Jupyter notebook and iterating with my
## own code and chatGPT's code, this code was produced. 


import networkx as nx # type: ignore
import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Hashable, Set, FrozenSet, List # Used for type hints

# Networkx nodes have type Hashable. It's tedious to keep writing
# Set[Hashable] so I created an alias. The code should work on any
# Hashable object
Group = Set[Hashable]

class DendrogramHandler:
    def __init__(self,G: nx.Graph):
        all_partitions = self.get_all_partitions(G)
        self.link_matrix, self.link_matrix_labels = self.partitions_to_linkage(all_partitions)

    def get_all_partitions(self, G: nx.Graph
                           ) -> list[Tuple[Group, ...]]:
        """
            Use edge betweenness defined by Girvan and Newman to find
            a collection of partitions. 
            
            Each partition is defined as a tuple of groups, and each
            group contains a set of nodes. Partitions require that the 
            set of groups are mutually exclusive and that the union of 
            the groups equals the set of all nodes in the graph.

            Example: A nx.path_graph(5) has nodes {0, 1, ... 4}
            The partitions returned from this function are
            [({0, 1, 2, 3, 4},), (the comma next to "4}" is necessary)
            ({0, 1}, {2, 3, 4}),
            ({0, 1}, {2}, {3, 4}),
            ({0}, {1}, {2}, {3,4}),
            ({0}, {1}, {2}, {3}, {4})]
            The ordering of the partitions in the list is from coarse 
            (fewer sets and low index values) to fine (more sets at high
            index values).

            Limitations: The Girvan-Newman algorithm is slow, so this
            code won't work for large networks.

            Subtleties: The networkx implmentation of the Girvan-Newman
            algorithm doesn't return the original set of nodes, but that
            is required for the merge algorithm (below) to work. This
            code includes the set of all nodes. 
        """
        all_partitions:list[Tuple[Set[Hashable], ...]] = [(set(G.nodes()),)]
        all_partitions.extend(list(nx.algorithms.community.centrality.girvan_newman(G)))
        return all_partitions
        
    def partitions_to_linkage(self,
                              all_partitions: List[Tuple[Group, ...]]
                            ) -> Tuple[NDArray[np.float64], list[str]]:
        """
        Convert a list of partitions into a linkage matrix. See scipy
        dendrogram and linkage function definitions for the structure of
        the link matrix.
        
        Assumptions:
        • all_partitions is ordered from coarse (few communities) to fine 
            (many communities), with the final partition having each node 
            individually.
        • the difference between partition at index i and index i+1 is
            that one of the groups in partition i has been divided into
            two groups in partition i+1. Thus, each partition only differs
            from the next partition because one set becomes two
        • the first partition (index 0) is the set containing all nodes
        • the last partition (index n-1) is a tuple of sets {0}, {1}, ... {n-1}
        
        The Girvan-Newman method is a divisive process: coarse to fine
        We "invert" the divisive process by processing the partitions in reverse order.
        That is, we start from the finest partition (each node alone) and then
        work backward. In each step we determine which two clusters (from the finer level)
        must have merged to form the cluster at the next coarser level.
        
        The linkage matrix represents the nodes in the dendrogram tree. 
        The first and second columns in the linkage matrix which nodes
        will be merged at the node higher up in the tree. 

        Distance (third column of linkage matrix):
        • use the iteration index (plus 1) as the “distance” for the merge,
        • or use size of the cluster as the "distance" for the merge.
        
        Count (fourth column of linkage matrix):
        The fourth column is set to the size of the merged cluster.
        
        Returns:
        • A linkage matrix Z of shape (n-1, 4) where n is the number of nodes.
        • A set of labels for the leaf nodes of the dendrogram tree
        """
        # The final partition gives the leaves of the dendrogram tree.
        # Find them, count them, and label them
        leaves: Tuple[Group, ...] = all_partitions[-1]
        n: int = len(leaves)
        labels: list[str] = [str(list(leaf)[0]) for leaf in leaves]
        
        # The linkage matrix is formed by merging leaf nodes into larger
        # and larger clusters. The clusters dictionary assigns node numbers
        # to the groups of nodes in each cluster. We need the values of the
        # the cluster dictionary to be hashable, so we represent them
        # as frozensets.
        # We assign the leaf sets to cluster ids 0, 1, ..., n-1.
        clusters: dict[int, FrozenSet[Hashable]] = {i: frozenset([i]) for i in range(n)}
        linkage: list[list[float]] = []
        
        # We will merge fine clusters to coarse structures. 
        # Reverse the partition list so that partitions[0] is the finest 
        # partition (the one with the leaf nodes each in their own group)
        # and partitions[-1] is the coarsest (set of all nodes).
        partitions: list[Tuple[Group, ...]] = list(all_partitions)
        partitions.reverse()
        
        # For each merge step (from fine to coarse) we try to determine which sets to merge.
        # (This assumes that each step in the reversed sequence corresponds to one merge.)
        for i in range(len(partitions)-1):
            fine: Tuple[Group, ...] = partitions[i]      # e.g. a partition with k groups
            coarse: Tuple[Group, ...] = partitions[i+1]  # a partition with k-1 groups
            # In the reverse view, two groups in the fine partition must be
            # merged to form a larger group in the coarse partition
            c1, c2 = self._find_merge(coarse, fine)
            # Look up the node numbers for these two groups in the clusters dictionary
            cid1, cid2 = self._get_ids(c1, c2, clusters)
            if cid1 is None or cid2 is None:
                raise ValueError("No index in cluster dictionary found")
            
            # Group c1 and c2 from the fine partition are merged in the
            # coarse partition. Assign group formed by merging c1 and c2
            # a new index in the clusters dictionary. This defines a new
            # node with index n in the dendrogram tree
            clusters[n] = c1 | c2  

            # The distance column can be done in two ways:
            # Use the number of nodes in the cluster as the distance
            #distance: int = len(clusters[n]) 
            # or use the number of merges performed as the distance
            distance: int = i + 1

            # Set the count column
            count: int = len(clusters[n]) 

            # Add the new row to the linkage matrix
            linkage.append([cid1, cid2, distance, count])       
            
            # increment the counter that tracks the nodes in the dendrogram tree
            n = n + 1

        # The linkage list should have (n-1) rows for n leaves.
        Z = np.array(linkage, dtype=np.float64)
        return Z, labels

    ######################
    ## Helper Functions ##
    ######################
    def _find_merge(self, coarse: Tuple[Group, ...],
                fine:  Tuple[Group, ...]
                ) -> Tuple[FrozenSet[Hashable], FrozenSet[Hashable]]:
        """
            Takes a fine partition and a coarse partition and returns the
            two groups in the fine partition that must be merged to
            create the new group in the coarse partition.

            Assumptions:
            The difference between the fine partition and coarse partition
            is that one of the groups in the coarse partition can be divided
            to form two of the groups in the fine partition. All other
            groups in the two partitions are the same
        """
        for group in coarse:
            # Find all communities in the finer partition that are subsets of this community.
            parts = [c for c in fine if c.issubset(group)]
            # Assumes binary partition used in Girvan Newman
            if len(parts) == 2 and parts[0] | parts[1] == group:
                # These two communities (parts[0] and parts[1]) merged.
                c1, c2 = frozenset(parts[0]), frozenset(parts[1])
                break
        return c1, c2
    
    def _get_ids(self,
                c1: FrozenSet[Hashable], 
                c2: FrozenSet[Hashable], 
                clusters: dict[int, FrozenSet[Hashable]]
                ) -> Tuple[int | None, int| None]:
        """
            Return the index in the clusters dictionary for two groups
            in the values() of the dictionary
        """
        cid1: int | None = None
        cid2: int | None = None
        for cid, cl in clusters.items():
            if cl == c1:
                cid1 = cid
            if cl == c2:
                cid2 = cid
        return cid1, cid2
