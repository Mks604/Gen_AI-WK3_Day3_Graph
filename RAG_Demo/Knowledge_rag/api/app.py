from fastapi import FastAPI
import faiss
import numpy as np
import sys

sys.path.append("..")

from embeddings.embedder import get_embeddings

app=FastAPI()

with open("../data/semiconductor_docs.txt") as f:
    docs=[line.strip() for line in f if line.strip()]

index=faiss.read_index("../traditional_rag/semiconductor.index")

@app.get("/query")

def ask(question:str):

    vector=get_embeddings([question])

    D,I=index.search(np.array(vector),3)

    result=[docs[i] for i in I[0]]

    return {"answer":result}