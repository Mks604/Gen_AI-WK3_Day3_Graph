from neo4j import GraphDatabase

uri="bolt://localhost:7474"
user="neo4j"
password="knowledge_graph_demo_2024"

driver=GraphDatabase.driver(uri,auth=(user,password))

def create_graph(tx):

    tx.run("CREATE (:GPU {name:'H100'})")
    tx.run("CREATE (:GPU {name:'MI300'})")

    tx.run("CREATE (:Process {name:'5nm'})")
    tx.run("CREATE (:Foundry {name:'TSMC'})")

    tx.run("""
    MATCH (g:GPU {name:'H100'}),(p:Process {name:'5nm'})
    CREATE (g)-[:USES_PROCESS]->(p)
    """)

    tx.run("""
    MATCH (g:GPU {name:'MI300'}),(p:Process {name:'5nm'})
    CREATE (g)-[:USES_PROCESS]->(p)
    """)

    tx.run("""
    MATCH (p:Process {name:'5nm'}),(f:Foundry {name:'TSMC'})
    CREATE (p)-[:MANUFACTURED_BY]->(f)
    """)

with driver.session() as session:
    session.execute_write(create_graph)

print("Graph created successfully")