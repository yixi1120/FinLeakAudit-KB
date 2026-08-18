import csv, json
from pathlib import Path
p=Path('stage2_delivery/数据线')
j=json.loads((p/'natural_001.json').read_text())
for d in j['documents']:
    if d['source_type'].startswith('SEC_') and 'issuer original-release time' not in d['verification_note']:
        d['verification_note'] += ' original_published_at is null because EDGAR acceptance proves public availability, not a separate issuer original-release time.'
j['open_issues'].append('SEC filings have original_published_at null because their EDGAR acceptance times prove public availability but do not prove a separate issuer original-release time.')
(p/'natural_001.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
fields=['event_id','document_id','company','ticker','prediction_cutoff','retrieval_query','title','source_url','canonical_url','source_type','original_published_at','available_at','revised_at','vendor_indexed_at','timestamp_timezone_basis','timestamp_source_url','retrieved_at','archive_path','content_sha256','license_or_use_note','source_verification_status','verified_by','verification_note']
with (p/'natural_point_in_time_source_ledger_v1.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
 for d in j['documents']: w.writerow({k:j.get(k) if k in j else d.get(k) for k in fields})
