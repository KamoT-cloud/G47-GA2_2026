import csv
import networkx as nx
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

G = nx.Graph()  # undirected: each link is bidirectional; say so in the report
with open(DATA / "nodes.csv", newline="") as f:
    for r in csv.DictReader(f):
        G.add_node(r["node"], name=r["name"], pos=(float(r["lon"]), float(r["lat"])))
with open(DATA / "links.csv", newline="") as f:
    for r in csv.DictReader(f):
        G.add_edge(r["u"], r["v"],
                   capacity_mbps=float(r["capacity_mbps"]),
                   cost=int(r["cost"]),
                   delay_ms=float(r["delay_ms"]),
                   link_class=r["link_class"])

print(G.number_of_nodes(), G.number_of_edges(), nx.is_connected(G))
print("Bridges:", list(nx.bridges(G)))
print("Articulation points:", list(nx.articulation_points(G)))
for u, v, d in G.edges(data=True):
    print(u, v, d)