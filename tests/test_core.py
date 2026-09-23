from decimal import Decimal
import json
import pytest
from llm_cost_tracker import Price, append_usage, budget_status, estimate_cost, load_usage, make_usage, summarize

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

def test_budget_status():
    s=budget_status(Decimal("7.5"),Decimal("10"))
    assert s["remaining"]==Decimal("2.5") and s["percent"]==Decimal("75.00") and not s["exceeded"]

def test_corrupt_ledger_reports_line(tmp_path):
    p=tmp_path/"x.jsonl"; p.write_text('{"bad":true}\n',encoding="utf-8")
    with pytest.raises(ValueError,match="row 1"): load_usage(p)
