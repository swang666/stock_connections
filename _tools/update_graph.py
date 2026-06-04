#!/usr/bin/env python3
"""Regenerate everything derived from the live spreadsheet:
  1. AI Supply Chain Graph.html   -- interactive graph (catalyst + bottleneck modes)
  2. 00 - START HERE.md           -- the layer index (kept in sync with the node list)
  3. Degree (analytics) sheet     -- out/in/total degree per node

Bottleneck scores are computed in Python (bottleneck_analysis.py) and baked into node data so the
graph and the scoring engine never diverge. Run after any ingestion / manual edit."""
import os, json, sys, re
from collections import defaultdict
from openpyxl import load_workbook
HERE = os.path.dirname(os.path.abspath(__file__)); VAULT = os.path.dirname(HERE)
sys.path.insert(0, VAULT)
import bottleneck_analysis as ba
XLSX = os.environ.get("STOCKKB_XLSX", os.path.join(VAULT, "AI-Supply-Chain-Network.xlsx"))
TMPL = os.path.join(HERE, "graph_template_v3.html")
LAYERS = {1:"EDA & IP",2:"Semiconductor Equipment",3:"Foundry / Manufacturing",
 4:"Chip Designers (Accelerators/Networking)",5:"Memory (HBM/DRAM)",6:"Advanced Packaging / OSAT",
 7:"Optical & Interconnect",8:"Networking Systems",9:"Servers & ODM/OEM",10:"Hyperscalers / Cloud",
 11:"AI Labs / Model Developers",12:"Datacenter Infrastructure (REITs)",13:"Power & Cooling Equipment",
 14:"Power Generation / Utilities",0:"Demand Driver / Theme"}
LAYER_COLOR = {1:"7c3aed",2:"6d28d9",3:"2563eb",4:"059669",5:"0891b2",6:"0d9488",7:"0284c7",
 8:"4f46e5",9:"d97706",10:"dc2626",11:"db2777",12:"9333ea",13:"ea580c",14:"ca8a04",0:"475569"}

# ---------- read live data ----------
wb = load_workbook(XLSX, data_only=True, read_only=True)
nodes=[]
for r in wb["Nodes"].iter_rows(min_row=2, values_only=True):
    if not r or not r[0]: continue
    nodes.append({"id":r[0],"name":r[1],"type":r[2],"ticker":r[3] or "","layer":r[4],
                  "layer_name":r[5],"segment":r[6] or "","role":r[9] or ""})
edges=[]
for r in wb["Edges"].iter_rows(min_row=2, values_only=True):
    if not r or not r[0]: continue
    edges.append({"s":r[0],"r":r[2],"t":r[3],"w":r[5] if isinstance(r[5],(int,float)) else 2})
wb.close()

# ---------- 1) interactive graph ----------
bn, be = ba.load(); rows = ba.analyze(bn, be); S = {x["id"]: x for x in rows}
for nd in nodes:
    x = S.get(nd["id"])
    if x:
        nd.update({"bscore":x["score"],"breach":x["reach"],"balts":x["alts"],
                   "bconstr":x["constraint"],"bwhy":x["why"],"bemerging":bool(x["emerging"])})
    else:
        nd.update({"bscore":0,"breach":0,"balts":0,"bconstr":0,"bwhy":"","bemerging":False})
lcolor={str(k):"#"+v for k,v in LAYER_COLOR.items()}; lname={str(k):v for k,v in LAYERS.items()}
tmpl=open(TMPL,encoding="utf-8").read()
out=(tmpl.replace("/*NODES*/","NODES = "+json.dumps(nodes))
        .replace("/*EDGES*/","EDGES = "+json.dumps(edges))
        .replace("/*LCOLOR*/","LCOLOR = "+json.dumps(lcolor))
        .replace("/*LNAME*/","LNAME = "+json.dumps(lname)))
open(os.path.join(VAULT,"AI Supply Chain Graph.html"),"w",encoding="utf-8").write(out)
# also publish a copy as index.html at the repo root so GitHub Pages serves it at the site root
# (share link becomes https://<user>.github.io/<repo>/ with no %20-escaped filename).
open(os.path.join(VAULT,"index.html"),"w",encoding="utf-8").write(out)

# ---------- 2) regenerate START HERE layer index ----------
by_layer=defaultdict(list)
for nd in nodes:
    by_layer[nd["layer"]].append(nd["name"])
def links(names): return ", ".join(f"[[{n}]]" for n in sorted(names))
idx=["## Layers (upstream → downstream)",""]
for L in range(1,15):
    if by_layer.get(L):
        idx.append(f"**L{L} — {LAYERS[L]}**"); idx.append(links(by_layer[L])); idx.append("")
idx.append("## Demand drivers (themes)")
idx.append(links(by_layer.get(0,[])) or "_none_"); idx.append("")
SH=os.path.join(VAULT,"00 - START HERE.md")
txt=open(SH,encoding="utf-8").read()
marker="## Layers (upstream → downstream)"
head=txt.split(marker)[0].rstrip()+"\n\n"
open(SH,"w",encoding="utf-8").write(head+"\n".join(idx).rstrip()+"\n")

# ---------- 3) populate Degree (analytics) sheet ----------
outd=defaultdict(int); ind=defaultdict(int)
for e in edges:
    outd[e["s"]]+=1; ind[e["t"]]+=1
id2name={nd["id"]:nd["name"] for nd in nodes}; id2layer={nd["id"]:nd["layer_name"] for nd in nodes}
wb2=load_workbook(XLSX)            # write mode
if "Degree (analytics)" in wb2.sheetnames:
    ws=wb2["Degree (analytics)"]; wb2.remove(ws)
ws=wb2.create_sheet("Degree (analytics)")
ws.append(["node_id","name","layer_name","out_degree","in_degree","total_connections"])
for nd in sorted(nodes, key=lambda n:-(outd[n["id"]]+ind[n["id"]])):
    i=nd["id"]; ws.append([i,id2name[i],id2layer[i],outd[i],ind[i],outd[i]+ind[i]])
wb2.save(XLSX)

print(f"regenerated: graph ({len(nodes)} nodes, {len(edges)} edges, bottleneck baked) | "
      f"START HERE index ({sum(1 for L in range(1,15) if by_layer.get(L))} layers, {len(by_layer.get(0,[]))} themes) | "
      f"Degree sheet ({len(nodes)} rows)")
