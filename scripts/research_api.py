#!/usr/bin/env python3
import argparse,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];FILES={"records":"data/records.json","sources":"data/source-index.json","lineage":"research/source-lineage-register.json","disagreements":"research/disagreement-register.json"}
def rows(k):
 v=json.loads((R/FILES[k]).read_text())
 if isinstance(v,list):return v
 for z in ("records","items","lineages"):
  if isinstance(v.get(z),list):return v[z]
 return [v]
p=argparse.ArgumentParser();p.add_argument("resource",choices=FILES);p.add_argument("--text",default="");p.add_argument("--language");p.add_argument("--limit",type=int,default=50);a=p.parse_args();q=a.text.casefold();x=[v for v in rows(a.resource) if (not q or q in json.dumps(v,ensure_ascii=False).casefold()) and (not a.language or v.get("language")==a.language)][:a.limit];print(json.dumps({"resource":a.resource,"records":x,"boundary":"Source-attributed evidence; partitions, uncertainty and edition dependence remain controlling."},ensure_ascii=False,indent=2))
