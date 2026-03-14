import faiss
import numpy as np
import sys

sys.path.append("..")

from embeddings.embedder import get_embeddings

with open("../data/semiconductor_docs.txt") as f:
    docs=[line.strip() for line in f if line.strip()]

index=faiss.read_index("semiconductor.index")

query=input("Enter question: ")

vector=get_embeddings([query])

D,I=index.search(np.array(vector),3)

print("\nResults\n")

for i in I[0]:
    print(docs[i])