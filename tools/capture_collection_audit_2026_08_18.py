#!/usr/bin/env python3
"""Append raw SEC API inputs and an honest collection-audit manifest."""
import hashlib, json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'raw/collection_audit/2026-08-18'
CIKS=['0001045810','0000320187','0000829224','0000050863','0000034088','0000927628','0000789019','0000731766','0001158463']
def sec_user_agent():
 value=os.environ.get('FINLEAKAUDIT_SEC_USER_AGENT','').strip()
 if not value:raise RuntimeError('Set FINLEAKAUDIT_SEC_USER_AGENT to a project name and real contact email')
 return value
def add(path,b):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists() and path.read_bytes()!=b: raise RuntimeError(f'immutable raw collision: {path}')
 if not path.exists(): path.write_bytes(b)
 return hashlib.sha256(b).hexdigest()
def main():
 rows=[]
 for cik in CIKS:
  url=f'https://data.sec.gov/submissions/CIK{cik}.json'
  req=urllib.request.Request(url,headers={'User-Agent':sec_user_agent()})
  with urllib.request.urlopen(req,timeout=60) as r: b=r.read()
  rel=f'raw/collection_audit/2026-08-18/sec_submissions/CIK{cik}.json'
  rows.append({'url':url,'archive_path':rel,'sha256':add(ROOT/rel,b)})
 manifest={
  'record_type':'collection_audit',
  'created_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),
  'collector':'tools/build_natural_002_010_sec_primary.py',
  'search_engine_or_api':'SEC EDGAR submissions JSON API (data.sec.gov)',
  'request_method':'Direct issuer CIK submissions endpoints, then direct SEC Archives primary-document URLs. No web search engine or SERP API was used for natural_002–010.',
  'raw_ranking_preserved':False,
  'ranking_explanation':'The SEC submissions API is an issuer filing feed ordered by the SEC. The collector preserved the raw feed snapshots but did not preserve a search-engine result ranking because no search engine was queried.',
  'natural_001_historic_search_record':'Not recoverable: the original 2026-08-06 to 2026-08-07 collection did not retain search request payloads, SERPs, screenshots, browser history, or an Agent-chat export. This file does not reconstruct or claim those missing records.',
  'excluded_results_record':'No structured external-search exclusion log exists. The current collection did not discard external search results because it used direct SEC endpoints only.',
  'sec_submission_inputs':rows,
  'unavailable_raw_materials':['original web-search SERPs/rankings','browser-history export','collection-time screenshots','Agent conversation/tool transcript export']
 }
 b=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
 add(ROOT/'raw/collection_audit/2026-08-18/collection_audit_manifest.json',b)
if __name__=='__main__': main()
