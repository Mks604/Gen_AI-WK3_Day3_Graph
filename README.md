# 🚀 RAG vs GraphRAG Hardware Knowledge System

A **modern AI project demonstrating the difference between Traditional RAG and Knowledge Graph RAG** using hardware technology data such as GPUs, semiconductor processes, and storage systems.

This project combines **Vector Search + Knowledge Graph reasoning + Visualization** in one pipeline.

---

## 📊 Project Overview

This system compares two AI retrieval approaches:

| Method                  | Description                                      |
| ----------------------- | ------------------------------------------------ |
| **Traditional RAG**     | Uses vector embeddings and similarity search     |
| **Knowledge Graph RAG** | Uses graph relationships for multi-hop reasoning |

The project uses hardware examples such as GPUs, semiconductor foundries, and HDD storage devices to demonstrate **enterprise knowledge retrieval systems**.

---

## 🧠 Example Knowledge Domain

The dataset includes information about:

* GPUs
* Semiconductor manufacturing processes
* Foundries
* Storage devices
* Storage manufacturers
* AI datacenter infrastructure

Example entities include companies such as **NVIDIA**, **AMD**, **Intel**, **TSMC**, **Western Digital**, and **Seagate**.

---

## 🏗 System Architecture

```
                User Question
                      │
                      ▼
              Embedding Model
        (Sentence Transformers)
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    Vector Database          Knowledge Graph
        (FAISS)                 (Neo4j)
          │                       │
          ▼                       ▼
   Traditional RAG         GraphRAG Reasoning
          │                       │
          └───────────┬───────────┘
                      ▼
               Result Comparison
                      │
                      ▼
           Visualization + CSV Output
```

---

## 📂 Project Structure

```
rag-graph-demo
│
├── rag_graph_demo.py
├── rag_comparison_results.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Core programming             |
| FAISS                 | Vector similarity search     |
| Neo4j                 | Knowledge graph database     |
| Sentence Transformers | Embedding model              |
| NetworkX              | Graph visualization          |
| Matplotlib            | Charts and graph rendering   |
| Pandas                | Result comparison and export |

---

## 📦 Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/rag-graph-demo.git
cd rag-graph-demo
```

---

### 2️⃣ Install dependencies

```
pip install sentence-transformers
pip install faiss-cpu
pip install neo4j
pip install networkx
pip install matplotlib
pip install pandas
pip install numpy
```

---

### 3️⃣ Start Neo4j with Docker

```
docker run -d \
-p7474:7474 \
-p7687:7687 \
-e NEO4J_AUTH=neo4j/password \
neo4j:5
```

Neo4j browser will be available at:

```
http://localhost:7474
```

Login credentials:

```
Username: neo4j
Password: password
```

---

## ▶️ Run the Project

```
python rag_graph_demo.py
```

Example question:

```
Which GPU uses TSMC manufacturing?
```

---

## 📈 Output

The system produces:

### 1️⃣ Traditional RAG Results

Vector search retrieves the most relevant documents.

### 2️⃣ GraphRAG Results

Multi-hop reasoning from the knowledge graph.

Example reasoning chain:

```
H100 → 5nm → TSMC → AI_Datacenter → HDD → Seagate
```

---

### 3️⃣ Knowledge Graph Visualization

The system automatically displays a graph visualization showing relationships between:

* GPU
* Process
* Foundry
* Storage
* Storage brands

---

### 4️⃣ Comparison Chart

The project generates a comparison chart:

```
Traditional RAG vs GraphRAG
```

---

### 5️⃣ CSV Result File

```
rag_comparison_results.csv
```

Example:

| Question                | Traditional_RAG    | Graph_RAG         |
| ----------------------- | ------------------ | ----------------- |
| Which GPU uses TSMC 5nm | H100 GPU uses TSMC | H100 → 5nm → TSMC |

---

## 🔍 Example Questions

Try asking:

```
Which GPU uses TSMC manufacturing?
```

```
Which companies produce HDD storage?
```

```
Which GPUs use 5nm process?
```

```
What storage devices are produced by Seagate?
```

---

## 🧩 Knowledge Graph Example

Nodes in the graph:

```
GPU
Process
Foundry
System
Storage
StorageBrand
```

Relationships:

```
GPU → USES_PROCESS → Process
Process → MANUFACTURED_BY → Foundry
GPU → USED_IN → System
System → STORES_DATA_ON → Storage
StorageBrand → PRODUCES → Storage
```

---

## 🎯 Why This Project Is Useful

This project demonstrates concepts used in **enterprise AI systems** such as:

* AI knowledge retrieval
* Graph-based reasoning
* Multi-hop question answering
* Hardware knowledge modeling
* AI infrastructure documentation

---

## 📸 Example Visualization

```
H100
 │
USES_PROCESS
 │
5nm
 │
MANUFACTURED_BY
 │
TSMC
 │
USED_IN
 │
AI_Datacenter
 │
STORES_DATA_ON
 │
HDD
 │
PRODUCES
 │
Seagate
```

---




