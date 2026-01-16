import unittest

import numpy as np
import networkx as nx

from SLPA import find_communities


class TestSLPA(unittest.TestCase):
    def _build_graph(self, edges, isolated_nodes=None):
        G = nx.Graph()
        if isolated_nodes:
            G.add_nodes_from(isolated_nodes)
        for u, v in edges:
            G.add_edge(u, v, weight=1.0)
        return G

    def test_isolated_node_community(self):
        np.random.seed(7)
        G = self._build_graph([(1, 2)], isolated_nodes=[3])
        communities = find_communities(G, T=3, r=0.5)
        self.assertIn(3, communities)
        self.assertEqual(communities[3], {3})

    def test_nodes_partitioned_once(self):
        np.random.seed(21)
        G = self._build_graph([(0, 1), (1, 2), (2, 3), (3, 4)])
        communities = find_communities(G, T=4, r=0.2)
        all_nodes = [node for community in communities.values() for node in community]
        self.assertEqual(set(all_nodes), set(G.nodes()))
        self.assertEqual(len(all_nodes), len(set(all_nodes)))

    def test_deterministic_with_seed(self):
        G = self._build_graph([(0, 1), (1, 2), (2, 0)])
        np.random.seed(123)
        first = find_communities(G, T=2, r=0.1)
        np.random.seed(123)
        second = find_communities(G, T=2, r=0.1)
        self.assertEqual(first, second)

    def test_zero_iterations_returns_self_labels(self):
        np.random.seed(9)
        G = self._build_graph([(0, 1), (1, 2)])
        communities = find_communities(G, T=0, r=0.1)
        self.assertEqual(set(communities.keys()), set(G.nodes()))
        for node in G.nodes():
            self.assertEqual(communities[node], {node})


if __name__ == "__main__":
    unittest.main()
