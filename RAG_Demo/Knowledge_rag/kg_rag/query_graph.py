from neo4j import GraphDatabase

uri="bolt://localhost:7474"
user="neo4j"
password="knowledge_graph_demo_2024"

driver=GraphDatabase.driver(uri,auth=(user,password))

query="""
MATCH (gpu)-[:USES_PROCESS]->(p {name:'5nm'})
MATCH (p)-[:MANUFACTURED_BY]->(f {name:'TSMC'})
RETURN gpu.name
"""

with driver.session() as session:

    result=session.run(query)

    print("\nGPUs using TSMC 5nm\n")

    for r in result:
        print(r["gpu.name"])