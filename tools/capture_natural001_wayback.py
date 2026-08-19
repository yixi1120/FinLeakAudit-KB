#!/usr/bin/env python3
"""Append 2024 Wayback captures/body extracts for the six blocked web sources.

Capture time is evidence that a particular page version was publicly retrievable
by that time; it is deliberately *not* substituted for first-publication time.
The existing blocked retrieval units therefore remain blocked pending a
document-specific earliest-availability verifier.
"""
import csv, gzip, hashlib, io, json, os, re, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'raw/natural_001/historical'
OUT=ROOT/'数据线/natural_001_historical_capture_ledger_v1.csv'
UA=os.environ.get('FINLEAKAUDIT_HTTP_USER_AGENT','FinLeakAudit-KB/1.0 (+https://github.com/yixi1120/FinLeakAudit-KB)')
SPECS={
 'natural_001_doc_015':('https://techcrunch.com/2024/07/19/what-we-know-about-crowdstrikes-update-fail-thats-causing-global-outages-and-travel-chaos/','//*[contains(concat(" ", normalize-space(@class), " "), " wp-block-post-content ")]'),
 'natural_001_doc_016':('https://www.crowdstrike.com/en-us/blog/to-our-customers-and-partners/','//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]'),
 'natural_001_doc_018':('https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/','//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]'),
 'natural_001_doc_019':('https://www.crowdstrike.com/en-us/blog/channel-file-291-rca-available/','//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]'),
 'natural_001_doc_020':('https://www.crowdstrike.com/en-us/blog/crowdstrike-unifies-threat-data-and-ai-for-mdr/','//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]'),
 'natural_001_doc_021':('https://www.techtarget.com/cybersecurity/news/366596579/CrowdStrike-Content-validation-bug-led-to-global-outage','//section[@id="content-body"]/p[not(descendant::i)][not(starts-with(normalize-space(.), "UPDATE:"))]'),
}
def load(url, binary=False):
 req=urllib.request.Request(url,headers={'User-Agent':UA})
 with urllib.request.urlopen(req,timeout=90) as r: return r.read()
def clean(n):
 for u in n.xpath('.//script|.//style|.//noscript'): u.drop_tree()
 return re.sub(r'\s+',' ',' '.join(n.xpath('.//text()'))).strip()
def addonly(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists() and path.read_bytes()!=data: raise RuntimeError(f'immutable raw collision: {path}')
 if not path.exists(): path.write_bytes(data)
 return hashlib.sha256(data).hexdigest()
def main():
 rows=[]
 selected = set(sys.argv[1:])
 for doc,(url,xpath) in SPECS.items():
  if selected and doc not in selected:
   continue
  # The initial direct retrieval may already have saved a capture before a
  # later CDX request times out. Re-register that immutable artifact instead
  # of redownloading it.
  known = {'natural_001_doc_015': '20240719170555'}
  known_raw = RAW/f'{doc}_wayback_{known[doc]}.html' if doc in known else None
  if known_raw and known_raw.exists():
   ts = known[doc]
   capture = f'https://web.archive.org/web/{ts}id_/{url}'
   payload = known_raw.read_bytes()
   raw_rel = f'raw/natural_001/historical/{known_raw.name}'
   h = hashlib.sha256(payload).hexdigest()
   tree=html.fromstring(payload); nodes=tree.xpath(xpath); text='\n\n'.join(clean(n) for n in nodes if clean(n))
   text_rel=f'raw/natural_001/extracted/{doc}_wayback_{ts}_body.txt'
   th=addonly(ROOT/text_rel,(text+'\n').encode())
   rows.append({'document_id':doc,'capture_url':capture,'capture_timestamp_utc':datetime.strptime(ts,'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc).isoformat(),'capture_archive_path':raw_rel,'capture_sha256':h,'extracted_text_archive_path':text_rel,'extracted_text_sha256':th,'extraction_method':'lxml HTML parser; selected editorial content XPath; removed script/style/noscript; collapsed whitespace.','status':'historical_capture_saved_not_first_availability_proof','note':'Capture timestamp proves this page version was retrievable by that instant, but does not prove first publication/availability. Do not activate existing blocked unit without resolving earliest availability and any version conflict.'})
   continue
  q='https://web.archive.org/cdx/search/cdx?'+urllib.parse.urlencode({'url':url,'output':'json','filter':'statuscode:200','fl':'timestamp,original,statuscode,digest','filter':'timestamp:2024','collapse':'digest'})
  data=json.loads(load(q).decode())
  if len(data)<2:
   rows.append({'document_id':doc,'capture_url':'','capture_timestamp_utc':'','capture_archive_path':'','capture_sha256':'','extracted_text_archive_path':'','extracted_text_sha256':'','extraction_method':'','status':'no_2024_capture_found','note':'Wayback CDX request returned no 2024 HTTP-200 capture; source remains blocked.'})
   continue
  ts=data[1][0]
  capture=f'https://web.archive.org/web/{ts}id_/{url}'
  payload=load(capture)
  if payload[:2]==b'\x1f\x8b': payload=gzip.GzipFile(fileobj=io.BytesIO(payload)).read()
  raw_rel=f'raw/natural_001/historical/{doc}_wayback_{ts}.html'
  h=addonly(ROOT/raw_rel,payload)
  tree=html.fromstring(payload)
  nodes=tree.xpath(xpath)
  text='\n\n'.join(clean(n) for n in nodes if clean(n))
  if not text:
   rows.append({'document_id':doc,'capture_url':capture,'capture_timestamp_utc':datetime.strptime(ts,'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc).isoformat(),'capture_archive_path':raw_rel,'capture_sha256':h,'extracted_text_archive_path':'','extracted_text_sha256':'','extraction_method':'xpath selected no editorial body','status':'capture_saved_body_not_found','note':'Historical page capture retained but body selector found no editorial text; source remains blocked.'})
   continue
  text_rel=f'raw/natural_001/extracted/{doc}_wayback_{ts}_body.txt'
  th=addonly(ROOT/text_rel,(text+'\n').encode())
  rows.append({'document_id':doc,'capture_url':capture,'capture_timestamp_utc':datetime.strptime(ts,'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc).isoformat(),'capture_archive_path':raw_rel,'capture_sha256':h,'extracted_text_archive_path':text_rel,'extracted_text_sha256':th,'extraction_method':'lxml HTML parser; selected editorial content XPath; removed script/style/noscript; collapsed whitespace.','status':'historical_capture_saved_not_first_availability_proof','note':'Capture timestamp proves this page version was retrievable by that instant, but does not prove first publication/availability. Do not activate existing blocked unit without resolving earliest availability and any version conflict.'})
 existing = {}
 if OUT.exists():
  with OUT.open(newline='') as f:
   existing = {row['document_id']: row for row in csv.DictReader(f)}
 for row in rows:
  existing[row['document_id']] = row
 fields = list(rows[0])
 with OUT.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(existing[k] for k in sorted(existing))
if __name__=='__main__': main()
