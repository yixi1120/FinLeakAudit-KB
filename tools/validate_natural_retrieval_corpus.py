#!/usr/bin/env python3
"""Engineering handoff validator for Natural Point-in-Time candidate corpora.

It is deliberately a validator, not a retriever: it resolves only retrieval
units explicitly marked `active`, verifies their immutable local bytes, and
rejects blocked/superseded/unknown units.  It never computes relevance or top-k.
"""
import csv, hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'数据线'
FORBIDDEN_CURRENT_WEB_SNAPSHOTS={
    'raw/natural_001/natural_001_doc_015.html',
    'raw/natural_001/natural_001_doc_016.html',
    'raw/natural_001/natural_001_doc_018.html',
    'raw/natural_001/natural_001_doc_019.html',
    'raw/natural_001/natural_001_doc_020.html',
    'raw/natural_001/natural_001_doc_021.html',
}
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 errors=[]; active=[]; event_docs={}
 manifests=sorted(DATA.glob('natural_0[0-9][0-9].json'))
 if len(manifests)!=10: errors.append(f'expected exactly 10 event manifests, found {len(manifests)}')
 for p in manifests:
  d=json.loads(p.read_text()); event_id=d['event_id']; cutoff=d['prediction_cutoff']
  if not cutoff or not d['retrieval_query']: errors.append(f'{event_id}: missing frozen cutoff/query')
  if not 8<=len(d['documents'])<=20: errors.append(f'{event_id}: document count outside 8–20')
  event_docs[event_id]={x['document_id']:x for x in d['documents']}
  units_path=DATA/f'{event_id}_retrieval_units_v1.csv'
  if not units_path.exists(): errors.append(f'{event_id}: missing retrieval-unit ledger'); continue
  units=list(csv.DictReader(units_path.open()))
  ids=[u['retrieval_unit_id'] for u in units]
  if len(ids)!=len(set(ids)): errors.append(f'{event_id}: duplicate retrieval unit IDs')
  for u in units:
   status=u['ingest_status']
   if status != 'active': continue
   if u['retrieval_text_archive_path'] in FORBIDDEN_CURRENT_WEB_SNAPSHOTS:
    errors.append(f"{u['retrieval_unit_id']}: current full-page web snapshot is forbidden from ingestion")
    continue
   if not u['available_at']: errors.append(f"{u['retrieval_unit_id']}: active unit has null available_at"); continue
   pth=ROOT/u['retrieval_text_archive_path']
   if not pth.exists(): errors.append(f"{u['retrieval_unit_id']}: missing raw path {pth}"); continue
   if digest(pth)!=u['retrieval_text_sha256']: errors.append(f"{u['retrieval_unit_id']}: hash mismatch")
   active.append({'event_id':event_id,'retrieval_unit_id':u['retrieval_unit_id'],'parent_document_id':u['parent_document_id'],'available_at':u['available_at'],'path':u['retrieval_text_archive_path'],'sha256':u['retrieval_text_sha256']})
 # Candidate source coverage is measured at source grain, while a status page
 # may legally expand into multiple timestamped units.
 categories=set(json.loads(p.read_text()).get('event_category') for p in manifests)
 required={'earnings_guidance','regulatory_litigation','product_cybersecurity_incident','management','management_financing_ma'}
 if not {'earnings_guidance','regulatory_litigation','product_cybersecurity_incident'}.issubset(categories) or not ({'management','management_financing_ma'} & categories): errors.append('event categories do not cover protocol minimum')
 report={'validator':'validate_natural_retrieval_corpus.py','event_manifests':len(manifests),'active_retrieval_units':len(active),'errors':errors,'active_units':active}
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 1 if errors else 0
if __name__=='__main__': sys.exit(main())
