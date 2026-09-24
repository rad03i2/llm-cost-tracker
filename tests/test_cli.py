import csv
import json
from llm_cost_tracker.cli import main

def test_estimate_custom_price(capsys):
    code=main(["estimate","--model","custom","--input-tokens","1000000","--output-tokens","500000","--input-price","2","--output-price","8","--json"])
    assert code==0 and json.loads(capsys.readouterr().out)["cost_usd"]=="6.000000"

def test_record_then_filtered_summary_and_export(tmp_path,capsys):
    ledger=str(tmp_path/"u.jsonl")
    assert main(["record","--model","example-small","--input-tokens","1000","--output-tokens","500","--ledger",ledger,"--label","prod"])==0
    capsys.readouterr()
    assert main(["record","--model","example-medium","--input-tokens","100","--output-tokens","50","--ledger",ledger,"--label","dev"])==0
    capsys.readouterr()
    assert main(["summary","--ledger",ledger,"--label","prod","--budget","1","--json"])==0
    data=json.loads(capsys.readouterr().out); assert data["requests"]==1 and data["budget"]["exceeded"] is False
    output=str(tmp_path/"prod.csv")
    assert main(["export","--ledger",ledger,"--label","prod","--output",output,"--json"])==0
    result=json.loads(capsys.readouterr().out); assert result["rows"]==1
    with open(output,encoding="utf-8",newline="") as fh: rows=list(csv.DictReader(fh))
    assert rows[0]["label"]=="prod"

def test_unknown_model_requires_prices(capsys):
    assert main(["estimate","--model","unknown","--input-tokens","1","--output-tokens","1"])==2
    assert "unknown model" in capsys.readouterr().err

def test_invalid_filter_range(capsys):
    assert main(["summary","--since","2026-10-01T00:00:00Z","--until","2026-09-01T00:00:00Z"])==2
    assert "since" in capsys.readouterr().err
