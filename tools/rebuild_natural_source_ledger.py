#!/usr/bin/env python3
"""Deterministically rebuild the combined ledger from the event manifests."""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'数据线'
FIELDS=['event_id','document_id','company','ticker','prediction_cutoff','retrieval_query','title','source_url','canonical_url','source_type','original_published_at','available_at','revised_at','vendor_indexed_at','timestamp_timezone_basis','timestamp_source_url','retrieved_at','archive_path','content_sha256','license_or_use_note','source_verification_status','verified_by','verification_note']
def main():
 rows=[]
 for p in sorted(DATA.glob('natural_0[0-9][0-9].json')):
  d=json.loads(p.read_text())
  for doc in d['documents']:
   rows.append({'event_id':d['event_id'],'company':d['company'],'ticker':d['ticker'],'prediction_cutoff':d['prediction_cutoff'],'retrieval_query':d['retrieval_query'],**doc})
 with (DATA/'natural_point_in_time_source_ledger_v1.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore');w.writeheader();w.writerows(rows)
if __name__=='__main__':main()
