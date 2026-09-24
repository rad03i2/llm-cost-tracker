from decimal import Decimal
import csv
import pytest
from llm_cost_tracker import Price, append_usage, budget_status, estimate_cost, export_csv, filter_usage, load_usage, make_usage, summarize

def test_estimate_cost_exact():
    p=Price(Decimal("2"),Decimal("8"))
    assert estimate_cost(1_000_000,500_000,p)==Decimal("6.000000")

def test_invalid_tokens():
    with pytest.raises(ValueError): estimate_cost(-1,0,Price(Decimal("1"),Decimal("1")))

def test_ledger_roundtrip_unicode(tmp_path):
    path=tmp_path/"usage.jsonl"; u=make_usage("model-x",100,50,Price(Decimal("1"),Decimal("2")),"اختبار")
    append_usage(path,u); rows=load_usage(path)
    assert rows==[u]

def test_summary_by_model():
    p=Price(Decimal("1"),Decimal("1")); rows=[make_usage("a",1000,2000,p),make_usage("a",3000,4000,p),make_usage("b",1,1,p)]
    s=summarize(rows)
    assert s["requests"]==3 and s["by_model"]["a"]["requests"]==2 and s["input_tokens"]==4001

def test_filter_usage_model_label_and_time():
    p=Price(Decimal("1"),Decimal("1"))
    rows=[make_usage("a",1,1,p,"prod","2026-09-01T00:00:00Z"),make_usage("b",1,1,p,"dev","2026-09-10T00:00:00+00:00"),make_usage("a",1,1,p,"prod","2026-09-20T00:00:00Z")]
    assert len(filter_usage(rows,model="a",label="prod",since="2026-09-05T00:00:00Z"))==1
    assert len(filter_usage(rows,until="2026-09-10T00:00:00Z"))==2
    with pytest.raises(ValueError,match="since"): filter_usage(rows,since="2026-10-01T00:00:00Z",until="2026-09-01T00:00:00Z")

def test_export_csv_unicode(tmp_path):
    p=Price(Decimal("1"),Decimal("2")); row=make_usage("model-x",10,20,p,"عربي","2026-09-01T00:00:00Z")
    target=tmp_path/"usage.csv"
    assert export_csv(target,[row])==1
    with target.open(encoding="utf-8",newline="") as fh: data=list(csv.DictReader(fh))
    assert data[0]["label"]=="عربي" and data[0]["model"]=="model-x"

def test_budget_status():
    s=budget_status(Decimal("7.5"),Decimal("10"))
    assert s["remaining"]==Decimal("2.5") and s["percent"]==Decimal("75.00") and not s["exceeded"]

def test_corrupt_ledger_reports_line(tmp_path):
    p=tmp_path/"x.jsonl"; p.write_text('{"bad":true}\n',encoding="utf-8")
    with pytest.raises(ValueError,match="row 1"): load_usage(p)

def test_corrupt_ledger_rejects_negative_tokens(tmp_path):
    p=tmp_path/"x.jsonl"; p.write_text('{"model":"x","input_tokens":-1,"output_tokens":0,"cost_usd":"0","timestamp":"2026-09-01T00:00:00Z"}\n',encoding="utf-8")
    with pytest.raises(ValueError,match="row 1"): load_usage(p)
