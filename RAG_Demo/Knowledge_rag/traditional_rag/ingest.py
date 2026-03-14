import faiss
import numpy as np
import sys

sys.path.append("..")

from embeddings.embedder import get_embeddings

with open("../data/semiconductor_docs.txt","r") as f:
    docs=[line.strip() for line in f if line.strip()]

vectors=get_embeddings(docs)

dimension=vectors.shape[1]

index=faiss.IndexFlatL2(dimension)

index.add(np.array(vectors))

faiss.write_index(index,"semiconductor.index")

print("Vector database created")