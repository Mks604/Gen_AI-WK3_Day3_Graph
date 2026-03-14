import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

print("\n===== Hardware RAG vs GraphRAG Demo =====\n")

# ---------------------------------------------------
# Expanded Dataset (GPU + HDD + Semiconductor)
# ---------------------------------------------------

docs = [

"NVIDIA H100 GPU uses TSMC 5nm manufacturing process and is designed for AI datacenter workloads.",
"NVIDIA RTX 4090 graphics card is based on Ada Lovelace architecture and manufactured using TSMC 4nm process.",
"AMD MI300 accelerator uses TSMC 5nm and 6nm chiplets and is designed for high performance computing.",
"AMD Radeon RX 7900 XTX GPU is based on RDNA3 architecture and manufactured using TSMC 5nm process.",
"Intel Xeon processors use Intel 7 process technology and are widely used in enterprise servers.",
"Qualcomm Snapdragon mobile processors are fabricated by TSMC and Samsung foundries.",
"TSMC is the world's largest semiconductor foundry and manufactures chips for NVIDIA, AMD, and Qualcomm.",

"Western Digital produces high capacity HDD drives used for enterprise data storage.",
"Seagate Exos HDD drives provide up to 20TB capacity for hyperscale data centers.",
"Hard Disk Drives store data using magnetic platters and spinning disks.",
"HDD storage devices are commonly used in cloud storage systems and backup infrastructure.",
"Solid State Drives are faster than HDD because they use flash memory instead of spinning disks.",

"NVIDIA GPUs are widely used for AI training, machine learning, and high performance computing workloads.",
"AMD GPUs compete with NVIDIA in gaming graphics cards and AI accelerators.",
"Enterprise HDD drives from Seagate and Western Digital are designed for reliability and large scale storage."
]

# ---------------------------------------------------
# Load Embedding Model
# ---------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = model.encode(docs)

dimension = vectors.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(vectors))

print("Vector database created with", len(docs), "documents")

# ---------------------------------------------------
# Neo4j Connection
# ---------------------------------------------------

driver = GraphDatabase.driver(
    "bolt://127.0.0.1:7687",
    auth=("neo4j","password")
)

# ---------------------------------------------------
# Build Knowledge Graph
# ---------------------------------------------------

def create_graph(tx):

    tx.run("MATCH (n) DETACH DELETE n")

    # GPUs
    tx.run("CREATE (:GPU {name:'H100'})")
    tx.run("CREATE (:GPU {name:'RTX4090'})")
    tx.run("CREATE (:GPU {name:'MI300'})")

    # Processes
    tx.run("CREATE (:Process {name:'5nm'})")
    tx.run("CREATE (:Process {name:'4nm'})")

    # Foundry
    tx.run("CREATE (:Foundry {name:'TSMC'})")

    # System
    tx.run("CREATE (:System {name:'AI_Datacenter'})")

    # Storage
    tx.run("CREATE (:Storage {name:'HDD'})")

    # Storage Brands
    tx.run("CREATE (:StorageBrand {name:'Seagate'})")
    tx.run("CREATE (:StorageBrand {name:'WesternDigital'})")

    # GPU -> Process
    tx.run("""
    MATCH (g:GPU {name:'H100'}),(p:Process {name:'5nm'})
    CREATE (g)-[:USES_PROCESS]->(p)
    """)

    tx.run("""
    MATCH (g:GPU {name:'MI300'}),(p:Process {name:'5nm'})
    CREATE (g)-[:USES_PROCESS]->(p)
    """)

    tx.run("""
    MATCH (g:GPU {name:'RTX4090'}),(p:Process {name:'4nm'})
    CREATE (g)-[:USES_PROCESS]->(p)
    """)

    # Process -> Foundry
    tx.run("""
    MATCH (p:Process {name:'5nm'}),(f:Foundry {name:'TSMC'})
    CREATE (p)-[:MANUFACTURED_BY]->(f)
    """)

    tx.run("""
    MATCH (p:Process {name:'4nm'}),(f:Foundry {name:'TSMC'})
    CREATE (p)-[:MANUFACTURED_BY]->(f)
    """)

    # GPU -> System
    tx.run("""
    MATCH (g:GPU),(s:System {name:'AI_Datacenter'})
    CREATE (g)-[:USED_IN]->(s)
    """)

    # System -> Storage
    tx.run("""
    MATCH (s:System {name:'AI_Datacenter'}),(st:Storage {name:'HDD'})
    CREATE (s)-[:STORES_DATA_ON]->(st)
    """)

    # Storage Brand -> Storage
    tx.run("""
    MATCH (b:StorageBrand {name:'Seagate'}),(s:Storage {name:'HDD'})
    CREATE (b)-[:PRODUCES]->(s)
    """)

    tx.run("""
    MATCH (b:StorageBrand {name:'WesternDigital'}),(s:Storage {name:'HDD'})
    CREATE (b)-[:PRODUCES]->(s)
    """)

with driver.session() as session:
    session.execute_write(create_graph)

print("Knowledge Graph created")

# ---------------------------------------------------
# Ask Question
# ---------------------------------------------------

question = input("\nAsk your question: ")

# ---------------------------------------------------
# Traditional RAG Retrieval
# ---------------------------------------------------

vector = model.encode([question])

D,I = index.search(np.array(vector),3)

trad_results = [docs[i] for i in I[0]]

print("\n----- Traditional RAG Answer -----\n")

for r in trad_results:
    print("-", r)

# ---------------------------------------------------
# Knowledge Graph Query
# ---------------------------------------------------

query = """
MATCH (gpu)-[:USES_PROCESS]->(p)
MATCH (p)-[:MANUFACTURED_BY]->(f)
RETURN gpu.name,p.name,f.name
"""

graph_results=[]
edges=[]

with driver.session() as session:

    result=session.run(query)

    print("\n----- Knowledge Graph RAG Answer -----\n")

    for r in result:

        gpu=r["gpu.name"]
        process=r["p.name"]
        foundry=r["f.name"]

        ans=f"{gpu} -> {process} -> {foundry}"

        print(ans)

        graph_results.append(ans)

        edges.append((gpu,process))
        edges.append((process,foundry))

# ---------------------------------------------------
# Comparison Table
# ---------------------------------------------------

comparison = pd.DataFrame({

"Question":[question],
"Traditional_RAG":[" | ".join(trad_results)],
"Graph_RAG":[" | ".join(graph_results)],
"Traditional_Result_Count":[len(trad_results)],
"Graph_Result_Count":[len(graph_results)]

})

print("\n===== RAG Comparison Table =====\n")

print(comparison)

# ---------------------------------------------------
# Save Comparison File
# ---------------------------------------------------

comparison.to_csv("rag_comparison_results.csv",index=False)

print("\nCSV saved: rag_comparison_results.csv")

# ---------------------------------------------------
# Knowledge Graph Visualization
# ---------------------------------------------------

G = nx.DiGraph()

for e in edges:
    G.add_edge(e[0],e[1])

plt.figure(figsize=(8,6))

pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color="lightblue",
    font_weight="bold",
    arrows=True
)

plt.title("Knowledge Graph Visualization")

plt.show()

# ---------------------------------------------------
# Comparison Chart
# ---------------------------------------------------

methods = ["Traditional RAG","Graph RAG"]

counts = [len(trad_results),len(graph_results)]

plt.figure()

plt.bar(methods,counts)

plt.title("RAG vs GraphRAG Result Comparison")

plt.xlabel("Method")

plt.ylabel("Number of Results")

plt.show()

print("\nVisualization complete")