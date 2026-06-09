from rank_bm25 import BM25Okapi
import numpy as np

class Rank:
    def __init__(self):
        pass

    def rank(self, corpus: list, query:str):
        rankings = {}

        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)
        
        tokenized_query = query.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)

        sorted_indices = np.argsort(doc_scores)[::-1]
        for s in sorted_indices:
            rankings[corpus[s]] = round(float(doc_scores[s]), 3)

        return rankings

corpus = [
    "apple pie recipe baking apples",
    "apple apple apple apple apple banana fruit",
    "how to bake a perfect apple pie for autumn holidays with cinnamon and crust"
]