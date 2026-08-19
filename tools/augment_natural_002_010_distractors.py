#!/usr/bin/env python3
"""Append SEC form-type-diverse candidate sources without changing raw files."""
import csv, hashlib, json, time, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'数据线'; UA='FinLeakAudit-KB research contact@example.com'
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=90) as r:return r.read()
def iso(v):return v.replace('.000Z','+00:00').replace('Z','+00:00')
def main():
 ledger=DATA/'natural_point_in_time_source_ledger_v1.csv'; ledger_rows=list(csv.DictReader(ledger.open())); fields=list(ledger_rows[0])
 added=[]
 for manifest_path in sorted(DATA.glob('natural_0[0-9][0-9].json')):
  d=json.loads(manifest_path.read_text()); eid=d['event_id']
  if eid=='natural_001':continue
  if len(d['documents']) >= 18:
   continue
  cutoff=datetime.fromisoformat(d['prediction_cutoff']).astimezone(timezone.utc); cik={'natural_002':'0001045810','natural_003':'0000320187','natural_004':'0000829224','natural_005':'0000050863','natural_006':'0000034088','natural_007':'0000927628','natural_008':'0000789019','natural_009':'0000731766','natural_010':'0001158463'}[eid]
  feed=json.loads(get(f'https://data.sec.gov/submissions/CIK{cik}.json')); r=feed['filings']['recent']; used={x['source_url'] for x in d['documents']}; candidates=[]
  for i, acc in enumerate(r['acceptanceDateTime']):
   form=r['form'][i]; primary=r['primaryDocument'][i]
   when=datetime.fromisoformat(iso(acc))
   if form not in {'10-Q','10-K','DEF 14A','DEFA14A','4','144','SC 13G/A','13F-HR'} or not primary or not cutoff-timedelta(days=90)<=when<=cutoff+timedelta(days=90): continue
   no=r['accessionNumber'][i]; url=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{no.replace("-","")}/{primary}'
   if url in used: continue
   candidates.append((i,when))
  # Stable selection spanning types/time: two financial/proxy records plus up
  # to six ownership/sale records are deliberate query-adjacent distractors.
  priority={'10-Q':0,'10-K':1,'DEF 14A':2,'DEFA14A':3,'SC 13G/A':4,'13F-HR':5,'4':6,'144':7}
  candidates.sort(key=lambda x:(priority[r['form'][x[0]]],abs((x[1]-cutoff).total_seconds())))
  selected=[]; forms=set()
  for i,when in candidates:
   if r['form'][i] not in forms or len(selected)<8:
    selected.append(i);forms.add(r['form'][i])
   if len(selected)==8:break
  if len(selected)<8: raise RuntimeError(f'{eid}: insufficient diverse distractors ({len(selected)})')
  start=len(d['documents'])
  unit_path=DATA/f'{eid}_retrieval_units_v1.csv'; units=list(csv.DictReader(unit_path.open())); unitfields=list(units[0])
  for n,i in enumerate(selected,1):
   seq=start+n; did=f'{eid}_doc_{seq:03d}'; acc=r['acceptanceDateTime'][i]; no=r['accessionNumber'][i]; primary=r['primaryDocument'][i]; form=r['form'][i]; desc=(r['primaryDocDescription'][i] or primary).strip(); url=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{no.replace("-","")}/{primary}'; header=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{no.replace("-","")}/{no}-index-headers.html'; data=get(url); ext=Path(primary).suffix or '.html'; rel=f'raw/{eid}/{did}{ext}'; p=ROOT/rel
   if p.exists() and p.read_bytes()!=data:raise RuntimeError('immutable raw collision')
   if not p.exists():p.write_bytes(data)
   h=hashlib.sha256(data).hexdigest(); retrieved=datetime.now(timezone.utc).isoformat(timespec='seconds'); role='query_adjacent_distractor' if form in {'4','144','SC 13G/A','13F-HR'} else 'financial_or_governance_context_candidate'
   doc={'document_id':did,'title':f'SEC {form} — {desc}','text':f'SEC filing metadata: Form {form}. {desc}','text_status':'verbatim_or_source_grounded_extract','source_url':url,'canonical_url':url,'source_type':f'SEC_EDGAR_{form.replace("/","_")}','original_published_at':None,'available_at':iso(acc),'revised_at':None,'vendor_indexed_at':None,'timestamp_timezone_basis':'SEC EDGAR acceptance time supplied in UTC by the SEC submissions feed.','timestamp_source_url':header,'retrieved_at':retrieved,'archive_path':rel,'content_sha256':h,'license_or_use_note':'Public SEC-hosted issuer filing; no separate license identified; retained only as a research snapshot.','source_verification_status':'verified','verified_by':'data_line_initial_verification_2026-08-18','verification_note':f'Added as {role}; SEC submissions metadata and primary document were retrieved directly. This candidate role is a collection-coverage label, not a relevance score or a top-k decision. original_published_at is null because SEC acceptance proves public availability, not a separate issuer-release time.'}
   d['documents'].append(doc); added.append({'event_id':eid,'company':d['company'],'ticker':d['ticker'],'prediction_cutoff':d['prediction_cutoff'],'retrieval_query':d['retrieval_query'],**doc}); units.append({'retrieval_unit_id':did,'parent_document_id':did,'unit_type':'primary_source_snapshot','title':doc['title'],'source_type':doc['source_type'],'available_at':doc['available_at'],'revised_at':'','canonical_url':url,'timestamp_source_url':header,'retrieval_text_archive_path':rel,'retrieval_text_sha256':h,'extraction_id':'','historical_snapshot_status':'not_applicable_primary_source_snapshot','ingest_status':'active','notes':f'Use primary source snapshot; {role}; no top-k decision.'}); time.sleep(.12)
  manifest_path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  with unit_path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=unitfields);w.writeheader();w.writerows(units)
 with ledger.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(ledger_rows);w.writerows(added)
if __name__=='__main__':main()
