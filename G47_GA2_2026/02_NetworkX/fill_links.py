# fill_links.py - G47: fills capacity, cost and delay from link_class
import csv, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
CAP = {"core": 200, "backup": 140, "bottleneck": 120}   # Mbps, from the G47 sheet
COST = {"core": 20, "backup": 40, "bottleneck": 20}    # cost profile C3
REGION = {"CHA", "ANN", "PIT", "ITH"}                  # assumption: region links count as edge links

def km(a, b):  # haversine great-circle distance
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))

pos = {}
with open(DATA / "nodes.csv", newline="") as f:
    for r in csv.DictReader(f):
        pos[r["node"]] = (float(r["lon"]), float(r["lat"]))

rows = list(csv.DictReader(open(DATA / "links.csv", newline="")))
for r in rows:
    c = (r["link_class"] or "").strip().lower() or "core"   # a blank cell counts as core
    assert c in CAP, f"link_class must be core, backup or bottleneck on {r['u']}-{r['v']}, not '{c}'"
    r["link_class"] = c
    lo, hi = (4, 10) if {r["u"], r["v"]} <= REGION else (8, 23)
    delay = km(pos[r["u"]], pos[r["v"]]) / 200          # about 200 km per ms in fibre
    r["capacity_mbps"] = CAP[c]
    r["cost"] = COST[c]
    r["delay_ms"] = round(min(hi, max(lo, delay)), 1)

with open(DATA / "links.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("links.csv filled")