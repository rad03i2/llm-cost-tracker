import json
from llm_cost_tracker.cli import main

def test_estimate_custom_price(capsys):
    code=main(["estimate","--model","custom","--input-tokens","1000000","--output-tokens","500000","--input-price","2","--output-price","8","--json"])
    assert code==0 and json.loads(capsys.readouterr().out)["cost_usd"]=="6.000000"

def test_record_then_summary(tmp_path,capsys):
    ledger=str(tmp_path/"u.jsonl")
    assert main(["record","--model","example-small","--input-tokens","1000","--output-tokens","500","--ledger",ledger])==0
    capsys.readouterr()
    assert main(["summary","--ledger",ledger,"--budget","1","--json"])==0
    data=json.loads(capsys.readouterr().out); assert data["requests"]==1 and data["budget"]["exceeded"] is False

def test_unknown_model_requires_prices(capsys):
    assert main(["estimate","--model","unknown","--input-tokens","1","--output-tokens","1"])==2
    assert "unknown model" in capsys.readouterr().err
