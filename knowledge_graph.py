import spacy
import networkx as nx
from collections import defaultdict

class KnowledgeGraphBuilder:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.graph = nx.DiGraph()

    def extract_triples(self, text):
        """
        Extract Subject -> Relation -> Object triples
        """
        doc = self.nlp(text)

        triples = []

        for sent in doc.sents:

            subject = None
            relation = None
            obj = None

            for token in sent:

                if "subj" in token.dep_:
                    subject = token.text

                if token.pos_ == "VERB":
                    relation = token.lemma_

                if "obj" in token.dep_:
                    obj = token.text

            if subject and relation and obj:
                triples.append(
                    (subject, relation, obj)
                )

        return triples

    def build_graph(self, text):

        triples = self.extract_triples(text)

        for subject, relation, obj in triples:

            self.graph.add_node(subject)
            self.graph.add_node(obj)

            self.graph.add_edge(
                subject,
                obj,
                relation=relation
            )

        return triples

    def get_graph(self):
        return self.graph

    def get_neighbors(self, node):

        if node not in self.graph:
            return []

        neighbors = []

        for target in self.graph.successors(node):

            relation = self.graph[node][target]["relation"]

            neighbors.append({
                "source": node,
                "relation": relation,
                "target": target
            })

        return neighbors

    def graph_summary(self):

        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges()
        }
